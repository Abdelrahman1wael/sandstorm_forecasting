# 🖥️ Phase 1 • Subfolder 2: Computing & Software Environment
### *Hardware Provisioning, PyTorch CUDA Accelerators, Conda Environments & Tooling*
**Phase Horizon:** September 2025 – December 2025  
**Parent Phase:** Phase 1 (Preparation and Feasibility)

---

## 🎯 1. Operational Goal & Hardware Specifications

Phase 1.2 ensures all local and high-performance computing (HPC) environments are provisioned with required GPU accelerators, CUDA drivers, and reproducible Python environments:

### Hardware Requirements:
* **Workstation / Local Dev:** 8-Core CPU, 32GB RAM, NVIDIA RTX GPU (8GB+ VRAM) for local testing.
* **HPC Cluster / Cloud Server:** NVIDIA A100 / RTX 4090 (24GB+ VRAM) for training deep spatiotemporal foundation models (`unified_model.py` across 2018–2025 historical data).

---

## ⚙️ 2. Reproducible Conda Environment Setup

```bash
# 1. Create isolated conda environment
conda create -n dustml python=3.10 -y
conda activate dustml

# 2. Install PyTorch with CUDA support (e.g. CUDA 12.1)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 3. Install core Machine Learning & Spatial dependencies
pip install lightgbm xgboost catboost scikit-learn numpy scipy pandas polars
pip install geopandas rasterio rioxarray xarray netCDF4 h5py pyproj shapely

# 4. Install Operational Web & Video production dependencies
pip install fastapi uvicorn pydantic edge-tts pillow requests joblib
```

---

## 📋 3. Environment Verification Script

```python
import torch
import lightgbm
import sklearn

print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device Name:", torch.cuda.get_device_name(0))
    print("VRAM (GB):", torch.cuda.get_device_properties(0).total_memory / 1e9)
print("PyTorch Version:", torch.__version__)
print("LightGBM Version:", lightgbm.__version__)
```
