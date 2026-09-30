# 📚 Chapter 2: 文献综述与理论基础 (Literature Review & Theoretical Foundations)
### *Writing Guide, Academic Synthesis & Theoretical Formulations for Master's Thesis Chapter 2*
**Standard Chapter Designation:** 第二章 文献综述与理论基础 (Chapter 2: Literature Review & Theory)  
**Standard Word Count Target:** 12,000 – 16,000 Chinese characters (~25–30 thesis pages)  
**Degree Standard:** University of Science and Technology Beijing (USTB) • Environmental Engineering

---

## 🎯 Chapter 2 Structure & Required Theoretical Pillars

Chapter 2 establishes the intellectual and mathematical credibility of the dissertation. In Chinese universities, this chapter must synthesize physical principles, numerical history, modern machine learning breakthroughs, and socioeconomic behavioral science:

```
第二章 文献综述与理论基础 (Chapter 2: Literature Review & Theory)
├── 2.1 大气动力学与沙尘起沙输送物理机理 (Atmospheric Dynamics & Dust Saltation Physics)
│   ├── 2.1.1 大气边界层湍流扩散与纳维-斯托克斯 (Navier-Stokes) 方程
│   ├── 2.1.2 颗粒物起沙物理过程：空气动力学跃移与剪切应力机理
│   └── 2.1.3 气溶胶平流-扩散-沉降连续性控制方程
├── 2.2 数值天气预报与沙尘数值模式研究进展 (NWP & Dust Numerical Modeling)
│   ├── 2.2.1 传统数值天气预报模式体系 (ECMWF IFS, CMA-GFS, WRF-Chem)
│   ├── 2.2.2 气溶胶起沙经验参数化方案 (Gillette, Shao, Kok 模型)
│   └── 2.2.3 延伸期 (3-15天) 混沌效应与李雅普诺夫预报视界 (Lyapunov Horizon)
├── 2.3 机器学习与深度时空神经网络在大气环境中的应用 (Machine Learning in Atmospheric AI)
│   ├── 2.3.1 梯度提升决策树在数值预报统计后处理中的应用
│   ├── 2.3.2 循环神经网络与时空注意力模型 (ConvLSTM, PredRNN, Earthformer)
│   └── 2.3.3 非欧氏空间图神经网络 (GNN) 在区域大气输送中的演进
├── 2.4 物理信息神经网络 (PINN) 及其在环境工程中的前沿 (PINN & Physics Constraints)
│   ├── 2.4.1 PINN 基本数学架构与损失函数正则化原理
│   └── 2.4.2 物理驱动与数据驱动融合机制的优势与瓶颈
├── 2.5 空间计量分析与公众防灾行为决策理论 (Spatial Analytics & Behavioral Science)
│   ├── 2.5.1 空间自相关性理论 (莫兰指数 Moran's I 与 LISA 聚类)
│   └── 2.5.2 保护行动决策模型 (PADM) 与结构方程模型 (SEM) 在灾害响应中的应用
└── 2.6 文献述评与本研究突破点 (Summary of Literature Gaps & Thesis Entry Points)
```

---

## 🌪️ 2.1 大气动力学与沙尘起沙输送物理机理 (Core Physics)

### 2.1.1 Boundary Layer Dynamics & Navier-Stokes Balance
Atmospheric motion is governed by the conservation of momentum in a rotating planetary frame:

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \mathbf{g} - 2\mathbf{\Omega} \times \mathbf{u} + \nu \nabla^2 \mathbf{u}$$

In the Atmospheric Boundary Layer (ABL, the lowest $1\text{--}2\text{ km}$), turbulent shear stress $\tau$ drives surface friction velocity $u_*$:
$$u_* = \sqrt{\frac{\tau_0}{\rho_{\text{air}}}} = \frac{\kappa \cdot U(z)}{\ln(z / z_0) - \psi_m(z / L_{\text{MO}})}$$
Where $\kappa = 0.40$ is the von Kármán constant, $z_0$ is surface roughness length, and $\psi_m$ is the Monin-Obukhov atmospheric stability correction function.

### 2.1.2 Aerodynamic Saltation Mechanics (Bagnold, 1941; Owen, 1964; Gillette, 1979)
Dust emission is not direct aerodynamic suspension; it is initiated by **saltation** (bouncing sand grains striking the surface and dislodging fine clay/silt particles). Saltation requires friction velocity to exceed the critical threshold $u_{*t}$:

$$u_{*t} = A \cdot \sqrt{\frac{\rho_{\text{sand}} - \rho_{\text{air}}}{\rho_{\text{air}}} g d_p} \cdot f(w_s) \cdot f(z_0)$$

Where $f(w_s)$ accounts for capillary liquid bridging in damp soil:
$$f(w_s) = \sqrt{1 + 1.21 \left(w_s - w_s'\right)^{0.68}}$$
Once $u_* > u_{*t}$, the horizontal saltation sand flux $F_{\text{salt}}$ scales with the **cube of friction velocity** (Owen, 1964):
$$F_{\text{salt}} = c_{\text{salt}} \cdot \frac{\rho_{\text{air}}}{g} \cdot u_*^3 \left(1 - \frac{u_{*t}^2}{u_*^2}\right) \cdot \mathbb{I}(u_* > u_{*t})$$

### 2.1.3 Atmospheric Aerosol Transport PDE
The conservation of airborne particulate mass concentration $C(\mathbf{x}, t)$ ($\mu\text{g/m}^3$) is governed by the advection-diffusion-deposition PDE:

$$\frac{\partial C}{\partial t} + \nabla \cdot (\mathbf{u} C) = \nabla \cdot (\mathbf{K} \nabla C) + S_{\text{emission}} - v_d C - \Lambda_{\text{scav}} P_{\text{rain}} C$$

Where $\mathbf{K}$ is the turbulent eddy diffusivity tensor, $v_d$ is dry gravitational settling velocity, and $\Lambda_{\text{scav}}$ is the wet precipitation scavenging coefficient.

---

## 💻 2.2 数值天气预报局限性与李雅普诺夫预报视界 (NWP Limits)

### The Chaotic Lyapunov Horizon ($T_{\text{Lyap}}$):
Lorenz (1963) proved that non-linear atmospheric flow exhibits sensitive dependence on initial conditions. Error growth in phase space follows:
$$\|\delta \mathbf{x}(t)\| \approx \|\delta \mathbf{x}(0)\| \cdot e^{\lambda_{\text{max}} t}$$
Where $\lambda_{\text{max}}$ is the leading Lyapunov exponent of the atmosphere. 
* For planetary baroclinic waves: $\lambda_{\text{max}}^{-1} \approx 5\text{--}7\text{ days}$.
* Beyond $T_{\text{Lyap}} \approx 72\text{ hours}$ (Day 3), deterministic NWP dust trajectories diverge from ground station truth, necessitating statistical post-processing (Line A) and deep foundation modeling (Line B).

---

## 🤖 2.3 物理信息神经网络 (PINN) 理论基础 (Raissi et al., 2019)

### The PINN Framework:
Standard deep neural networks minimize purely empirical risk:
$$\min_\theta \frac{1}{N} \sum_{i=1}^N \left(y_i - f_\theta(\mathbf{x}_i)\right)^2$$
A **Physics-Informed Neural Network (PINN)** embeds the governing physical differential operator $\mathcal{N}[u]$ into the loss function via automatic differentiation:
$$\mathcal{L}_{\text{PINN}}(\theta) = \mathcal{L}_{\text{data}}(\theta) + \lambda_{\text{phys}} \mathcal{L}_{\text{physics}}(\theta)$$
$$\mathcal{L}_{\text{physics}}(\theta) = \frac{1}{N_{\text{colloc}}} \sum_{j=1}^{N_{\text{colloc}}} \left\| \mathcal{N}\left[ \hat{u}(\mathbf{x}_j; \theta) \right] - f(\mathbf{x}_j) \right\|^2$$
*In DustML, $\mathcal{N}$ represents the mass conservation continuity equation and Owen's thresholding gate.*

---

## 📊 2.5 空间分析与公众心理行为理论 (Spatial & Behavioral Theory)

### 2.5.1 Spatial Autocorrelation (Tobler's First Law)
*"Everything is related to everything else, but near things are more related than distant things."*
* **Global Moran's $I$:** Proves whether environmental risk is geographically clustered ($I > 0$).
* **LISA (Local Indicators of Spatial Association):** Identifies High-High risk clusters (e.g., Hexi Corridor to Beijing).

### 2.5.2 Protective Action Decision Model (PADM; Lindell & Perry, 2012)
Explains how individuals process environmental hazard cues:
$$\text{Hazard Cues} \longrightarrow \text{Risk Perception} \longrightarrow \text{Institutional Trust (Moderator)} \longrightarrow \text{Protective Action Compliance}$$
*Modeled in Chapter 5 using SPSS Exploratory Factor Analysis and AMOS Structural Equation Modeling.*

---

## 📌 2.6 文献述评与本研究切入点 (The Three Critical Research Gaps)

End Chapter 2 with a formal summary of the **Three Gaps in Current Literature**:

1. **Gap 1 (NWP Topographic Bias):** Numerical models cannot resolve sub-grid orographic channeling in narrow mountain corridors $\implies$ *Resolved by Line A LightGBM/CatBoost residual learning.*
2. **Gap 2 (Unconstrained AI Hallucinations):** Existing atmospheric deep learning models violate conservation of mass $\implies$ *Resolved by Line B PINN Owen saltation loss.*
3. **Gap 3 (Disaster Science Disconnect):** Engineering forecasting and socioeconomic human response are studied in total isolation $\implies$ *Resolved by Tri-Pillar Integration (AI + GIS + SPSS/AMOS).*
