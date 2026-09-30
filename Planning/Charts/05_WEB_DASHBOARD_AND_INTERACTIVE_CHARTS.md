# 05 交互大屏与智慧决策仪表盘图表规范 (Web Dashboard & Interactive Charts)

本规范为科研原型落地与系统前端大屏（React / TypeScript / Apache ECharts / Mapbox GL）的标准交互图表工程规范。

---

## 1. 实时 CMA 5级灾害动态径向仪表盘 (Radial Hazard Gauge)

### 1.1 系统功能与交互逻辑
- **功能**：在前端监控大屏正中央，实时显示当前城市或重点站点的 CMA 综合沙尘灾害危险度评分与预测峰值浓度。
- **动态状态映射**：
  - 指针转角：对应 $0 \sim 1500\ \mu\text{g/m}^3$ 刻度区间；
  - 环形背景：分段渐变色彩（清洁绿 $\to$ 蓝色预警 $\to$ 黄色预警 $\to$ 橙色预警 $\to$ 红色预警）；
  - 联动响应：当预测分位数 $P_{90} \ge 1000$ 时，仪表盘外圈触发红色脉冲发光动效（CSS Pulse Animation）。

```
        . - ~ ~ ~ - .
    . '   \  250  /   ' .       [Pointer at 680 ug/m3]
  /  150   \     /   500  \     
 |          \   /          |    Current: 680 ug/m3
| 0          \ /      1000  |   Alert: ORANGE ALERT (II级)
 |            O            |    Trend: Rising (+18%/hr)
  \          / \          /     Confidence: 86.4%
    . '  /         \  ' .
        ' - _ _ _ - '
```

### 1.2 Apache ECharts 配置 JSON 模板
```javascript
export const hazardGaugeOption = (pm10Value, alertLevel) => ({
  series: [
    {
      type: 'gauge',
      startAngle: 210,
      endAngle: -30,
      min: 0,
      max: 1200,
      splitNumber: 6,
      itemStyle: {
        color: alertLevel === 'Red' ? '#c0392b' : alertLevel === 'Orange' ? '#e67e22' : '#f39c12',
        shadowColor: 'rgba(0,0,0,0.3)',
        shadowBlur: 10
      },
      progress: { show: true, width: 14 },
      pointer: { length: '65%', width: 5 },
      axisLine: {
        lineStyle: {
          width: 14,
          color: [
            [150 / 1200, '#27ae60'],  // 正常清洁
            [250 / 1200, '#2980b9'],  // 蓝色预警
            [500 / 1200, '#f39c12'],  // 黄色预警
            [1000 / 1200, '#e67e22'], // 橙色预警
            [1.0, '#c0392b']          // 红色预警
          ]
        }
      },
      axisTick: { distance: -18, length: 5, lineStyle: { color: '#999' } },
      splitLine: { distance: -24, length: 10, lineStyle: { color: '#666', width: 2 } },
      axisLabel: { distance: -18, color: '#666', fontSize: 10 },
      detail: {
        valueAnimation: true,
        formatter: '{value} μg/m³',
        color: 'inherit',
        fontSize: 18,
        fontWeight: 'bold',
        offsetCenter: [0, '70%']
      },
      data: [{ value: pm10Value, name: 'CMA Predicted Hazard' }]
    }
  ]
});
```

---

## 2. 双轨模型对比交互滑动时序图 (Dual-Line Interactive Timeline)

### 2.1 系统功能与交互逻辑
- **功能**：在同一个时间坐标系下，支持用户自由勾选开启或隐藏以下图层：
  - [x] Ground Observation (真实观测)
  - [x] Line A: Tree Stacking ($P_{50}$ + $80\%$ CI)
  - [x] Line B: Deep PINN+ST-GNN ($P_{50}$ + $80\%$ CI)
  - [x] ECMWF Raw IFS Baseline
- **交互特性**：
  - 底部集成时间刷选器（DataZoom Slider），支持 $1 \sim 15$ 天预测时效的平滑缩放和平移；
  - 悬停浮层（Tooltip）同时对比两个模型当前的预测绝对误差（MAE）及与预警线的超标差距。

---

## 3. 智慧城市四级应急行动甘特推演图 (Municipal Action Playbook Gantt)

### 3.1 系统功能与交互逻辑
- **功能**：根据气象大模型提前 $72-120$ 小时输出的超标概率，在时间线上直观呈现城市各大委办局的联动响应进度。
- **展示要素（各部门任务条）**：
  - **气象与生态环境局**：发布黄色预警 $\to$ 提升至橙色预警 $\to$ 启动激光雷达加密观测；
  - **城市管理与环卫委**：增开抑尘车雾炮洒水 $\to$ 主干道路湿式清扫；
  - **住房与城乡建设委**：全市土石方施工全部停工 $\to$ 易扬尘物料覆盖审查；
  - **教育委员会**：中小学停止户外活动 $\to$ 远程网课启动；
  - **交通委与交管局**：高架道路限速 $60\text{ km/h}$ $\to$ 重型柴油货车临时禁行。

```
Department           | T-72h (Forecast)  | T-48h (Prep)      | T-24h (Mobilize)  | T_0 (Plume Arrival)
---------------------+-------------------+-------------------+-------------------+--------------------
Meteo / Ecology      | [Model Alert P80] | [Issue Yellow]    | [Escalate Orange] | [Continuous Tracking]
Sanitation / Water   |                   | [Spray Prep]      | [Flush Streets ======> Flush Active]
Construction Bureau  |                   | [Notice Dispatched] [Cease Earthworks =====> All Sites Halt]
Education Bureau     |                   |                   | [Cancel Outdoor]  | [Online School Plan]
Traffic Management   |                   |                   | [Speed Limit 60]  | [Diesel Truck Ban]
```

---

## 4. Mapbox GL / Leaflet 动态风场与沙尘粒子流向图 (Dynamic Particle Wind & Dust Plume)

### 4.1 系统功能与交互逻辑
- **功能**：将 ERA5 / ECMWF 预报的水平风场（$u_{10}, v_{10}$）与 ST-GNN 预测的三维网格沙尘气溶胶浓度场在 WebGL 地理底图上渲染为**高帧率粒子动画（Particle Streamlines）**。
- **渲染机理**：
  - 粒子生成速率正比于起沙源区（如内蒙古南戈壁、巴丹吉林）的起沙通量；
  - 粒子运动速度与方向由风矢量场驱动；
  - 粒子颜色按沙尘浓度动态渐变（黄褐色 $\to$ 橙红）；
  - 粒子生命周期结束后在受体城市群沉降消散，生动展现跨省跨国沙尘输送通道的宏观流动态势。
