# 🛰️ Satellite Image Preprocessing Suite: Master Overview
### *From Raw Swath Telemetry & Infrared Radiometry to Multi-Modal Deep Learning Tensors*
**Discipline:** Environmental Remote Sensing & Atmospheric Deep Learning  
**Platform:** DustML Forecasting System (北京科技大学 • USTB)  
**Target Domain:** East Asia ($70^\circ\text{E} - 135^\circ\text{E}, \ 25^\circ\text{N} - 55^\circ\text{N}$)

---

## 🌟 Executive Overview

Satellite Earth Observation (EO) provides continuous spatial views of airborne dust plumes that ground stations cannot match. However, raw satellite imagery cannot be directly fed into neural networks (e.g., the Coupled AI-GAMFS Backbone) due to:
1. **Instrument Swath Distortion:** Raw L1B granules suffer from orbital curvature, pixel deformation at swath edges ("bow-tie effect"), and missing geolocation metadata.
2. **Cloud vs. Dust Ambiguity:** In standard visible RGB channels, elevated mineral dust plumes look virtually identical to low-level clouds, ice cirrus, or bright desert sand.
3. **High Surface Albedo in Source Deserts:** Traditional Dark Target aerosol algorithms fail over bright surfaces like the Taklamakan and Gobi deserts ($R_{\text{surface}} > 0.30$).
4. **Cloud Gaps & Missing Pixels:** Cloud occlusion leaves severe missing-data gaps requiring physical spatio-temporal reconstruction.

This directory provides the complete technical specifications, mathematical inversion formulas, parameter dictionaries, and automated Python processing pipelines across the **5 Stages of Satellite Image Preprocessing**:

```
+---------------------------------------------------------------------------------------------------+
|                        5-STAGE SATELLITE IMAGE PREPROCESSING PIPELINE                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [STAGE 1: Raw L1B Calibration]     DN -> TOA Reflectance & Brightness Temperature (BT)           |
|                                     Bow-tie removal & Geolocation Grid Correction                 |
|                                     (Detailed in SATELLITE_CALIBRATION_AND_GEOMETRY.md)           |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 2: Cloud-vs-Dust Masking]   Split-Window BTD (11μm - 12μm < -0.5K)                        |
|                                     Tri-Spectral IR tests separating dust from cirrus/water       |
|                                     (Detailed in CLOUD_MASKING_AND_DUST_DISCRIMINATION.md)        |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 3: Deep Blue AOD Inversion] Deep Blue (0.412μm / 0.470μm) over bright desert sands        |
|                                     Spatio-Temporal DINEOF & Kriging Gap-Filling                  |
|                                     (Detailed in DEEP_BLUE_AOD_AND_GAP_FILLING.md)                |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 4: Multispectral Indices]   NDDI (Normalized Difference Dust Index)                       |
|                                     IDDI (Infrared Dust Difference) & WMO Dust RGB Composites     |
|                                     (Detailed in MULTISPECTRAL_DUST_INDICES_AND_RGB.md)           |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 5: Grid & Tensor Assembly]  Reprojection to WGS84, 5km Bilinear / Conservative Remap      |
|                                     Channel Normalization -> PyTorch Tensors [B, 3, 32, 32]       |
|                                     (Detailed in SPATIAL_REGRIDDING_AND_TENSOR_CONSTRUCTION.md)  |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 Preprocessing Suite Catalog

| Document | Focus & Core Methodology | Operational Output / Role in DustML |
| :--- | :--- | :--- |
| **[`SATELLITE_CALIBRATION_AND_GEOMETRY.md`](file:///c:/Users/hp/Desktop/China_project/Planning/image_preprocessing/SATELLITE_CALIBRATION_AND_GEOMETRY.md)** | Radiometric calibration, Digital Number (DN) conversion to TOA reflectance $\rho_{\text{TOA}}$ and Planck brightness temperature $T_b$, bow-tie distortion removal, and geolocation interpolation. | Corrected L1B calibrated radiance rasters for MODIS (Terra/Aqua) and FY-4A/B AGRI. |
| **[`CLOUD_MASKING_AND_DUST_DISCRIMINATION.md`](file:///c:/Users/hp/Desktop/China_project/Planning/image_preprocessing/CLOUD_MASKING_AND_DUST_DISCRIMINATION.md)** | Thermal infrared split-window $\text{BTD}(11\mu\text{m} - 12\mu\text{m}) < -0.5\text{K}$, tri-spectral test $(8.5\mu\text{m}, 11\mu\text{m}, 12\mu\text{m})$, and separation of silicate dust from water droplets and ice cirrus. | High-confidence binary dust flag mask and cloud exclusion mask. |
| **[`DEEP_BLUE_AOD_AND_GAP_FILLING.md`](file:///c:/Users/hp/Desktop/China_project/Planning/image_preprocessing/DEEP_BLUE_AOD_AND_GAP_FILLING.md)** | Deep Blue surface reflectance database inversion at $412\text{ nm}$ and $470\text{ nm}$ over bright desert sands, followed by spatio-temporal DINEOF / Kriging gap-filling for missing overcast pixels. | Gap-free continuous Aerosol Optical Depth ($\text{AOD}_{550}$) surface field. |
| **[`MULTISPECTRAL_DUST_INDICES_AND_RGB.md`](file:///c:/Users/hp/Desktop/China_project/Planning/image_preprocessing/MULTISPECTRAL_DUST_INDICES_AND_RGB.md)** | Spectral index calculation: NDDI (Normalized Difference Dust Index), IDDI (Infrared Dust Difference Index), DAI (Dust Aerosol Index), and standard WMO 24-bit Dust RGB composites (Red: 12-10.8μm, Green: 10.8-8.7μm, Blue: 10.8μm). | 3-channel optical and thermal dust feature maps for convolutional vision models. |
| **[`SPATIAL_REGRIDDING_AND_TENSOR_CONSTRUCTION.md`](file:///c:/Users/hp/Desktop/China_project/Planning/image_preprocessing/SPATIAL_REGRIDDING_AND_TENSOR_CONSTRUCTION.md)** | Reprojection from orbital swath geometry to standardized $0.05^\circ$ / 5km regular mesh over East Asia, min-max robust scaling, and formatting into PyTorch 4D tensor batches `[B, 3, 32, 32]`. | Ready-to-train deep learning tensor batches for the Coupled AI-GAMFS Backbone. |
