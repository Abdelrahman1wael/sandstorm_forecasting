# 02 主线B：多模态张量与时空图神经网络模型映射规范 (Line B Deep Learning Pipeline)

本规范详述主线B（端到端气象大模型、时空图神经网络与物理信息偏微分网络）中从高维网格影像到 PyTorch 张量缓存、深度子网络模块及统一大模型权重的端到端物理路径绑定。

---

## 1. 原始输入多模态数据路径 (Raw Multimodal Sources)

| 数据模态 | 原始物理文件路径 | 格式与通道 | 物理意义与空间覆盖 |
|:---|:---|:---:|:---|
| **ECMWF 动力气象网格** | `data/raw/nwp/ecmwf_hres_grid_2020_2025.nc` | NetCDF4 (6通道) | $u_{10}, v_{10}, T_{2m}, \text{BLH}, \text{SM}, \text{Surface Pressure}$ 覆盖东亚 $90^\circ\text{E} \sim 125^\circ\text{E}, 30^\circ\text{N} \sim 50^\circ\text{N}$ |
| **风云4号/MODIS 遥感反演** | `data/raw/satellite/fy4_dust_and_aod_mosaic.hdf` | HDF5 (3通道) | 通道1: 550nm AOD; 通道2: $12\mu\text{m}-11\mu\text{m}$ 分裂窗亮温差; 通道3: NDVI 植被覆盖指数 |
| **14节点走廊地理拓扑** | `data/raw/gis/corridor_nodes_14_metadata.json` | JSON / CSV | 14个关键起沙区、输送通道与受体城市的经纬度、海拔与空间邻近距离 |
| **历史地面监测时序** | `data/raw/ground/station_seq_hourly.parquet` | Parquet | 过去24小时各节点连续气象与 $\text{PM}_{10}$ 序列 |

---

## 2. 规整张量构建与 PyTorch 缓存路径 (Processed Tensor Store)

### 2.1 张量规整生成脚本
- **执行脚本文件**：`scripts/data/build_line_b_spatiotemporal_tensors.py`
- **执行功能**：
  1. 将连续区域 ECMWF 栅格下采样并投影为正则网格 `[B, 6, 16, 16]`；
  2. 将多光谱卫星拼接影像双三次插值重采样为 `[B, 3, 32, 32]`；
  3. 基于大圆距离（Haversine Distance）与年均高空风向通量构建静态归一化邻接矩阵 $\hat{A} = \tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}}$；
  4. 滑动时间窗口封装历史 24 小时节点特征序列。

### 2.2 产出的 PyTorch 张量持久化存储路径
- **张量存储目录**：`data/processed/tensors/`
  - `nwp_grid_16x16.pt`：气象动力场张量 `torch.Size([N_batches, 6, 16, 16])`
  - `satellite_grid_32x32.pt`：卫星反演张量 `torch.Size([N_batches, 3, 32, 32])`
  - `node_features.pt`：当前时间步 14 节点特征 `torch.Size([N_batches, 14, 12])`
  - `seq_features_24h.pt`：过去 24 小时时序张量 `torch.Size([N_batches, 24, 14, 12])`
  - `targets_lead_pm10.pt`：未来 6 个延伸期步长浓度目标 `torch.Size([N_batches, 14, 6])`
  - `hazard_classes.pt`：未来 6 个步长 CMA 预警真实标签 `torch.Size([N_batches, 14, 6])`
- **图拓扑矩阵文件**：`data/processed/graph/adjacency_matrix_14x14.npy`

---

## 3. PyTorch 数据集对接与深度模型组件映射 (Model Components & Code Paths)

```mermaid
graph TD
    subgraph "PyTorch Dataset 中枢 (dataset.py)"
        D["SpatiotemporalDustDataset"]
        D -->|nwp_grid [B,6,16,16]| B1["aigamfs_backbone.py<br>(AI-GAMFS 3D/2D CNN Encoder)"]
        D -->|sat_grid [B,3,32,32]| B1
        D -->|seq_features [B,24,14,12]| G1["st_gnn.py<br>(ST-GNN 时空图卷积)"]
        D -->|adj_matrix [14,14]| G1
    end

    subgraph "核心网络融合与物理约束"
        B1 -->|Visual Token Embeddings| U["unified_model.py<br>(UnifiedDeepDustModel)"]
        G1 -->|Graph Spatial Dynamics| U
        U --> P["pinn_core.py<br>(PINN 质量守恒与跃移损失)"]
    end

    subgraph "多任务输出头与权重保存"
        U --> O1["单调分位数预测<br>[B, 14, 6, 3] (P10/P50/P90)"]
        U --> O2["CMA 5级预警概率<br>[B, 14, 6, 5] Logits"]
        U --> W["checkpoints/line_b/best_unified_model.pth"]
    end
```

### 3.1 核心深度学习脚本与代码映射表
| 深度网络模块 | 物理代码实现文件 | 对应 PyTorch 核心类名 | 接收的张量形状与字段 |
|:---|:---|:---|:---|
| **视觉气象主干** | `Ai Pipline/models/deep_learning/aigamfs_backbone.py` | `AIGAMFSBackbone` | `nwp_grid`: `[B, 6, 16, 16]`<br>`satellite_grid`: `[B, 3, 32, 32]` |
| **时空图卷积网络** | `Ai Pipline/models/deep_learning/st_gnn.py` | `SpatiotemporalGNN` | `seq_features`: `[B, 24, 14, 12]`<br>`adj_matrix`: `[14, 14]` |
| **物理信息偏微分核** | `Ai Pipline/models/deep_learning/pinn_core.py` | `DustPhysicsInformedLoss` | `pred_pm10`, `u_star`, `u_star_t`, `wind_u`, `wind_v` |
| **统一大模型主干** | `Ai Pipline/models/deep_learning/unified_model.py` | `UnifiedDeepDustModel` | 融合视觉与图拓扑隐向量，输出多步长分位数与分类 |
| **端到端训练入口** | `Ai Pipline/training/train_line_b.py` | `LineBTrainer.fit()` | 组织多任务加权反向传播与早停验证 |

### 3.2 模型检查点权重存储规范
- **最优模型权重（Best Validation Loss）**：  
  `Ai Pipline/models/checkpoints/line_b/best_unified_model.pth`
- **最后周期备份（Last Epoch Backup）**：  
  `Ai Pipline/models/checkpoints/line_b/last_checkpoint_epoch100.pth`
- **优化器与学习率调度状态**：  
  `Ai Pipline/models/checkpoints/line_b/optimizer_state.pth`

---

## 4. 在线微服务挂载与端点调用 (Serving Pipeline)

- **API 驱动代码**：`Ai Pipline/api/app.py`
- **加载逻辑**：
  ```python
  import torch
  from models.deep_learning.unified_model import UnifiedDeepDustModel

  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model_deep = UnifiedDeepDustModel(node_feats=12, seq_len=24, n_nodes=14)
  checkpoint = torch.load("models/checkpoints/line_b/best_unified_model.pth", map_location=device)
  model_deep.load_state_dict(checkpoint["model_state_dict"])
  model_deep.eval()
  ```
- **对外暴露端点**：
  - `POST /api/v1/forecast/line-b/full-graph`
  - `POST /api/v1/forecast/blend/ensemble`（Line A 与 Line B 动态融合端点）。
