# 03 模型可解释性与物理诊断核心图表规范 (XAI & Physical Diagnostics Charts)

本规范为硕士学位论文第4章与第6章中针对“破除AI黑箱、证明物理驱动一致性”而必须绘制的可解释性（Explainable AI, XAI）与物理动力学诊断图表标准。

---

## 1. Tree SHAP 全局特征重要性蜂群图与柱状图 (SHAP Beeswarm & Bar Plot)

### 1.1 学术目标与指标定义
- **目的**：利用博弈论 Shapley 加性解释框架（SHAP），对 Line A 树集成模型（LightGBM / CatBoost）进行全局归因，量化各个气象与下垫面特征对最终 $\text{PM}_{10}$ 预报浓度的边际贡献方向与强度。
- **视觉要素（Beeswarm 图）**：
  - 纵轴（$y$）：按平均绝对 SHAP 值降序排列的特征列表；
  - 横轴（$x$）：特征对模型输出的影响值（SHAP Value），大于 0 表示助推沙尘浓度上升，小于 0 表示压低浓度；
  - 散点颜色：表示特征本身的原始数值高低（红色为高值，蓝色为低值）；
  - **物理验证点**：10m 阵风（Gust）高值（红色）必须集中分布在 SHAP $> 0$ 右侧；表层土壤湿度（Soil Moisture）高值（红色）必须集中分布在 SHAP $< 0$ 左侧，证明模型自主学习到了正确的物理因果规律。

```
Feature                SHAP Value (Impact on PM10 Concentration)
                      <-- Decreasing Dust           Increasing Dust -->
10m Gust Wind Speed      [Low] ... (Blue) ... | ... (Red) ... [High]
Soil Moisture (0-7cm)    [High] ... (Red) ... | ... (Blue) ... [Low]
Boundary Layer Height    [High] ... (Red) ... | ... (Blue) ... [Low]
500hPa Geopotential Grad                      | ... (Red) ... [High]
NDVI Vegetation Index    [High] ... (Red) ... | ... (Blue) ... [Low]
                      ------------------------+------------------------>
                                              0
```

### 1.2 Python 发表级绘图代码
```python
import shap
import matplotlib.pyplot as plt

def plot_shap_summary(model, X_sample, feature_names, save_path="fig_shap_summary.pdf"):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    fig = plt.figure(figsize=(9, 6), dpi=300)
    shap.summary_plot(shap_values, X_sample, feature_names=feature_names, 
                      show=False, plot_size=(9, 6), alpha=0.6)
    
    plt.title("Tree SHAP Global Attribution for PM10 Predictions", fontsize=11, fontweight='bold', pad=12)
    plt.xlabel("SHAP Value (Impact on $\mathrm{PM}_{10}$, $\mu\mathrm{g}/\mathrm{m}^3$)", fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
```

---

## 2. 欧文跃移临界拐点依赖图 (SHAP Dependence & Owen Threshold)

### 2.1 学术目标与指标定义
- **目的**：通过单特征 SHAP 依赖图（Dependence Plot）或偏依赖图（Partial Dependence Plot, PDP），探寻特定物理阈值的突变拐点。
- **核心论点**：在欧文跃移起沙物理理论中（Owen, 1964），风速低于临界摩擦风速阈值 $u_{*t}$ 时地表无起沙通量；一旦风速突破阈值，输沙量按 $(u_* - u_{*t}) u_*^2$ 的非线性三次方急剧暴增。
- **图表展示**：横轴为 10m 摩擦风速 $u_*$（$\text{m/s}$），纵轴为 SHAP 贡献值。曲线在 $6.5\text{ m/s}$ 之前近乎为零平稳线，在 $\approx 6.5\text{ m/s}$ 处呈现极其陡峭的非线性向上拐折（Kink），严密证明了机器学习对经典流体力学临界跃移特性的精确捕获。

```
SHAP Value of Friction Velocity
  ^
  |                                        ./' Exponential Jump
  |                                      ./
  |                                    ./  (Owen Cubic Dust Flux)
  |                                  ./
  |       Flat / Inactive Zone     ./
0 +-------------------------------*------------------------> Friction Velocity u*
  0               4.0            6.5 (Critical Threshold)    15.0 m/s
```

---

## 3. ST-GNN 时空动态图注意力矩阵热力图 (Attention Heatmap)

### 3.1 学术目标与指标定义
- **目的**：揭示 Line B 深度图网络在沙尘暴不同演变阶段，节点与节点之间的跨区域空间自适应信息流动机制。
- **展示方式（阶段对比热力图）**：
  - **(a) 起沙爆发期（Day 0）**：注意力权重强烈集聚在节点 1（蒙古南戈壁）与节点 2（内蒙古二连浩特）的自环和源区局部边缘；
  - **(b) 跨境跨区输送期（Day +1）**：源区与通道节点（二连浩特 $\to$ 张家口 $\to$ 北京）之间的交叉注意力权重 $\alpha_{ij}$ 显著跃升至 $0.45 \sim 0.60$；
  - **(c) 沉降阻滞消亡期（Day +3）**：受体城市群（北京、天津、石家庄、太原）内部的互联边权重增加，反映山前滞留沉降特征。

```
               Source Nodes          Gateway Nodes        Receptor Nodes
            [Gobi] [Badain] [Takla] | [Eren] [Zhang] | [BJ] [TJ] [SJZ] [TY]
   [Gobi]     ■■■    ■■       □     |   ■■■    ■     |  □    □    □     □
   [Eren]     ■■■    ■        □     |   ■■     ■■■   |  ■■   ■    □     □
   [Zhang]    ■      □        □     |   ■■■    ■■    |  ■■■  ■■   ■     □
   [BJ]       □      □        □     |   ■      ■■■   |  ■■■  ■■■  ■■    ■
```

---

## 4. PINN 质量守恒偏微分方程空间残差分布图 (PINN PDE Residual Surface)

### 4.1 学术目标与指标定义
- **目的**：检验深度神经网络预测的三维时空场是否违背了连续介质力学的质量守恒定律（Mass Continuity PDE）：
  $$R(x, y, t) = \frac{\partial C}{\partial t} + u \frac{\partial C}{\partial x} + v \frac{\partial C}{\partial y} - K_h \left(\frac{\partial^2 C}{\partial x^2} + \frac{\partial^2 C}{\partial y^2}\right) - S_{emission} + D_{deposition}$$
- **图表展示**：
  - **纯数据驱动深度学习（No-PINN）**：在大风剧烈扰动边缘存在明显的非物理伪源（Phantom Source）和伪汇（Phantom Sink），残差 $R(x, y, t)$ 震荡发散（残差绝对值高达数百）；
  - **物理增强深度学习（With-PINN）**：由于损失函数强力惩罚残差项，全域残差图呈现均匀收敛至接近 0 的均匀灰度分布，有力回击了评审专家对深度学习“破坏物理规律”的质疑。

---

## 5. 多任务多目标损失函数收敛曲线 (Multi-Objective Training Curves)

### 5.1 学术目标与指标定义
- **目的**：在同一张折线图上记录 100 个 Epoch 的训练集与验证集损失函数轨迹，证明模型平稳收敛且未发生过拟合。
- **四条关键损失曲线**：
  1. 总损失函数（Total Loss: $L_{total} = \lambda_1 L_{data} + \lambda_2 L_{PINN} + \lambda_3 L_{quantile} + \lambda_4 L_{focal}$）；
  2. 经验数据拟合损失（Data MSE Loss $L_{data}$）；
  3. 物理偏微分残差损失（Physics Loss $L_{PINN}$）；
  4. 分位数单调 Pinball 损失（Quantile Pinball Loss $L_{quantile}$）。
