# 🌌 Main Line B: Complete Phases & Technical Methodology Guide
### *End-to-End Deep Spatiotemporal Foundation Model, Coupled AI-GAMFS, ST-GNN Corridors & Physics-Informed Neural Networks (PINN)*
**Discipline:** Environmental Engineering (环境工程) • Atmospheric Deep Learning  
**Platform:** DustML Operational Forecasting System (北京科技大学 • USTB)  
**Target Horizon:** Extended-Range (3–15 Days / 72h–360h) Sand and Dust Storms (SDS)

---

## 🌟 Executive Overview & Architectural Philosophy

While **Main Line A** focuses on statistical post-processing and bias-correcting numerical models (NWP), **Main Line B** represents a paradigm shift: **a fully differentiated, end-to-end multi-modal deep foundation model**. 

Purely data-driven neural networks frequently suffer from two fatal failure modes in atmospheric science:
1. **Physical Hallucinations:** Predicting sudden dust generation in calm conditions or creating mass out of vacuum, violating fundamental physical laws.
2. **Loss of Non-Euclidean Transport Dynamics:** Standard convolutional neural networks (CNNs) treat geographic space as a flat 2D grid, failing to capture high-speed advection through complex orographic corridors (such as the Hexi Corridor or the gap between the Yin and Helan Mountains).

**Main Line B** solves these fundamental bottlenecks by integrating three advanced AI pillars:
1. **Coupled AI-GAMFS Multi-Modal Backbone:** Simultaneously ingests 3D atmospheric fluid dynamics and high-resolution satellite aerosol optical depth (AOD) rasters via cross-modal gated fusion.
2. **Spatio-Temporal Graph Neural Network (ST-GNN):** Models dust plume transport as bidirectional diffusion over 14 East Asian corridor nodes, tracking both downstream advection ($P_1$) and upstream source attribution ($P_2$).
3. **Physics-Informed Neural Network (PINN) Loss Regularization:** Directly enforces Owen's aerodynamic saltation threshold ($u_* > u_{*t}$) and mass conservation continuity PDEs during gradient backpropagation.

```
+---------------------------------------------------------------------------------------------------+
|                                 MAIN LINE B: NINE-PHASE WORKFLOW                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [PHASE 1: Tensor Cubes]        Multi-Modal Inputs: NWP Tensors [B,6,16,16] + Satellites [B,3,32,32]|
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 2: AI-GAMFS Backbone]   Coupled Aerosol-Meteorology Vision Encoder & Gated Fusion Gate    |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 3: ST-GNN Corridors]    Bidirectional Graph Diffusion (14 Nodes) + Temporal Sequence GRU  |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 4: PINN Physics Core]   Owen Aerodynamic Saltation (u* > u*t) + Mass Continuity PDEs      |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 5: Multi-Scale Fusion]  Global Planetary Context + Node Local State + Graph Advection     |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 6: Monotonic Quantiles] Non-Crossing Uncertainty Heads: P10 <= P50 <= P90 (Lead Times 1..L)|
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 7: Hazard Classifier]   5-Tier CMA Classification Logits with Cost-Sensitive Extreme Loss  |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 8: Physics Scheduling]  Curriculum Learning: Data Loss Warm-Up -> PINN Regularization     |
|                                                     |                                             |
|                                                     v                                             |
|  [PHASE 9: Dual-Line Blending]  Lyapunov Horizon Blending with Line A -> FastAPI Microservice     |
+---------------------------------------------------------------------------------------------------+
```

---

## 📐 Mathematical Formulation of Line B

Line B constructs a direct nonlinear mapping from multi-modal historical and forecast state tensors to future spatial dust concentration fields and hazard alert tiers across $L$ lead steps:

$$\mathcal{F}_{\Theta}: \left\{ \mathcal{X}_{\text{NWP}} \in \mathbb{R}^{B \times C_{\text{nwp}} \times H \times W}, \ \mathcal{X}_{\text{Sat}} \in \mathbb{R}^{B \times C_{\text{sat}} \times H_s \times W_s}, \ \mathcal{X}_{\text{Seq}} \in \mathbb{R}^{B \times T \times N \times F}, \ \mathbf{A} \in \mathbb{R}^{N \times N} \right\} \longrightarrow \left\{ \hat{\mathbf{Y}}_{P10}, \hat{\mathbf{Y}}_{P50}, \hat{\mathbf{Y}}_{P90}, \hat{\mathbf{H}} \right\}$$

Subject to the **governing atmospheric advection-diffusion-settling partial differential equation (PDE)**:

$$\frac{\partial C}{\partial t} + \nabla \cdot (\mathbf{u} C) = \nabla \cdot (K \nabla C) + S_{\text{emission}} - D_{\text{dry}} - D_{\text{wet}}$$

And **Owen's aerodynamic saltation initiation threshold**:

$$S_{\text{emission}} = \begin{cases} c_{\text{salt}} \cdot \frac{\rho_{\text{air}}}{g} \cdot u_*^3 \left(1 - \frac{u_{*t}^2}{u_*^2}\right), & \text{if } u_* > u_{*t}(w_{\text{soil}}, z_0) \\ 0, & \text{if } u_* \le u_{*t} \end{cases}$$

---

## 🛠️ Phase-by-Phase Detailed Breakdown

---

### Phase 1: Multi-Modal Spatiotemporal Tensor Construction

Phase 1 transforms disparate satellite swaths, numerical grids, and point-sensor time series into synchronized PyTorch tensor batches:

```
Batch Data Tensors:
├── nwp_grid:         [B, 6, 16, 16]    -> Dynamic atmospheric fluid field
├── satellite_grid:   [B, 3, 32, 32]    -> High-resolution aerosol optical depth (AOD)
├── seq_features:     [B, 24, 14, 12]   -> 24-hour historical time-series across 14 nodes
├── node_features:    [B, 14, 12]       -> Current static/dynamic station conditions
└── adj_matrix:       [14, 14]          -> Normalized spatial transport graph topology
```

#### 1.1 Input Channel Definitions
1. **NWP Fluid Dynamic Grid ($C_{\text{nwp}} = 6$):**
   * Channel 0: $U_{10}$ (Zonal 10m wind velocity, $\text{m/s}$)
   * Channel 1: $V_{10}$ (Meridional 10m wind velocity, $\text{m/s}$)
   * Channel 2: $Z_{850}$ (850 hPa Geopotential Height, $\text{gpm}$)
   * Channel 3: $T_{2\text{m}}$ (2m Surface Temperature, $\text{K}$)
   * Channel 4: $Q_{850}$ (Specific Humidity at 850 hPa, $\text{kg/kg}$)
   * Channel 5: $\text{PBLH}$ (Planetary Boundary Layer Height, $\text{m}$)
2. **Satellite Earth Observation Grid ($C_{\text{sat}} = 3$):**
   * Channel 0: FY-4 / MODIS Aerosol Optical Depth ($550\text{ nm}$ AOD)
   * Channel 1: Dust Aerosol Index (DAI, deep blue channel absorbing ratio)
   * Channel 2: Top-of-Atmosphere (TOA) Brightness Temperature Difference ($\text{BTD}_{11\mu\text{m} - 12\mu\text{m}}$)
3. **Corridor Node Sequence Features ($T=24\text{ hours}, N=14\text{ stations}, F=12\text{ features}$):**
   * Past PM10, Friction velocity $u_*$, Threshold velocity $u_{*t}$, Relative Humidity, Soil Moisture, Pressure, Elevation, Distance to source, Wind direction sine/cosine, Hour-of-day sine/cosine.

---

### Phase 2: Coupled AI-GAMFS Multi-Modal Foundation Encoder

The foundation encoder translates raw 2D fluid and raster grids into a compact planetary representation $\mathbf{h}_{\text{global}} \in \mathbb{R}^{d_{\text{embed}}}$.

```
                 NWP Grid [B, 6, 16, 16]         Satellite Grid [B, 3, 32, 32]
                            │                                   │
                            ▼                                   ▼
                   Conv2D (k=3, s=1)                   Conv2D (k=3, s=2)
                   BatchNorm + GELU                    BatchNorm + GELU
                            │                                   │
                            ▼                                   ▼
                   Conv2D (k=3, s=2)                   Conv2D (k=3, s=2)
                   BatchNorm + GELU                    BatchNorm + GELU
                            │                                   │
                            ▼                                   ▼
                   AdaptiveAvgPool2d(1,1)              AdaptiveAvgPool2d(1,1)
                   Linear -> [B, 64]                   Linear -> [B, 64]
                            │                                   │
                            └─────────────────┬─────────────────┘
                                              ▼
                                 Concatenation [B, 128]
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
                 Sigmoid Gate (g)                        Linear Projection
                         │                                         │
                         └────────────────────┬────────────────────┘
                                              ▼
                             Gated Blending: g * h_nwp + (1-g) * h_sat
                                              │
                                              ▼
                                    LayerNorm + Residual
                                              │
                                              ▼
                                   h_global [B, HiddenDim]
```

#### 2.1 Cross-Modal Adaptive Gating
Optical satellite sensors cannot penetrate thick cloud decks or high-altitude storm clouds. Conversely, NWP dynamic fields maintain total coverage but lack fine aerosol plume resolution. The cross-modal gate $g \in (0, 1)$ dynamically balances the modalities:

$$\mathbf{g} = \sigma\left(\mathbf{W}_g [\mathbf{h}_{\text{nwp}} \, \| \, \mathbf{h}_{\text{sat}}] + \mathbf{b}_g\right)$$
$$\mathbf{h}_{\text{fused}} = \text{LayerNorm}\left(\mathbf{W}_p [\mathbf{h}_{\text{nwp}} \, \| \, \mathbf{h}_{\text{sat}}] + \mathbf{g} \odot \mathbf{h}_{\text{nwp}} + (1 - \mathbf{g}) \odot \mathbf{h}_{\text{sat}}\right)$$

*Under overcast cloud conditions, $\mathbf{g} \to 1.0$ (relying on NWP fluid dynamics). Under clear skies with visible dust plumes, $\mathbf{g} \to 0.0$ (relying on satellite imagery).*

---

### Phase 3: Spatio-Temporal Graph Neural Network (ST-GNN) Corridor Diffusion

Dust does not diffuse uniformly in all directions; it travels through narrow geographic channels constrained by topography (e.g., the Hexi Corridor bottleneck between the Qilian Mountains and Heli Mountains). Phase 3 models transport across a **14-Node East Asian Topological Graph**:

```
[Node 0: Taklamakan] ─────► [Node 2: Dunhuang] ─────► [Node 3: Zhangye (Hexi Corridor)]
                                                                  │
[Node 1: Badain Jaran] ───► [Node 4: Wuwei] ◄────────────────────┘
                                   │
                                   ▼
[Node 5: Tengger] ────────► [Node 6: Yinchuan (Ningxia Plain)]
                                   │
                                   ├─────────────────────────────┐
                                   ▼                             ▼
                        [Node 7: Hohhot (Inner Mongolia)] [Node 9: Yan'an (Loess Plateau)]
                                   │                             │
                                   ▼                             ▼
                        [Node 8: Zhangjiakou Gate]        [Node 12: Xi'an / Guanzhong]
                                   │                             │
                                   ▼                             ▼
                        [Node 10: Beijing Capital]        [Node 13: Qinling Barrier / Chengdu]
                                   │
                                   ▼
                        [Node 11: Shijiazhuang / Jinan (North China Plain)]
```

#### 3.1 Bidirectional Graph Diffusion Operator
Graph propagation uses a 3-way support decomposition:
1. **$P_0 = \mathbf{I}$ (Local Node Self-Evolution):** Station-specific accumulation and deposition.
2. **$P_1 = \mathbf{D}_{\text{out}}^{-1} \mathbf{A}$ (Forward Downstream Advection):** Wind pushing dust from upstream deserts to downstream cities.
3. **$P_2 = \mathbf{D}_{\text{in}}^{-1} \mathbf{A}^T$ (Reverse Upstream Source Tracking):** Back-tracing downwind pollution to its desert source origin.

$$\mathbf{H}^{(l+1)} = \text{LeakyReLU}\left(\sum_{k=0}^2 P_k \mathbf{H}^{(l)} \mathbf{W}_k + \mathbf{b}\right)$$

#### 3.2 Temporal Sequence Modeling via GRU
For each node $i$, the historical 24-hour sequence of graph embeddings is processed through a Gated Recurrent Unit (GRU):
$$\mathbf{h}_{t, i} = \text{GRU}\left(\mathbf{H}_{t, i}^{(2)}, \ \mathbf{h}_{t-1, i}\right)$$
Yielding the dynamic spatiotemporal corridor state: $\mathbf{H}_{\text{corridor}} \in \mathbb{R}^{B \times N \times d_{\text{hidden}}}$.

---

### Phase 4: Physics-Informed Neural Network (PINN) Loss & PDE Constraints

Phase 4 bridges deep learning with atmospheric physics. The network parameters are optimized against a multi-objective loss function that mathematically penalizes violations of physics:

$$\mathcal{L}_{\text{PINN}} = \mathcal{L}_{\text{data}} + \lambda_{\text{mass}} \mathcal{L}_{\text{mass}} + \lambda_{\text{salt}} \mathcal{L}_{\text{saltation}} + \lambda_{\text{neg}} \mathcal{L}_{\text{negativity}}$$

```
                                  Forward Predictions
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
   Data Loss (Huber)             Mass Continuity Loss            Owen Saltation Loss
   L_data = Huber(y, y_hat)       L_mass = ||ΔC - Inflow||²       L_salt = (u* <= u*t)*C²
         │                                 │                                 │
         └─────────────────────────────────┼─────────────────────────────────┘
                                           ▼
                                 Weighted Backprop:
                     Loss = L_data + 0.15*L_mass + 0.20*L_salt + 0.10*L_neg
```

#### 4.1 Aerodynamic Saltation Thresholding ($\mathcal{L}_{\text{saltation}}$)
Dust cannot be lifted from the surface unless the friction velocity $u_*$ exceeds the aerodynamic threshold $u_{*t}$, which depends on soil moisture $w_s$ and surface roughness $z_0$:
$$u_{*t} = 0.13 \cdot \sqrt{\frac{\rho_{\text{sand}} g d_p}{\rho_{\text{air}}}} \cdot \sqrt{1 + \frac{0.06}{\rho_{\text{sand}} g d_p^{2.5}}} \cdot f(w_s)$$

If the model predicts positive dust emission at a desert node while $u_* < u_{*t}$, the saltation loss fires a severe gradient penalty:

$$\mathcal{L}_{\text{saltation}} = \frac{1}{B \cdot N} \sum_{b=1}^B \sum_{i=1}^N \mathbb{I}\left(u_{*, b, i} < 0.9 \, u_{*t, b, i}\right) \cdot \left(\max\left(0, \ \hat{C}_{b, i, t=1} - C_{\text{background}}\right)\right)^2$$

#### 4.2 Spatiotemporal Mass Continuity Loss ($\mathcal{L}_{\text{mass}}$)
Mass cannot materialize spontaneously in mid-air. Downstream particulate concentration increases between forecast steps ($\Delta C = C_{t+1} - C_t$) must be physically accounted for by either **upstream graph advective inflow** or **local surface aerodynamic emissions**:

$$\text{Inflow}_{i, t} = \sum_{j=1}^N A_{j \to i} \cdot C_{j, t}$$
$$\mathcal{L}_{\text{mass}} = \frac{1}{B \cdot N \cdot (L-1)} \sum_{b, i, l} \left(\text{ReLU}\left(\left(\hat{C}_{l+1} - \hat{C}_l\right) - 1.5 \cdot \text{Inflow}_{l}\right)\right)^2$$

This guarantees that the network cannot hallucinate isolated sudden dust spikes in Beijing without an upstream plume advancing through Zhangjiakou or Inner Mongolia.

#### 4.3 Non-Negativity Enforcement ($\mathcal{L}_{\text{negativity}}$)
$$\mathcal{L}_{\text{neg}} = \frac{1}{B \cdot N \cdot L} \sum_{b, i, l} \left(\text{ReLU}\left(-\hat{C}_{b, i, l}\right)\right)^2$$

---

### Phase 5: Multi-Scale Feature Fusion

Phase 5 fuses global planetary context, local station observations, and corridor advection states into unified latent node representations:

```
[Global Context: h_global] ──(expand)──► [B, 14, 64] ──┐
                                                       │
[Current Node Features: x_node] ───────► [B, 14, 12] ──┼──► Concat [B, 14, 140]
                                                       │            │
[ST-GNN Corridor State: h_corridor] ───► [B, 14, 64] ──┘            ▼
                                                            Linear (140 -> 128)
                                                            LayerNorm + GELU + Dropout(0.15)
                                                                    │
                                                                    ▼
                                                            Linear (128 -> 64)
                                                            LayerNorm
                                                                    │
                                                                    ▼
                                                            Latent Nodes [B, 14, 64]
```

---

### Phase 6: Multi-Lead Monotonic Quantile Uncertainty Head

Standard deep regression heads predict only a single scalar $y$. Line B predicts an entire **non-parametric uncertainty distribution** for each station $i$ and lead time $l \in \{1, 2, \dots, L\}$:

$$\hat{\mathbf{Y}}_{P10}, \ \hat{\mathbf{Y}}_{P50}, \ \hat{\mathbf{Y}}_{P90} \in \mathbb{R}^{B \times N \times L}$$

#### 6.1 Guaranteed Monotonic Non-Crossing Formulation
To eliminate quantile crossing ($\hat{y}_{P10} > \hat{y}_{P50}$ or $\hat{y}_{P50} > \hat{y}_{P90}$), the network uses **softplus delta parameterization**:

$$\hat{y}_{P50} = \text{softplus}\left(\mathbf{W}_{50} \mathbf{h}_{\text{latent}} + \mathbf{b}_{50}\right)$$
$$\Delta_{10} = \text{softplus}\left(\mathbf{W}_{10} \mathbf{h}_{\text{latent}} + \mathbf{b}_{10}\right)$$
$$\Delta_{90} = \text{softplus}\left(\mathbf{W}_{90} \mathbf{h}_{\text{latent}} + \mathbf{b}_{90}\right)$$
$$\hat{y}_{P10} = \max\left(0, \ \hat{y}_{P50} - \Delta_{10}\right)$$
$$\hat{y}_{P90} = \hat{y}_{P50} + \Delta_{90}$$

Since $\Delta_{10}, \Delta_{90} > 0$ strictly for all inputs, **monotonicity is mathematically guaranteed by construction**:

$$0 \le \hat{y}_{P10} \le \hat{y}_{P50} \le \hat{y}_{P90} \quad \forall (s, t, l)$$

---

### Phase 7: Cost-Sensitive Hazard Categorization Head

Simultaneously, the latent node embeddings pass through a multi-lead classification head predicting official CMA warning tiers:

$$\mathbf{z}_{\text{hazard}} = \mathbf{W}_{\text{hazard}} \mathbf{h}_{\text{latent}} + \mathbf{b}_{\text{hazard}} \quad \longrightarrow \quad [B, N, L, 5]$$
$$p(k \mid s, l) = \frac{\exp(z_{s, l, k})}{\sum_{j=0}^4 \exp(z_{s, l, j})}$$

#### 7.1 Extreme Event Focal Loss
To prevent the overwhelming majority of clean air days (Class 0) from washing out gradients for rare severe storms (Class 4), the classification head is trained on **Class-Weighted Focal Loss**:

$$\mathcal{L}_{\text{focal}} = -\sum_{k=0}^4 \alpha_k \left(1 - p_k\right)^\gamma \log(p_k)$$

Where $\gamma = 2.0$ dynamically suppresses easy background examples, and $\alpha_4 = 10.0$ amplifies severe storm backpropagation.

---

### Phase 8: Training Optimization, Physics Scheduling & Regularization

```
Epoch 1 - 3: Warm-up Phase
├── λ_mass = 0.00, λ_salt = 0.00
└── Data loss only (learn basic data correlations)

Epoch 4 - 8: Physics Introduction
├── Linear ramp-up: λ_mass -> 0.15, λ_salt -> 0.20
└── Enforce mass continuity and saltation boundaries

Epoch 9 - 15: Fine-Tuning & Quantile Calibration
├── Full PINN regularized loss + Cosine Annealing LR
└── Gradient clipping (max_norm = 2.0) to stabilize PDE gradients
```

#### 8.1 Hyperparameter Specifications
* **Optimizer:** AdamW (Weight Decay $= 10^{-4}$)
* **Learning Rate:** $\eta_0 = 10^{-3}$, decaying to $10^{-5}$ via `CosineAnnealingLR`
* **Batch Size:** 16 (corresponding to 16 full 14-node corridor snapshots)
* **Gradient Clipping:** Max Euclidean norm $\|g\|_2 \le 2.0$ to prevent explosive PDE gradients during frontal shock transitions.

---

### Phase 9: Dual-Line Blending & Operational Inference Serving

#### 9.1 Adaptive Lead-Time Blending with Line A
Neither model is universally superior across all horizons. Main Line A excels at localized station calibrations at short lead times ($72\text{h} - 120\text{h}$), while Main Line B excels at capturing planetary Rossby wave teleconnections and corridor advection at extended horizons ($168\text{h} - 360\text{h}$).

The unified system computes an **adaptive lead-time weighted ensemble**:

$$\hat{y}_{\text{final}}(s, t+L) = w_A(L) \cdot \hat{y}_{\text{LineA}}(s, t+L) + \left(1 - w_A(L)\right) \cdot \hat{y}_{\text{LineB}}(s, t+L)$$

Where the weighting function $w_A(L)$ follows a smooth sigmoid transition:

$$w_A(L) = \frac{1}{1 + \exp\left(\frac{L - L_{\text{crossover}}}{\tau_{\text{decay}}}\right)}$$

With $L_{\text{crossover}} = 168\text{ hours}$ (Day 7) and $\tau_{\text{decay}} = 48\text{ hours}$:
* **Day 3 (72h):** $w_A = 0.88$ (Line A NWP Bias Correction dominates).
* **Day 7 (168h):** $w_A = 0.50$ (Equal 50/50 contribution).
* **Day 15 (360h):** $w_A = 0.05$ (Line B Deep Foundation PINN dominates).

```
Lead Time (Days):   Day 3         Day 5         Day 7         Day 10        Day 15
                    ├─────────────┼─────────────┼─────────────┼─────────────┤
Line A Weight:      [ 88% ]       [ 73% ]       [ 50% ]       [ 22% ]       [  5% ]
Line B Weight:      [ 12% ]       [ 27% ]       [ 50% ]       [ 78% ]       [ 95% ]
```

---

## 💻 Python Implementation Architecture

The core implementation of Main Line B resides in `Ai Pipline/models/deep_learning/`:

### 1. `aigamfs_backbone.py`
Contains `CoupledAIGAMFSEncoder`:
* CNN feature extraction over NWP dynamic grids ($6 \times 16 \times 16$) and satellite AOD rasters ($3 \times 32 \times 32$).
* Sigmoid cross-modal adaptive gating with residual projection.

### 2. `st_gnn.py`
Contains `GraphDiffusionLayer` & `SpatioTemporalGNN`:
* 3-support graph diffusion ($P_0$ self, $P_1$ forward downstream, $P_2$ reverse upstream).
* Temporal GRU sequence processing over 24-hour histories across 14 corridor nodes.

### 3. `pinn_core.py`
Contains `OwenSaltationPhysics` & `PhysicsInformedLoss`:
* Owen theoretical saltation flux calculations ($u_* > u_{*t}$).
* Mass continuity residual checking against graph advective inflow.
* Non-negativity penalty.

### 4. `unified_model.py`
Contains `DustMLUnifiedDeepModel`:
* Integrates Backbone + ST-GNN + Feature Fusion + Monotonic Quantiles + Hazard Heads.
* Guarantees $P_{10} \le P_{50} \le P_{90}$ via softplus delta parameterization.

### 5. `train_dl.py`
Master training script for Line B:
```bash
# Run training pipeline
python "Ai Pipline/training/train_dl.py"
```

---

## 📋 Comprehensive Checklist for Line B Execution

- [x] **Multi-Modal Tensor Shapes:** Validate that NWP grids, satellite AOD rasters, and node sequences align along batch dimension $B$.
- [x] **Adjacency Normalization:** Ensure graph adjacency matrix $\mathbf{A}$ has self-loops added and both out-degree and in-degree row/column normalizations are precomputed.
- [x] **Friction Velocity Thresholds:** Verify that $u_*$ and $u_{*t}$ are computed using dynamic soil moisture $\theta_{\text{soil}}$ and roughness $z_0$ at each step.
- [x] **PINN Curriculum Warm-Up:** Do not activate full $\lambda_{\text{mass}}$ and $\lambda_{\text{salt}}$ penalties during the first 3 epochs to allow initial data manifold alignment.
- [x] **Monotonicity Assertion:** Run automated unit test asserting $\min(P_{50} - P_{10}) \ge 0$ and $\min(P_{90} - P_{50}) \ge 0$ across all test batches.
- [x] **Focal Loss Weighting:** Check that extreme dust storm class logits receive adequate gradient backpropagation despite severe class imbalance.
- [x] **Smooth Blending:** Verify that dual-line blending transitions smoothly across lead times $72\text{h} \to 360\text{h}$ without step discontinuities.
