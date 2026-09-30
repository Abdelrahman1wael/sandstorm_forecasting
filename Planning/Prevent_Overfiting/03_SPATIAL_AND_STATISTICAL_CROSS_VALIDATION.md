# 03 空间统计与社会计量模型防过拟合规范 (Spatial & Statistical Cross-Validation)

本规范详述地理信息系统（GIS 空间插值与 GWR）以及社会学结构方程模型（SPSS / AMOS）在防过拟合、防止假性高精度以及避免“偶然性资本化（Capitalization on Chance）”方面的严格准则。

---

## 1. 空间交叉验证体系 (Spatial Cross-Validation Standards)

### 1.1 托布勒地理学第一定律对常规交叉验证的瓦解
- **学术警示**：根据地理学第一定律，“任何事物都是相关的，但相近的事物关联更紧密”。
- **虚假精度陷阱**：若将北京东四站作为测试集、北京天坛站（相距仅 8km）作为训练集，模型即使完全没有学到大气物理扩散机理，仅通过近邻复制也能取得 $R^2 > 0.95$ 的假象。这在盲审评阅中属于严重的数据泄露学术硬伤。

### 1.2 空间缓冲留一站法 (Buffered Leave-One-Station-Out, BLOO-CV)
在留出目标测试站点时，**必须以该站点为中心划定半径 $R = 150 \sim 200\text{ km}$ 的空间缓冲禁区（Buffer Zone）**。凡落在该缓冲圆内的所有邻近站点，均不得参与训练。

```
                    [ 训练站点 A ]
                          *
                 . - ~ ~ ~ - .
             . '   Buffer    ' .
           /     Radius 150km    \
          |           x           |
           \   [测试站点: 北京]   /
             . '               ' .
                 ' - _ _ _ - '
          *                           *
    [ 训练站点 B ]              [ 训练站点 C ]
```

```python
import numpy as np
from scipy.spatial.distance import cdist

def buffered_leave_one_station_out(coords_df, buffer_km=150.0):
    """
    coords_df: 包含 station_id, lat, lon 的 DataFrame
    产出严格具备空间缓冲隔离的训练/验证索引
    """
    from math import radians, cos, sin, asin, sqrt
    
    def haversine_km(lat1, lon1, lat2, lon2):
        # 矢量化两点间大圆距离计算 (km)
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        return 2 * 6371.0 * np.arcsin(np.sqrt(a))

    coords = coords_df[['lat', 'lon']].values
    n_stations = len(coords)
    
    for test_idx in range(n_stations):
        test_coord = coords[test_idx]
        distances = np.array([haversine_km(test_coord[0], test_coord[1], c[0], c[1]) for c in coords])
        
        # 剔除测试站点本身以及落在缓冲半径以内的站点
        train_indices = np.where(distances > buffer_km)[0]
        val_indices = np.array([test_idx])
        
        yield test_idx, train_indices, val_indices
```

---

## 2. GIS 克里金与 GWR 空间防过拟合参数约束 (GIS Regularization)

### 2.1 普通克里金半变异函数（Semivariogram）正则约束
- **块金基台比检验（Nugget-to-Sill Ratio）**：严格控制在 $25\% \sim 75\%$ 之间。若块金值强制设为 0，模型将陷入局部噪声的过拟合阶跃；若块金值过高，则会导致全域过平滑；
- **邻域搜索点数（Search Neighborhood）**：限定最小邻近点数 $\ge 6$、最大邻近点数 $\le 16$，避免单个极端站点统治大面积插值结果。

### 2.2 地理加权回归（GWR）自适应带宽惩罚控制
- **准则选择**：严禁人为凭借主观经验拍定带宽（Bandwidth），必须采用**修正赤池信息量准则（Corrected AIC, AICc）**自动寻优：
  $$\text{AICc} = 2n \ln(\hat{\sigma}) + n \ln(2\pi) + n \left\{ \frac{n + \text{tr}(S)}{n - 2 - \text{tr}(S)} \right\}$$
  AICc 会对局部自由度 $\text{tr}(S)$ 进行强力惩罚，有效防止算法为追逐高拟合度而选择极微小的空间带宽。

---

## 3. AMOS 结构方程模型（SEM）防过拟合与学风规范 (SEM Overfitting Controls)

在社会学问卷量表与 SEM 建模中，“过拟合（Over-fitting）”表现为通过无理论依据地滥用**修正指数（Modification Indices, MI）**、人为在残差项之间乱拉相关线来强行凑出优秀拟合指标。这属于教育部盲审的重点一票否决项。

### 3.1 自由度刚性保护与过度识别准则
- **过度识别要求**：模型自由度必须严格保持 **$df \gg 0$**（推荐 $df > 30$），确保卡方检验 $\chi^2$ 具备统计效力。若模型自由度接近 0（饱和模型），则完全失去了统计推断价值。

### 3.2 严禁“修正指数钓鱼（MI Fishing）”四不准规则
1. **不准跨潜变量关联残差**：严禁在隶属于不同潜变量的题项残差之间（如 $e_{WP1} \leftrightarrow e_{RP2}$）添加双向协方差弧线；
2. **不准为追求 CFI 凑线**：唯有题项在语义表述上具有高度重叠（如“N95口罩”与“防护面罩”同属个人装备），且经过理论严格论证后，方可谨慎在同维度题项残差间添加**不超过 2 条**协方差弧线；
3. **每次只能释放一个参数**：若确实需要释放约束，每次只能添加一条路径，并立即重新评估拟合指标与理论合理性；
4. **样本拆半交叉验证（Split-Half Cross-Validation）**：
   将 842 份样本随机拆解为**校准样本（Calibration Sample, $N_1 = 421$）**与**验证样本（Validation Sample, $N_2 = 421$）**。在 $N_1$ 上探索得到的路径结构，必须在 $N_2$ 上直接通过多群组不变性检验（Multi-Group Invariance），证明模型未在样本上产生偶然性拟合。

### 3.3 共同方法偏差（CMB）防范
执行 Harman 单因子方差分析，第一主成分未旋转解释方差必须 **$< 40\%$**（本研究为 $28.4\%$），严密排除由于同源调查填答习惯引起的系统性虚假共变。
