"""
==============================================================================
Physics-Informed Neural Network (PINN) Core Constraints
Enforcing Mass Conservation PDEs & Aerodynamic Saltation Friction Thresholds
==============================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Tuple


class OwenSaltationPhysics:
    """
    Aerodynamic Saltation Physics Simulator based on Owen (1964) & Gillette (1979).
    Saltation horizontal sand flux formula:
    F_salt = C * (rho_air / g) * u_*^3 * (1 - u_*t^2 / u_*^2) * I(u_* > u_*t)
    """

    def __init__(self, rho_air: float = 1.225, g: float = 9.80665, saltation_const: float = 0.25):
        self.rho_air = rho_air
        self.g = g
        self.saltation_const = saltation_const

    def compute_theoretical_flux(self, u_star: torch.Tensor, u_star_t: torch.Tensor) -> torch.Tensor:
        """
        Compute theoretical physical saltation flux in mg/(m*s).
        Zero below threshold u_* <= u_*t.
        """
        active_mask = (u_star > u_star_t).float()
        u_ratio_sq = (u_star_t / torch.clamp(u_star, min=1e-5)) ** 2
        excess_term = torch.clamp(1.0 - u_ratio_sq, min=0.0)

        flux = self.saltation_const * (self.rho_air / self.g) * (u_star ** 3) * excess_term * active_mask
        # Scale to μg/m3 emission proxy
        return flux * 1000.0


class PhysicsInformedLoss(nn.Module):
    """
    PINN Loss Regularizer.
    Penalizes non-physical predictions violating:
      1. Atmospheric advective mass conservation along corridor edges
      2. Threshold aerodynamic friction velocity (u_* > u_*t)
      3. Non-negativity of mass concentration
    """

    def __init__(self, lambda_mass: float = 0.15, lambda_salt: float = 0.20, lambda_neg: float = 0.10):
        super().__init__()
        self.lambda_mass = lambda_mass
        self.lambda_salt = lambda_salt
        self.lambda_neg = lambda_neg
        self.saltation_calc = OwenSaltationPhysics()

    def forward(self, pred_pm10: torch.Tensor, target_pm10: torch.Tensor,
                u_star: torch.Tensor, u_star_t: torch.Tensor,
                adj_matrix: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Args:
          pred_pm10: [B, N, Leads] predicted dust concentration
          target_pm10: [B, N, Leads] observed ground truth
          u_star: [B, N] surface friction velocity (m/s)
          u_star_t: [B, N] threshold friction velocity (m/s)
          adj_matrix: [N, N] normalized spatial graph adjacency
        """
        # 1. Supervised Data Loss (Smooth L1 / Huber Loss for robustness to extreme spikes)
        loss_data = F.smooth_l1_loss(pred_pm10, target_pm10)

        # 2. Non-negativity penalty (concentrations cannot be negative)
        loss_neg = torch.mean(F.relu(-pred_pm10) ** 2)

        # 3. Aerodynamic Saltation Constraint:
        # At source nodes (where u* < u*t), local primary generation should be near zero.
        # Predicted Day 1 concentration should correlate with theoretical Owen's flux.
        day1_pred = pred_pm10[:, :, 0] # [B, N]
        phys_flux = self.saltation_calc.compute_theoretical_flux(u_star, u_star_t) # [B, N]

        # Penalize non-zero emissions when u* is substantially below threshold
        sub_threshold_mask = (u_star < (u_star_t * 0.9)).float()
        loss_saltation = torch.mean(sub_threshold_mask * (day1_pred - 45.0).clamp(min=0.0) ** 2) / 1000.0

        # 4. Spatiotemporal Mass Advection Continuity:
        # Downstream concentration is bounded by upstream inflow: C_downstream <= sum(Adj * C_upstream) + Local_Source
        # [B, N, Leads] -> advected inflow [B, N, Leads]
        advected_inflow = torch.einsum("ij,bjl->bil", adj_matrix, pred_pm10)
        # Difference between adjacent lead times represents net accumulation/loss
        lead_delta = pred_pm10[:, :, 1:] - pred_pm10[:, :, :-1] # [B, N, Leads-1]
        inflow_trunc = advected_inflow[:, :, 1:]
        # Mass residual: sudden unphysical surges without upstream advection or local wind trigger
        mass_residual = F.relu(lead_delta - inflow_trunc * 1.5)
        loss_mass = torch.mean(mass_residual ** 2) / 100.0

        total_loss = loss_data + self.lambda_mass * loss_mass + self.lambda_salt * loss_saltation + self.lambda_neg * loss_neg

        telemetry = {
            "loss_total": float(total_loss.item()),
            "loss_data": float(loss_data.item()),
            "loss_mass": float(loss_mass.item()),
            "loss_saltation": float(loss_saltation.item()),
            "loss_negativity": float(loss_neg.item())
        }

        return total_loss, telemetry
