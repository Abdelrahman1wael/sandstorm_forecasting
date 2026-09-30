"""
==============================================================================
AI-GAMFS Backbone: Coupled Aerosol-Meteorology Multi-Modal Foundation Encoder
Ingests Gridded NWP Dynamic Fields + Satellite Imagery + Ground Reanalysis
==============================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CoupledAIGAMFSEncoder(nn.Module):
    """
    Coupled AI-GAMFS Aerosol-Meteorology Large Model Encoder Backbone.
    Extracts multi-scale planetary atmospheric features from gridded NWP fluid dynamics
    and high-resolution satellite aerosol optical depth rasters.
    """

    def __init__(self, nwp_channels: int = 6, sat_channels: int = 3, embed_dim: int = 128):
        super().__init__()
        self.embed_dim = embed_dim

        # NWP Atmospheric Grid Encoder [B, 6, 16, 16] -> [B, EmbedDim]
        self.nwp_conv = nn.Sequential(
            nn.Conv2d(nwp_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1), # -> [B, 64, 8, 8]
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, embed_dim)
        )

        # Satellite Imagery Encoder [B, 3, 32, 32] -> [B, EmbedDim]
        self.sat_conv = nn.Sequential(
            nn.Conv2d(sat_channels, 32, kernel_size=3, stride=2, padding=1), # -> [B, 32, 16, 16]
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1), # -> [B, 64, 8, 8]
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, embed_dim)
        )

        # Cross-modal fusion gate
        self.fusion_gate = nn.Sequential(
            nn.Linear(embed_dim * 2, embed_dim),
            nn.Sigmoid()
        )
        self.fusion_proj = nn.Linear(embed_dim * 2, embed_dim)
        self.layer_norm = nn.LayerNorm(embed_dim)

    def forward(self, nwp_grid: torch.Tensor, sat_grid: torch.Tensor) -> torch.Tensor:
        """
        nwp_grid: [B, 6, 16, 16]
        sat_grid: [B, 3, 32, 32]
        Returns: [B, EmbedDim]
        """
        h_nwp = self.nwp_conv(nwp_grid)
        h_sat = self.sat_conv(sat_grid)

        concat = torch.cat([h_nwp, h_sat], dim=-1)
        gate = self.fusion_gate(concat)
        fused = gate * h_nwp + (1.0 - gate) * h_sat
        fused = self.layer_norm(self.fusion_proj(concat) + fused)

        return fused
