"""
==============================================================================
Training Pipeline: Main Line B Physics-Informed Deep Learning (PINN + ST-GNN)
Coupled AI-GAMFS Foundation Backbone with Automated Conservation Regularization
==============================================================================
"""

import os
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
import numpy as np
from typing import Dict, Any

try:
    from ..data.dataset import get_dl_dataloaders
    from ..models.deep_learning.unified_model import DustMLUnifiedDeepModel
    from ..models.deep_learning.pinn_core import PhysicsInformedLoss
except (ImportError, ValueError):
    from data.dataset import get_dl_dataloaders
    from models.deep_learning.unified_model import DustMLUnifiedDeepModel
    from models.deep_learning.pinn_core import PhysicsInformedLoss


def run_dl_training_pipeline(
    epochs: int = 15,
    batch_size: int = 16,
    lr: float = 1e-3,
    save_dir: str = "models/checkpoints/line_b",
    device: str = "cpu",
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Executes end-to-end PINN Deep Spatiotemporal Training.
    """
    if verbose:
        print("=" * 75)
        print("🌌 [Main Line B] Starting Physics-Informed Deep Learning Training...")
        print("   Backbone: Coupled AI-GAMFS Multi-Modal Encoder + ST-GNN + PINN")
        print("=" * 75)

    os.makedirs(save_dir, exist_ok=True)
    device = torch.device(device if torch.cuda.is_available() and device != "cpu" else "cpu")

    # 1. Prepare Data Loaders
    train_loader, val_loader, adj_matrix = get_dl_dataloaders(batch_size=batch_size)
    adj_matrix = adj_matrix.to(device)

    # 2. Instantiate Model and Physics Loss
    model = DustMLUnifiedDeepModel(
        n_stations=14,
        n_lead_times=6,
        n_classes=5,
        hidden_dim=64
    ).to(device)

    pinn_criterion = PhysicsInformedLoss(lambda_mass=0.15, lambda_salt=0.20, lambda_neg=0.10)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    best_val_rmse = float("inf")
    best_checkpoint_path = os.path.join(save_dir, "dustml_dl_best.pth")
    training_history = []

    # 3. Training Loop
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss_total = 0.0
        train_loss_mass = 0.0
        train_loss_salt = 0.0
        n_train_batches = 0

        for batch in train_loader:
            nwp_grid = batch["nwp_grid"].to(device)
            sat_grid = batch["satellite_grid"].to(device)
            seq_feats = batch["seq_features"].to(device)
            node_feats = batch["node_features"].to(device)
            targets_pm10 = batch["targets_pm10"].to(device)

            # Node friction velocities: index 1 is u*, index 2 is u*t
            u_star = node_feats[:, :, 1]
            u_star_t = node_feats[:, :, 2]

            optimizer.zero_grad()
            outputs = model(nwp_grid, sat_grid, seq_feats, node_feats, adj_matrix)
            pred_p50 = outputs["p50"]

            # Compute PINN regularized loss
            loss, telemetry = pinn_criterion(
                pred_pm10=pred_p50,
                target_pm10=targets_pm10,
                u_star=u_star,
                u_star_t=u_star_t,
                adj_matrix=adj_matrix
            )

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
            optimizer.step()

            train_loss_total += telemetry["loss_total"]
            train_loss_mass += telemetry["loss_mass"]
            train_loss_salt += telemetry["loss_saltation"]
            n_train_batches += 1

        scheduler.step()

        # 4. Validation Loop
        model.eval()
        val_sq_errors = []
        with torch.no_grad():
            for batch in val_loader:
                nwp_grid = batch["nwp_grid"].to(device)
                sat_grid = batch["satellite_grid"].to(device)
                seq_feats = batch["seq_features"].to(device)
                node_feats = batch["node_features"].to(device)
                targets = batch["targets_pm10"].to(device)

                outputs = model(nwp_grid, sat_grid, seq_feats, node_feats, adj_matrix)
                preds = outputs["p50"]
                sq_err = (preds - targets) ** 2
                val_sq_errors.append(sq_err.cpu().numpy())

        val_rmse = float(np.sqrt(np.mean(np.concatenate(val_sq_errors))))
        avg_train_loss = train_loss_total / max(1, n_train_batches)
        avg_mass_loss = train_loss_mass / max(1, n_train_batches)
        avg_salt_loss = train_loss_salt / max(1, n_train_batches)

        # Track history
        epoch_record = {
            "epoch": epoch,
            "train_loss": round(avg_train_loss, 4),
            "mass_loss": round(avg_mass_loss, 4),
            "saltation_loss": round(avg_salt_loss, 4),
            "val_rmse": round(val_rmse, 2)
        }
        training_history.append(epoch_record)

        if val_rmse < best_val_rmse:
            best_val_rmse = val_rmse
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_rmse": val_rmse,
                "adj_matrix": adj_matrix.cpu()
            }, best_checkpoint_path)

        if verbose and (epoch % max(1, epochs // 5) == 0 or epoch == epochs or epoch == 1):
            print(f"   Epoch [{epoch:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Mass Res: {avg_mass_loss:.4f} | Salt Res: {avg_salt_loss:.4f} | Val RMSE: {val_rmse:.2f} μg/m³")

    if verbose:
        print(f"\n🏆 Best Deep Learning Val RMSE: {best_val_rmse:.2f} μg/m³")
        print(f"💾 Checkpoint saved to '{best_checkpoint_path}'")

    return {
        "best_val_rmse": best_val_rmse,
        "checkpoint_path": best_checkpoint_path,
        "training_history": training_history
    }


if __name__ == "__main__":
    run_dl_training_pipeline(epochs=10)
