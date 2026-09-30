# 📐 Chapters 3 & 4: 数据融合与双线预测模型构建 (Data & Methodology Standards)
### *Writing Guide & Methodological Specifications for Master's Thesis Chapters 3 & 4*
**Designation:** 第三章 多源数据系统与特征工程 / 第四章 基于物理约束的双线沙尘暴预测模型构建  
**Standard Word Count Target:** 18,000 – 24,000 Chinese characters across both chapters (~35–45 thesis pages)  
**Degree Standard:** University of Science and Technology Beijing (USTB) • Environmental Engineering

---

## 🎯 Chapter 3 Blueprint: 多源异构数据系统与特征工程

```
第三章 多源异构数据系统与特征工程 (Chapter 3: Data System & Feature Engineering)
├── 3.1 多源异构气象与遥感数据源描述 (Multi-Source Data Descriptions)
│   ├── 3.1.1 数值天气预报产品 (ECMWF IFS 高分辨率与集合预报, CMA-GFS)
│   ├── 3.1.2 大气再分析资料 (ERA5 压力层与近地面层物理场)
│   ├── 3.1.3 卫星遥感观测 (MODIS 深蓝 AOD, FY-4A/B 静止气象卫星辐射计)
│   └── 3.1.4 地面环境与气象监测网络 (生态环境部 1500+ 国控站与 CMA 地面站)
├── 3.2 数据质量控制、剔异与时空对齐 (Quality Control & Harmonization)
│   ├── 3.2.1 地面传感器机械冻结 (零方差平线) 与滚动 MAD 动态剔尖
│   ├── 3.2.2 负值漂移截断与分层插补 (Akima 保形样条与空间克里金)
│   ├── 3.2.3 UTC 时区统一与 8 小时昼夜相位漂移消除
│   └── 3.2.4 5km WGS84 规则网格双线性与面积保守重采样
├── 3.3 四层级领域先验特征工程体系 (4-Tier Domain Feature Engineering)
│   ├── 3.3.1 动力学与热力学特征 (10m风速、风切变、Z500、逆温层位势高度)
│   ├── 3.3.2 地表与土壤状态特征 (0-7cm 土壤含水率、粗糙度 z0、NDVI 距平、积雪覆盖)
│   ├── 3.3.3 地形地貌与源区距离 (DEM 高程、坡度、地表粗糙度指数 TRI、沙源欧氏距离)
│   └── 3.3.4 时间周期与大尺度遥相关指数 (DOY 周期谐波、极涡指数、北极涛动 AO)
└── 3.4 样本集严格时序划分协议 (Dataset Partitioning & Walk-Forward Validation)
```

---

## 🎯 Chapter 4 Blueprint: 基于物理约束的双线预测模型构建

```
第四章 基于物理约束的双线沙尘暴预测模型构建 (Chapter 4: Dual-Line Modeling & PINN)
├── 4.1 双线预测架构设计哲学 (Dual-Line Modeling Philosophy)
│   ├── 4.1.1 主线 A 与主线 B 的互补性与动力学定位
│   └── 4.1.2 预报时效衰减 (Lead-Time Decay) 与时效交叉加权融合机理
├── 4.2 主线 A: 数值预报统计后处理与树集成模型 (Main Line A: NWP ML Bias Correction)
│   ├── 4.2.1 系统性时空残差学习数学表征: ε(s, t, L) = y_obs - y_nwp
│   ├── 4.2.2 LightGBM (GOSS 梯度采样与 EFB 特征捆绑优化)
│   ├── 4.2.3 CatBoost (有序目标统计与对称不经意树构建)
│   ├── 4.2.4 XGBoost (二阶泰勒展开与梯度增益分裂)
│   └── 4.2.5 约束 Ridge 回归 Stacking 融合元学习器
├── 4.3 主线 B: 端到端深度时空物理约束基座模型 (Main Line B: Deep PINN Foundation)
│   ├── 4.3.1 耦合 AI-GAMFS 双模态气象-气溶胶视觉编码器 (自适应 Sigmoid 门控)
│   ├── 4.3.2 14 节点东亚沙尘输送走廊时空图神经网络 (ST-GNN 双向切比雪夫扩散)
│   └── 4.3.3 物理信息神经网络 (PINN) 损失函数注入:
│       • Owen (1964) 空气动力学起沙跃移阈值 (u* > u*t) 罚函数
│       • 大气平流质量连续性偏微分方程 (Mass Continuity PDE) 沿走廊边的守恒约束
│       • 浓度非负性物理边界硬约束
├── 4.4 分位数不确定性估计与单调性保证 (Quantile Uncertainty Head)
│   ├── 4.4.1 Pinball 检验损失函数数学推导 (τ = 0.10, 0.50, 0.90)
│   └── 4.4.2 累积 Softplus Delta 参数化单调性证明: 0 <= P10 <= P50 <= P90
├── 4.5 顾及极端不平衡的代价敏感预警分类器 (Cost-Sensitive Hazard Classifier)
│   ├── 4.5.1 中国气象局 (CMA) 五级沙尘预警标准映射
│   ├── 4.5.2 非对称代价矩阵设计 (漏报惩罚 50x 于虚警)
│   └── 4.5.3 保序回归 (Isotonic Regression) 概率校准
└── 4.6 本章小结 (Chapter Summary)
```

---

## 📐 Key Mathematical Equations to Present in Chapter 4

### 1. Dual-Line Blending Across Lead Times ($L \in [72\text{h}, 360\text{h}]$):
$$\hat{y}_{\text{final}}(s, t+L) = w_A(L) \cdot \hat{y}_{\text{LineA}}(s, t+L) + (1 - w_A(L)) \cdot \hat{y}_{\text{LineB}}(s, t+L)$$
$$w_A(L) = \frac{1}{1 + \exp\left(\frac{L - 168\text{h}}{48\text{h}}\right)}$$

### 2. Multi-Task PINN Conservation Objective:
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{Huber}}(y, \hat{y}) + 0.15 \mathcal{L}_{\text{mass}} + 0.20 \mathcal{L}_{\text{saltation}} + 0.10 \mathcal{L}_{\text{negativity}}$$
$$\mathcal{L}_{\text{saltation}} = \frac{1}{B \cdot N} \sum_{b, n} \mathbb{I}\left(u_{*, b, n} < 0.9 \, u_{*t, b, n}\right) \cdot \left(\max\left(0, \hat{C}_{b, n, t=1} - 45.0\right)\right)^2$$
$$\mathcal{L}_{\text{mass}} = \frac{1}{B \cdot N \cdot (L-1)} \sum_{b, n, l} \left( \text{ReLU}\left( (\hat{C}_{l+1} - \hat{C}_l) - 1.5 \cdot \text{Inflow}_l \right) \right)^2$$

### 3. Monotonic Quantile Non-Crossing Guarantee:
$$\hat{y}_{P50} = \text{softplus}\left(\mathbf{W}_{50} \mathbf{h} + \mathbf{b}_{50}\right)$$
$$\hat{y}_{P10} = \max\left(0, \ \hat{y}_{P50} - \text{softplus}(\mathbf{W}_{10} \mathbf{h})\right)$$
$$\hat{y}_{P90} = \hat{y}_{P50} + \text{softplus}(\mathbf{W}_{90} \mathbf{h})$$
$$\implies 0 \le \hat{y}_{P10} \le \hat{y}_{P50} \le \hat{y}_{P90} \quad \forall (s, t, l)$$

---

## 📋 Evaluation Checklist for Thesis Chapters 3 & 4

- [x] **Zero Raw NWP Overwrite:** Clearly state that raw numerical physics are preserved as background forcing tensors.
- [x] **Walk-Forward Validation:** Ensure no future data leaks into the training sets.
- [x] **Units & Symbols Standard:** Every variable in equations must have explicit units ($\mu\text{g/m}^3, \text{m/s}, \text{gpm}, \text{hPa}, \text{Kelvin}$).
- [x] **Reproducibility Details:** Detail batch sizes, learning rates, Optuna parameter search spaces, and GPU memory configurations.
