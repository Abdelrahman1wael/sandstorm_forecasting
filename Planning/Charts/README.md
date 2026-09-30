# 📊 硕士论文与科研系统全图表规范指南 (Master Research & System Charts Catalog)

本目录为华北沙尘暴延伸期数值订正预报与防灾减灾决策支持系统（DustML）的**全图表工程与学术绘图规范库**。涵盖发表级 SCI 期刊（300+ DPI）、中国工学硕士学位论文标准插图、以及前端 Web 可视化交互大屏（Apache ECharts / Mapbox GL）的全部图表类型。

---

## 📑 图表分类与模块索引 (Charts Directory Index)

| 规范文档 | 涵盖图表类型 | 主要应用领域与论文对应章节 | 推荐工具库 |
|:---|:---|:---|:---|
| **[`01_METEOROLOGICAL_AND_FORECAST_CHARTS.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Charts/01_METEOROLOGICAL_AND_FORECAST_CHARTS.md)** | • 分位数不确定性预报包络时序图 ($P_{10}-P_{50}-P_{90}$)<br>• 泰勒图 (Taylor Diagram)<br>• 延伸期时效衰减曲线 (Lead-time Decay: $T+1 \sim T+15$)<br>• 概率校准可靠性图与敏锐度直方图 (Reliability & Sharpness)<br>• CMA 5级灾害 ROC/PR 曲线<br>• TS / CSI 评分曲线 | 气象模式性能检验、预报不确定性评估<br>*(论文第3、4、6章)* | `matplotlib`<br>`seaborn`<br>`scikit-learn` |
| **[`02_SPATIAL_AND_REMOTE_SENSING_CHARTS.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Charts/02_SPATIAL_AND_REMOTE_SENSING_CHARTS.md)** | • 普通克里金空间插值与预测方差面 (Kriging & Variance)<br>• 局部莫兰指数聚类图 (LISA Cluster Map)<br>• 14节点动态输送通道弦图/流向矢量图<br>• 三维综合风险空间叠置图 ($Risk = H \times E \times V$)<br>• 卫星 WMO 沙尘 RGB 与分裂窗 BTD 亮温差图 | 空间暴露分析、跨境输送走廊刻画、卫星反演<br>*(论文第3、5、6章)* | `Cartopy`<br>`GeoPandas`<br>`MetPy`<br>`rasterio` |
| **[`03_XAI_AND_PHYSICAL_DIAGNOSTICS_CHARTS.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Charts/03_XAI_AND_PHYSICAL_DIAGNOSTICS_CHARTS.md)** | • Tree SHAP 全局特征重要性蜂窝蜂群图<br>• 欧文跃移临界风速局部依赖图 (SHAP Dependence)<br>• ST-GNN 时空注意力热力图 (Attention Rollout)<br>• PINN 质量守恒偏微分方程残差分布图<br>• 多任务损失函数收敛曲线 ($L_{total}, L_{data}, L_{pinn}$) | 模型物理可解释性诊断、动力学守恒检验<br>*(论文第4、6章)* | `shap`<br>`torch`<br>`matplotlib` |
| **[`04_SOCIOECONOMIC_AND_SEM_CHARTS.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Charts/04_SOCIOECONOMIC_AND_SEM_CHARTS.md)** | • AMOS 结构方程模型 (SEM) 标准化路径图<br>• 验证性因子分析 (CFA) 测量模型图<br>• Hayes PROCESS 中介效应 Bootstrap 置信区间直方图<br>• 李克特量表公众感知发散条形图 (Diverging Bar)<br>• 多群体社会脆弱性雷达图 (Radar Chart) | 社会易损性评估、公众防灾避险行为心理学机制<br>*(论文第5章)* | `IBM SPSS AMOS`<br>`matplotlib`<br>`seaborn` |
| **[`05_WEB_DASHBOARD_AND_INTERACTIVE_CHARTS.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Charts/05_WEB_DASHBOARD_AND_INTERACTIVE_CHARTS.md)** | • 实时 CMA 5级灾害动态径向仪表盘 (Radial Gauge)<br>• 双轨模型对比交互滑动时序轴 (Dual-Line Slider)<br>• 智慧城市四级应急行动甘特图 (Gantt Playbook)<br>• Mapbox GL / Leaflet 动态风场与羽流粒子流图 | 智慧城市防灾减灾大屏、前端工程落地<br>*(系统平台与论文第6章)* | `Apache ECharts`<br>`Recharts`<br>`Mapbox GL` |

---

## 🎨 统一学术出版视觉设计规范 (Academic Visual Standards)

为确保全篇硕士论文与科研论文所有插图呈现统一、专业、出版级的高级质感，必须严格遵循以下全局规范：

### 1. 颜色体系 (Color Palettes)
- **避免纯高饱和原色**：严禁直接使用纯红 (`#FF0000`)、纯绿 (`#00FF00`)、纯蓝 (`#0000FF`)。
- **中国气象局 CMA 预警等级标准配色**：
  - 无沙尘/正常：清洁绿 `#27ae60`
  - 浮尘 / 扬沙 (IV级 - 蓝色)：`#2980b9`
  - 沙尘暴 (III级 - 黄色)：`#f39c12`
  - 强沙尘暴 (II级 - 橙色)：`#e67e22`
  - 特强沙尘暴 (I级 - 红色)：`#c0392b`
- **分位数预报不确定性带**：
  - $P_{50}$ 主预测线：深深海蓝 `#1f77b4`，线宽 $2.0\text{ pt}$；
  - $P_{10} \sim P_{90}$ 80%置信包络：天蓝半透明填充 `rgba(31, 119, 180, 0.25)`。
- **发散色阶（用于残差与差值）**：采用对色盲友好的 `RdYlBu_r` 或 `coolwarm`。

### 2. 字体与字号规范 (Typography)
- **字体族**：
  - 英文与数字：优先使用 `Arial`、`Helvetica` 或 `Times New Roman`；
  - 中文标签：优先使用 `SimSun`（宋体）或 `SimHei`（黑体）；
- **字号阶梯**（以单栏宽 $8.5\text{ cm}$ 或双栏宽 $17.5\text{ cm}$ 为基准）：
  - 图表主标题（Title）：$10.5 \sim 12\text{ pt}$（加粗）
  - 坐标轴名称（Axis Label）：$9 \sim 10\text{ pt}$（加粗）
  - 坐标轴刻度数字（Tick Label）：$8 \sim 8.5\text{ pt}$
  - 图例文字（Legend Text）：$8 \sim 8.5\text{ pt}$
  - 图注/数据标签（Annotation）：$7 \sim 8\text{ pt}$

### 3. 出版分辨率与格式导出标准 (Export Formats)
- **学位论文及正文插入**：导出为矢量图 **PDF** 或 **SVG**，或无损压缩 **TIFF / PNG**（分辨率 $\ge 300\text{ DPI}$，最佳为 $600\text{ DPI}$）。
- **线宽设定**：主数据曲线 $1.5 \sim 2.0\text{ pt}$，参考基准线（如 0 值线）$0.8\text{ pt}$ 虚线，坐标轴边框 $0.8\text{ pt}$。
