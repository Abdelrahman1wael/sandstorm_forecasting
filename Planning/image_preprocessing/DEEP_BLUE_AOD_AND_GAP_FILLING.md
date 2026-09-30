# 🌊 Deep Blue Aerosol Optical Depth (AOD) & Spatio-Temporal Gap Filling
### *Aerosol Inversion over High-Albedo Deserts & Continuous Field Reconstruction*
**Theoretical Foundation:** Deep Blue Algorithm (Hsu et al., 2004, 2013) & Spatiotemporal DINEOF  
**Sensors:** MODIS (MOD04_L2 / MYD04_L2), VIIRS (AERDB_L2), FY-4A AGRI  
**Output Target:** Continuous, Gap-Free $550\text{ nm}$ Aerosol Optical Depth Field ($\text{AOD}_{550}$)

---

## 🎯 1. Operational Goal & Scientific Importance

### 1.1 Why Standard Aerosol Inversion (Dark Target) Fails over Deserts
The classic NASA Dark Target algorithm relies on dense, dark green vegetation where surface reflectance at $2.1\mu\text{m}$ is very low ($R < 0.05$). Over arid East Asian terrain (the Taklamakan, Badain Jaran, Tengger, and Gobi deserts), the bare quartz and sand dunes have extremely high surface reflectance:
$$R_{\text{surface}}(0.66\mu\text{m}) > 0.35, \quad R_{\text{surface}}(2.1\mu\text{m}) > 0.45$$
At these wavelengths, the underlying desert is brighter than the atmospheric dust layer, causing Dark Target inversions to fail completely and output missing values (`NaN`).

### 1.2 The Deep Blue Solution
The **Deep Blue (DB)** algorithm exploits a critical physical property of desert minerals: **iron oxides (hematite, goethite)** strongly absorb ultraviolet and blue light. Consequently, in the **deep blue spectrum ($412\text{ nm}$ and $470\text{ nm}$)**, desert surfaces appear relatively dark ($R_{\text{surface}} \approx 0.06 - 0.12$). This allows high-accuracy retrieval of atmospheric aerosol optical depth even over bright desert dunes.

---

## 📐 2. Mathematical Inversion Formulation

```
Top-of-Atmosphere (TOA) Reflectance Formulation:
ρ_TOA(λ, θ_0, θ, φ) = ρ_path(λ, θ_0, θ, φ; τ_550, ω_0, P) + [ T(θ_0) * T(θ) * ρ_surface(λ) ] / [ 1 - s(λ) * ρ_surface(λ) ]
```

Where:
* $\tau_{550}$: Aerosol Optical Depth at $550\text{ nm}$ (the target variable to invert).
* $\rho_{\text{path}}$: Atmospheric path reflectance contributed by molecular Rayleigh scattering and particulate aerosol scattering.
* $\omega_0$: Single scattering albedo of the dust model ($\sim 0.89 - 0.93$ in blue wavelengths).
* $P(\Theta)$: Aerosol scattering phase function for non-spherical dust particles (approximated via T-matrix spheroid distributions).
* $T(\theta_0), T(\theta)$: Downward solar and upward sensor atmospheric transmission factors.
* $s(\lambda)$: Atmospheric spherical albedo.
* $\rho_{\text{surface}}(\lambda)$: Pre-calculated surface reflectance retrieved from the global **Deep Blue Surface Reflectance Database** (composited from multi-year minimum clear-sky observations).

### The Inversion Protocol:
Given known viewing angles $(\theta_0, \theta, \phi)$ and pre-stored surface albedo $\rho_{\text{surface}}$, radiative transfer Look-Up Tables (LUTs generated via 6S/DISORT) are searched to find the $\tau_{550}$ that minimizes the residual between observed and simulated TOA reflectance at $412\text{ nm}$ and $470\text{ nm}$:

$$\tau_{550}^* = \arg\min_{\tau} \sum_{\lambda \in \{412, 470\}} \left| \rho_{\text{TOA, obs}}(\lambda) - \rho_{\text{TOA, LUT}}(\lambda; \tau) \right|$$

---

## 🧩 3. Spatio-Temporal Gap Filling Pipeline

Because cloud decks and sensor swaths leave $25\text{--}40\%$ of pixels empty on any given day, an automated 3-stage gap-filling pipeline reconstructs a $100\%$ continuous field for deep neural networks:

```
[Raw Deep Blue AOD Swaths (MOD04 / MYD04)]
                    │
                    ▼
[Stage 1: Multi-Orbit Fusion]      Combine Terra (Morning ~10:30) + Aqua (Afternoon ~13:30)
                    │
                    ▼
[Stage 2: Spatiotemporal DINEOF]   Data Interpolating Empirical Orthogonal Functions
                                   Decomposes AOD field into leading spatial/temporal modes:
                                   AOD(x, t) ≈ sum_{k=1}^K σ_k u_k(x) v_k(t)
                    │
                    ▼
[Stage 3: Background CAMS Anchor]  For remaining cloud holes > 300 km:
                                   Blend with CAMS / MERRA-2 Aerosol Reanalysis baseline
                    │
                    ▼
[100% Continuous 5km AOD Grid for Deep Neural Input]
```

---

## ⚙️ 4. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `target_wavelength`| `float` | `550.0` | Fixed ($550\text{ nm}$) | Reference wavelength for visible aerosol optical depth. |
| `max_aod_threshold`| `float` | `5.0` | `4.0 - 5.0` | Upper physical retrieval ceiling for dense dust plumes. |
| `min_aod_threshold`| `float` | `0.0` | `0.0 - 0.05` | Lower physical baseline for pristine clean mountain air. |
| `dineof_max_modes` | `int` | `10` | `5 - 15` | Maximum number of EOF spatial modes retained in DINEOF iterative reconstruction. |
| `dineof_convergence`|`float` | `1e-3` | `1e-4 - 1e-2` | Relative error tolerance for DINEOF convergence. |
| `kriging_n_neighbors`|`int` | `16` | `12 - 24` | Local spatial neighbors evaluated for localized Ordinary Kriging infill. |
| `cams_blend_weight`| `float` | `0.30` | `0.20 - 0.50` | Blending weight assigned to CAMS numerical background in deep cloud holes. |

---

## 💡 5. Automated Python Gap-Filling Implementation

```python
import numpy as np
from scipy.ndimage import distance_transform_edt

def spatio_temporal_dineof_infill(aod_cube: np.ndarray, max_modes: int = 10, tol: float = 1e-3) -> np.ndarray:
    """
    Data Interpolating Empirical Orthogonal Functions (DINEOF)
    Reconstructs missing pixels in a 3D spatiotemporal AOD raster stack [Time, Height, Width].
    """
    T, H, W = aod_cube.shape
    flat_data = aod_cube.reshape(T, H * W).copy()
    
    # Identify missing mask
    missing_mask = np.isnan(flat_data)
    if not np.any(missing_mask):
        return aod_cube
    
    # Initial guess: spatial mean of valid pixels
    spatial_mean = np.nanmean(flat_data, axis=0, keepdims=True)
    spatial_mean = np.nan_to_num(spatial_mean, nan=0.15)
    flat_data[missing_mask] = np.broadcast_to(spatial_mean, flat_data.shape)[missing_mask]
    
    prev_state = flat_data.copy()
    
    # Iterative SVD reconstruction
    for mode in range(1, max_modes + 1):
        for iteration in range(20):
            # Singular Value Decomposition
            U, S, Vt = np.linalg.svd(flat_data, full_matrices=False)
            
            # Truncated reconstruction using top 'mode' components
            recon = np.dot(U[:, :mode] * S[:mode], Vt[:mode, :])
            
            # Update only missing positions
            flat_data[missing_mask] = recon[missing_mask]
            
            # Check convergence
            delta = np.linalg.norm(flat_data - prev_state) / max(np.linalg.norm(prev_state), 1e-6)
            prev_state = flat_data.copy()
            if delta < tol:
                break

    reconstructed_cube = np.clip(flat_data.reshape(T, H, W), 0.0, 5.0)
    return reconstructed_cube

def anchor_with_cams_reanalysis(aod_gap_filled: np.ndarray, cams_aod: np.ndarray, original_missing_mask: np.ndarray) -> np.ndarray:
    """
    Blends reconstructed satellite AOD with CAMS reanalysis for massive persistent cloud holes.
    """
    # Calculate distance to nearest valid satellite pixel
    dist = distance_transform_edt(original_missing_mask)
    
    # Sigmoid blending: far from valid pixels (>50 km), transition toward CAMS
    alpha = 1.0 / (1.0 + np.exp(-(dist - 10.0) / 5.0))
    final_aod = (1.0 - alpha) * aod_gap_filled + alpha * cams_aod
    return np.clip(final_aod, 0.0, 5.0)
```
