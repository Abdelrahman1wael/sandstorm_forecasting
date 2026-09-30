# 01 气象与预报验证核心图表规范 (Meteorological & Forecast Verification Charts)

本规范详述硕士学位论文第3、4、6章中用于证明模型预测精度、时效衰减以及概率不确定性评估的全部核心气象验证图表。

---

## 1. 分位数不确定性预报包络时序图 (Quantile Uncertainty Envelope Plot)

### 1.1 学术目标与指标定义
- **目的**：展示模型在极端沙尘爆发全过程（如2021年3.15特大沙尘暴）中的逐日逐时拟合能力，同时展示 $P_{10} \sim P_{90}$ 的 80% 预测置信区间（Prediction Interval Coverage Probability, PICP）。
- **核心要素**：
  - 真实观测值（地面 MEE 监测站 $\text{PM}_{10}$ 浓度，黑色散点或实线）；
  - 数值预报基准（ECMWF IFS / WRF-Chem 模拟值，灰色点划线）；
  - Line A / Line B 预报中位数（$P_{50}$，深蓝色实线）；
  - 80% 不确定性包络（$P_{10} \sim P_{90}$，浅蓝半透明着色带）；
  - CMA 国家预警阈值水平虚线（蓝色预警 $150\ \mu\text{g/m}^3$、黄色 $250\ \mu\text{g/m}^3$、橙色 $500\ \mu\text{g/m}^3$、红色 $1000\ \mu\text{g/m}^3$）。

```
PM10 (ug/m3)
 ^
 |             [P90 Upper Envelope]
5000|                   .---.
 |                  /     \      * Actual Observed Peak
 |                 /   *   \    /
2500|       .-----.  /  / \   \  /
 |      /       \/  /   \   \/   [P50 Median Forecast]
1000|--/---.-----\-/-----\---/---\----------------- Red Warning (1000 ug/m3)
 500|-/--/---\----X-------\-/-----\---------------- Orange Warning (500 ug/m3)
 150|/--/-----\--/-\-------X-------\--------------- Blue Warning (150 ug/m3)
 0  +---------------------------------------------> Time (Days / Hours)
    T-2    T-1     T_0    T+1    T+2   ... T+10
```

### 1.2 Python 发表级绘图代码
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# 设置学术字体与样式
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

def plot_quantile_envelope(time_index, obs, p10, p50, p90, baseline=None, save_path="fig_quantile_ts.pdf"):
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    
    # 1. 绘制 CMA 预警等级参考线
    ax.axhline(150, color='#2980b9', linestyle='--', linewidth=0.9, alpha=0.7, label='Blue Alert (150)')
    ax.axhline(500, color='#e67e22', linestyle='--', linewidth=0.9, alpha=0.7, label='Orange Alert (500)')
    ax.axhline(1000, color='#c0392b', linestyle='--', linewidth=0.9, alpha=0.7, label='Red Alert (1000)')
    
    # 2. 绘制 80% 不确定性包络带 (P10 - P90)
    ax.fill_between(time_index, p10, p90, color='#1f77b4', alpha=0.22, label='80% Uncertainty Band ($P_{10}-P_{90}$)')
    
    # 3. 绘制 ECMWF / WRF 基线
    if baseline is not None:
        ax.plot(time_index, baseline, color='#7f8c8d', linestyle='-.', linewidth=1.4, label='ECMWF Raw NWP')
        
    # 4. 绘制模型预测中位数 (P50) 与真实观测 (Obs)
    ax.plot(time_index, p50, color='#084081', linewidth=2.0, label='AI-GAMFS Forecast ($P_{50}$)')
    ax.scatter(time_index, obs, color='#111111', s=16, alpha=0.85, zorder=5, label='In-situ Observation')
    
    # 坐标轴与排版
    ax.set_ylabel(r'Surface $\mathrm{PM}_{10}$ Concentration ($\mu\mathrm{g}/\mathrm{m}^3$)', fontweight='bold')
    ax.set_xlabel('Forecast Valid Time (UTC)', fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:00'))
    ax.grid(True, linestyle=':', alpha=0.45)
    ax.set_ylim(0, max(np.max(obs), np.max(p90)) * 1.15)
    
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, edgecolor='none', ncol=2)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
```

---

## 2. 多模型综合性能泰勒图 (Taylor Diagram)

### 2.1 学术目标与指标定义
- **目的**：在单张二维极坐标图上，同时呈现观测值与多个模型（ARIMA, MLP, LightGBM, CatBoost, ST-GNN, PINN-Blend）之间的三大几何统计关系：
  1. 相关系数（Pearson Correlation Coefficient, $r$，沿极角分布）；
  2. 标准差比率（Standard Deviation Normalized, $\sigma_f / \sigma_o$，沿径向距离）；
  3. 中心化均方根误差（Centered RMS Difference, $E'$，以观测点为圆心的同心圆弧）。
- **判定准则**：在泰勒图上离观测基准点（REF: $r=1.0, \sigma/\sigma_0=1.0$）欧式距离越近的模型，其综合预报技能越高。

```
              Correlation (r)
            0.1  0.3  0.5  0.7  0.9  0.95  0.99
         +----------------------------------+ 1.0 (REF)
         |                                /   * Proposed PINN (r=0.92)
         |                             /     
         |                          /       o Stacking (r=0.82)
Standard |                       /
Deviation|                    /            x LightGBM (r=0.74)
  Ratio  |                 /
         |              /                 + Raw ECMWF (r=0.51)
         |           /
         +------------------------------------+
         0.0                                1.5
```

### 2.2 Python 发表级绘图代码
```python
import numpy as np
import matplotlib.pyplot as plt

def plot_taylor_diagram(models_data, ref_std=1.0, save_path="fig_taylor_diagram.pdf"):
    """
    models_data: dict, e.g.
    {
      'Raw NWP': {'corr': 0.52, 'std': 1.45, 'color': '#7f8c8d', 'marker': '^'},
      'LightGBM': {'corr': 0.76, 'std': 1.15, 'color': '#2ca02c', 'marker': 's'},
      'ST-GNN': {'corr': 0.86, 'std': 1.08, 'color': '#ff7f0e', 'marker': 'D'},
      'PINN-Blend': {'corr': 0.93, 'std': 1.02, 'color': '#d62728', 'marker': 'o'}
    }
    """
    fig = plt.figure(figsize=(6.5, 6), dpi=300)
    ax = fig.add_subplot(111, polar=True)
    
    # 设置极角范围为 0 到 pi/2 (相关系数 0 到 1)
    ax.set_thetamin(0)
    ax.set_thetamax(90)
    
    corr_ticks = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99]
    ax.set_thetagrids(np.arccos(corr_ticks) * 180 / np.pi, labels=corr_ticks)
    
    # 绘制参考圆弧
    ax.set_rlabel_position(0)
    ax.plot(np.linspace(0, np.pi/2, 100), [ref_std]*100, 'k--', linewidth=1.2, label='Reference')
    ax.plot(0, ref_std, 'k*', markersize=12, label='Observation')
    
    # 绘制模型散点
    for name, m in models_data.items():
        theta = np.arccos(m['corr'])
        r = m['std']
        ax.plot(theta, r, marker=m['marker'], color=m['color'], markersize=8, markeredgecolor='black', label=name)
        
    ax.set_title("Model Skill Taylor Diagram (T+7 Days)", pad=20, fontweight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.05), frameon=True)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
```

---

## 3. 延伸期时效性能衰减曲线 (Lead-Time Degradation Curves)

### 3.1 学术目标与指标定义
- **目的**：检验预报时效从短期（$T+1$ 天）外推至延伸期（$T+15$ 天）过程中，RMSE、MAE 与 $R^2$ 的衰减速率。
- **验证重点**：
  - 传统纯统计模型在 $T+4$ 天后由于累积误差发散，性能发生断崖式下跌；
  - 引入了物理质量守恒与图时空依赖的 PINN+ST-GNN 能够显著平抑衰减斜率，将有效预报期由 3 天大幅拓宽至 8–10 天。

### 3.2 Python 发表级绘图代码
```python
import matplotlib.pyplot as plt
import numpy as np

def plot_lead_time_decay(lead_days, rmse_dict, r2_dict, save_path="fig_lead_time_decay.pdf"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)
    
    styles = {
        'ECMWF IFS': {'color': '#7f8c8d', 'ls': '--', 'm': 'x'},
        'Line A (Stacking)': {'color': '#2b8cbe', 'ls': '-.', 'm': 's'},
        'Line B (PINN+ST-GNN)': {'color': '#e41a1c', 'ls': '-', 'm': 'o'}
    }
    
    # 绘制左图: RMSE 随时效递增
    for name, vals in rmse_dict.items():
        ax1.plot(lead_days, vals, label=name, color=styles[name]['color'], 
                 linestyle=styles[name]['ls'], marker=styles[name]['m'], linewidth=1.8, markersize=5)
    ax1.set_xlabel('Forecast Lead Time (Days)', fontweight='bold')
    ax1.set_ylabel(r'RMSE ($\mu\mathrm{g}/\mathrm{m}^3$)', fontweight='bold')
    ax1.set_title('(a) Continuous Error Growth', fontweight='bold', loc='left')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.set_xticks(lead_days)
    ax1.legend(frameon=True)
    
    # 绘制右图: R² 决定系数衰减
    for name, vals in r2_dict.items():
        ax2.plot(lead_days, vals, label=name, color=styles[name]['color'], 
                 linestyle=styles[name]['ls'], marker=styles[name]['m'], linewidth=1.8, markersize=5)
    ax2.axhline(0.5, color='gray', linestyle=':', alpha=0.7, label='Useful Skill Threshold ($R^2=0.5$)')
    ax2.set_xlabel('Forecast Lead Time (Days)', fontweight='bold')
    ax2.set_ylabel(r'Coefficient of Determination ($R^2$)', fontweight='bold')
    ax2.set_title('(b) Predictability Horizon Skill', fontweight='bold', loc='left')
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.set_xticks(lead_days)
    ax2.set_ylim(0.2, 1.0)
    ax2.legend(frameon=True)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
```

---

## 4. 概率校准可靠性图与敏锐度直方图 (Reliability Diagram & Sharpness)

### 4.1 学术目标与指标定义
- **目的**：评估模型输出的“概率预报是否可信”（例如：模型预测有 70% 概率发生重度沙尘暴时，历史上是否真有约 70% 的批次发生了重度沙尘暴）。
- **组成结构**：
  - **主图（Reliability Curve）**：预报概率（$x$轴，分 10 个区间）对比实际观测频率（$y$轴）。完美校准线为 $45^\circ$ 对角线；
  - **子图（Sharpness Histogram）**：展示预测概率本身的分布。优质模型应具备敏锐度（Sharpness），即概率值倾向于集中在接近 0 或 1 的两端，而非模棱两可地聚集在 0.5。

```
Observed Frequency
  1.0 |                ./' Perfect Calibration (45 deg)
      |              ./
      |            ./  o Proposed Model (Well-Calibrated)
      |          ./'  
  0.5 |        ./    x Uncalibrated Baseline (Over-confident)
      |      ./
      |    ./
  0.0 +---'-------------------> Forecast Probability
      0.0        0.5       1.0
  [Sharpness Histogram: Number of forecasts in each bin below]
```

---

## 5. CMA 五级灾害等级 ROC 与 PR 曲线 (Multi-Class ROC & PR Curves)

### 5.1 学术目标与指标定义
- **问题背景**：严重沙尘暴样本（$\text{PM}_{10} > 1000\ \mu\text{g/m}^3$）出现频次极低（类极不平衡）。此时单纯看整体准确率（Accuracy）存在严重虚假繁荣。
- **必备评估图**：
  1. **受试者工作特征曲线（ROC）**：真阳性率（TPR）对比假阳性率（FPR），计算每类各自的 AUC 以及微平均（Micro-average AUC）和宏平均（Macro-average AUC）；
  2. **精确率-召回率曲线（Precision-Recall, PR）**：在极长尾灾害等级下，PR 曲线能更加敏感地暴露模型虚警率（FAR）与漏报率。要求严重沙尘暴类的 PR-AUC 达到 $0.75$ 以上。
