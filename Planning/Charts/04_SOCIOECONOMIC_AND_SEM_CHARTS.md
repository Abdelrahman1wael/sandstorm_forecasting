# 04 社会经济与结构方程模型核心图表规范 (Socioeconomic & SEM Charts)

本规范为硕士学位论文第5章关于公众风险认知、早期预警响应以及社会脆弱性实证研究的统计制图标准（基于 IBM SPSS 与 AMOS 分析产出）。

---

## 1. AMOS 结构方程模型全路径图 (SEM Standardized Path Diagram)

### 1.1 学术目标与指标定义
- **目的**：在单张规范模型图中，完整展现保护行动决策模型（PADM）中各潜变量（Latent Variables）、观测测量题项（Manifest Indicators）、残差变量（Residuals）以及因果路径系数。
- **绘图构成规范**：
  - **潜变量**：采用椭圆形表示（预警感知 Warning Perception, 风险认知 Risk Perception, 利益相关方公信力 Stakeholder Attribute, 保护行动行为 Protective Action）；
  - **观测题项**：采用矩形框表示，附带由潜变量指向题项的因子载荷量（Factor Loadings, 要求 $\lambda \ge 0.60$）；
  - **结构因果路径**：单向实线箭头，标注标准化路径系数 $\beta$ 与显著性星号（如 $\beta = 0.42^{***}, p < 0.001$）；
  - **相关外生弧**：双向弧形虚线箭头，标注相关系数 $r$；
  - **图注必须列出整体拟合指数**：$\chi^2/df = 2.14, \text{RMSEA} = 0.038, \text{CFI} = 0.962, \text{TLI} = 0.954, \text{SRMR} = 0.031$。

```
              [WP1] [WP2] [WP3]
                ^     ^     ^
                |     |     | (λ=0.81-0.85)
             ( 预警信息感知 WP )
                 /          \
  (β=0.42***)   /            \  (β=0.28***)
               v              v
      ( 沙尘风险认知 RP ) ---> ( 公众避险行为 PA )
               ^      (β=0.36***)
               |
          (β=0.24**)
               |
      ( 利益相关方属性 SA )
         /           \
     [SA1]           [SA2]
```

---

## 2. 验证性因子分析测量模型图 (CFA Measurement Model Diagram)

### 2.1 学术目标与指标定义
- **目的**：在建立结构因果模型前，证明各题项与其测量潜变量之间的收敛效度（Convergent Validity）与潜变量之间的区别效度（Discriminant Validity）。
- **图表展示**：
  - 所有潜变量之间均以双向弧线相连（表征协方差/相关关系）；
  - 报告每个题项的测量误差方差 $e_1, e_2, \dots$（严禁出现小于 0 的 Heywood 负误差异象）；
  - 表明每个题项的平均方差抽取量（AVE）均大于 $0.50$，组合信度（CR）均大于 $0.70$。

---

## 3. Hayes PROCESS 中介效应 Bootstrap 置信区间直方图 (Bootstrap Distribution)

### 3.1 学术目标与指标定义
- **目的**：利用非参数百分位 Bootstrap 算法（5000 次重抽样），证明风险认知（Risk Perception）在预警信息传达与公众防灾行动之间的间接中介效应（Indirect Effect: $a \times b$）。
- **图表构成**：
  - 中介效应抽样均值点估计线（Point Estimate，实线）；
  - 95% 置信区间下限（LLCI）与上限（ULCI，虚线）；
  - 零参考基准线（Zero Line: $x=0$）；
  - **核心判定**：若整个 95% 置信区间条带完全落在零点右侧（$LLCI > 0$），则图示直观严密地排除了中介效应为零的虚无假设。

```
Frequency
  ^                    [Bootstrap Resamples: N=5000]
  |                             .----.
  |                           /        \
  |                         /            \
  |                       /                \
  |                     /                    \
  |             LLCI  /|      Mean Point     |\  ULCI
  |             0.082  |         0.151       |   0.224
--+---------------[----+-----------|---------+----]--------> Indirect Effect (a*b)
  0 (Zero Line)
```

### 3.2 Python 发表级绘图代码
```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bootstrap_mediation_hist(boot_effects, point_est, llci, ulci, save_path="fig_bootstrap_mediation.pdf"):
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
    
    # 绘制 Bootstrap 分布核密度曲线与直方图
    sns.histplot(boot_effects, kde=True, color='#2b8cbe', stat='density', 
                 edgecolor='white', alpha=0.55, bins=40, ax=ax)
    
    # 绘制点估计与 95% 置信区间
    ax.axvline(point_est, color='#084081', linestyle='-', linewidth=2.0, label=f'Mean Indirect Effect = {point_est:.3f}')
    ax.axvline(llci, color='#e41a1c', linestyle='--', linewidth=1.4, label=f'95% LLCI = {llci:.3f}')
    ax.axvline(ulci, color='#e41a1c', linestyle='--', linewidth=1.4, label=f'95% ULCI = {ulci:.3f}')
    ax.axvline(0, color='black', linestyle=':', linewidth=1.2, label='Null Hypothesis Baseline (0.0)')
    
    # 阴影填充置信区间范围
    ax.axvspan(llci, ulci, color='#e41a1c', alpha=0.08)
    
    ax.set_title("Bootstrap Distribution of Indirect Mediation Effect ($WP \\to RP \\to PA$)", fontweight='bold', fontsize=10.5)
    ax.set_xlabel("Standardized Indirect Path Coefficient ($a \\times b$)", fontweight='bold')
    ax.set_ylabel("Sampling Density", fontweight='bold')
    ax.legend(frameon=True, facecolor='white', loc='upper right')
    ax.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
```

---

## 4. 李克特量表公众感知发散堆叠条形图 (Diverging Stacked Bar Chart)

### 4.1 学术目标与指标定义
- **目的**：清晰直观呈现 800+ 份问卷中受访者在 5 点李克特量表（李克特 1-5 分：非常不同意、不同意、中立、同意、非常同意）上的态度分布对比。
- **设计原则**：
  - 以“中立（Neutral）”为居中零点基准线；
  - 负面态度（非常不同意/不同意）向左延伸（采用浅红/红褐色配色）；
  - 正面态度（同意/非常同意）向右延伸（采用天蓝/深深蓝色配色）；
  - 中立态度在零轴两侧均匀对称分布；
  - 这种发散图表远比普通饼图或单向堆叠柱状图具备更强的学术对比冲击力。

```
                         Negative Tendency (<0)   |   Positive Tendency (>0)
                             [Disagree] [Strongly]| [Neutral] | [Agree] [Strongly Agree]
WP1: 提前3天收到预警         ===                  |   ==    | ==========================
RP1: 担忧户外扬尘呼吸疾病      =                    |   =     | ==============================
PA1: 预警发布后主动佩戴N95     ==                   |   ==    | =========================
PA2: 停止老人儿童户外活动      =                    |   =     | ==============================
```

---

## 5. 多群体社会脆弱性雷达图 (Vulnerability Radar Chart)

### 5.1 学术目标与指标定义
- **目的**：比较不同人群（按年龄、职业、受教育程度、既往基础病史分层）在多维度承灾脆弱性上的异质性表现。
- **评估维度（5个轴向）**：
  1. 户外暴露暴露时长（Outdoor Exposure Duration）；
  2. 呼吸系统易感度（Respiratory Vulnerability）；
  3. 预警信息获取阻碍度（Digital Warning Access Barrier）；
  4. 防护物资经济承受力（Protective Resource Affordability）；
  5. 应急响应行动意愿（Evacuation & Stay-at-home Compliance）。
