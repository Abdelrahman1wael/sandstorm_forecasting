# 01 机器学习（Line A）防过拟合与泛化提升技术规范 (Machine Learning Anti-Overfitting Standards)

本规范为主线 A（基于 GBDT 树集成的 NWP 统计订正）的防过拟合实战指南。针对时序气象数据中普遍存在的“时间自相关泄露”、“特征共线性冗余”以及“叶子节点过深记忆”等问题，制定了严格的工程约束。

---

## 1. 绝对禁止随机打乱划分：时间滚动交叉验证 (Walk-Forward Temporal CV)

### 1.1 随机划分的致命陷阱 (Data Leakage Danger)
- **学术禁忌**：在大气环境与气象预报中，严禁使用常规的随机打乱 $K$ 折交叉验证（`train_test_split(shuffle=True)`）。
- **根因**：强沙尘暴过程通常持续 $24 \sim 72$ 小时，相邻小时观测高度自相关。若将 $T$ 时刻样本划入训练集、将 $T+1$ 时刻划入验证集，模型只需“记忆”相邻时刻状态即可取得虚假的超高得分（$R^2 > 0.98$），在实际业务推理时面对全新天气过程则彻底崩溃。

### 1.2 滚动步进时间窗口划分方案 (Expanding & Sliding Window)

```
Split 1: [ Train: 2020-2022 ] -> [ Val: 2023 Spring (沙尘季) ]
Split 2: [ Train: 2020-2023 ] -> [ Val: 2024 Spring (沙尘季) ]
Split 3: [ Train: 2020-2024 ] -> [ Test: 2025 Spring (全新盲测季) ]
```

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

def walk_forward_temporal_split(df, datetime_col='datetime', n_splits=5):
    """
    按年份或严格时间序列生成时序交叉验证折，保证任何验证折都在训练折的时间之后。
    """
    df = df.sort_values(datetime_col).reset_index(drop=True)
    unique_dates = df[datetime_col].dt.date.unique()
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    for fold, (train_idx_date, val_idx_date) in enumerate(tscv.split(unique_dates)):
        train_dates = set(unique_dates[train_idx_date])
        val_dates = set(unique_dates[val_idx_date])
        
        train_indices = df[df[datetime_col].dt.date.isin(train_dates)].index.values
        val_indices = df[df[datetime_col].dt.date.isin(val_dates)].index.values
        
        yield fold, train_indices, val_indices
```

---

## 2. 树模型核心正则化超参数网格 (Tree Regularization Parameters)

通过对树深、叶子节点样本量、特征采样率与权重范数实施硬性约束，迫使决策树学习宏观气象因果规律，而非记忆微观噪声：

| 算法框架 | 防过拟合核心超参数 | 推荐安全取值区间 | 物理与算法控制机制 |
|:---|:---|:---:|:---|
| **LightGBM** | `max_depth`<br>`num_leaves`<br>`min_child_samples`<br>`colsample_bytree`<br>`subsample`<br>`reg_alpha` (L1)<br>`reg_lambda` (L2) | `4 ~ 6`<br>`15 ~ 31`<br>`30 ~ 80`<br>`0.7 ~ 0.85`<br>`0.7 ~ 0.85`<br>`0.1 ~ 2.0`<br>`1.0 ~ 10.0` | • `max_depth` 严格限制最大深度，防止生长病态细长树；<br>• `min_child_samples` 强制叶子必须包含足够观测，防止单样本叶子；<br>• `colsample_bytree` 特征子采样，防止强特征（如风速）掩盖关键次要特征；<br>• L1/L2 惩罚项压缩叶子权重。 |
| **CatBoost** | `depth`<br>`l2_leaf_reg`<br>`random_strength`<br>`subsample` | `5 ~ 7`<br>`3.0 ~ 15.0`<br>`0.5 ~ 2.0`<br>`0.75 ~ 0.85` | • `l2_leaf_reg` 强化叶子权重衰减；<br>• `random_strength` 为分裂分数添加微小随机扰动，抑制单点过度敏感；<br>• 对称树结构天然具备极强抗过拟合能力。 |
| **XGBoost** | `max_depth`<br>`min_child_weight`<br>`gamma` (min_split_loss)<br>`colsample_bytree`<br>`reg_lambda` | `4 ~ 6`<br>`5.0 ~ 20.0`<br>`0.5 ~ 3.0`<br>`0.7 ~ 0.85`<br>`2.0 ~ 10.0` | • `min_child_weight` 限制二阶导数和，避免极少样本造成分裂；<br>• `gamma` 只有当分裂带来的损失下降超过阈值时才允许分裂；<br>• `reg_lambda` 平滑叶子节点的输出方差。 |

---

## 3. 多重共线性诊断与特征剪枝 (VIF & Collinearity Pruning)

### 3.1 方差膨胀因子（VIF）检验标准
气象要素中温度、位势高度、风速及其衍生项常存在严重的共线性，导致树模型分裂选择产生随机振荡。
- **公式**：$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
- **判定阈值**：
  - $\text{VIF} < 5.0$：共线性安全（保留）；
  - $5.0 \le \text{VIF} < 10.0$：中度共线性（需评估重要性）；
  - $\text{VIF} \ge 10.0$：严重共线性（**必须剔除或执行 PCA/交互聚合**）。

### 3.2 自动相关性聚类剪枝代码
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

def prune_collinear_features(X_df, vif_threshold=5.0):
    """
    迭代剔除 VIF 最高的特征，直至所有特征 VIF 均低于设定阈值。
    """
    features = list(X_df.columns)
    while True:
        vif_data = pd.DataFrame()
        vif_data["feature"] = features
        vif_data["VIF"] = [variance_inflation_factor(X_df[features].values, i) for i in range(len(features))]
        
        max_vif = vif_data["VIF"].max()
        if max_vif > vif_threshold:
            drop_feat = vif_data.sort_values("VIF", ascending=False).iloc[0]["feature"]
            features.remove(drop_feat)
        else:
            break
    return features
```

---

## 4. Stacking 集成折外生成机制 (Out-of-Fold, OOF)

在构建 Stacking 二级元学习器（Meta-Learner，如 RidgeCV 或 HuberRegressor）时，**绝不能使用基学习器在训练集上的拟合值作为元特征输入**，否则元模型会严重过拟合基学习器的训练残差。

```
Raw Training Set:
+-------------------+-------------------+-------------------+
|      Fold 1       |      Fold 2       |      Fold 3       |
+-------------------+-------------------+-------------------+
  Train on Fold 2,3  --> Predict Fold 1 (OOF Prediction 1)
  Train on Fold 1,3  --> Predict Fold 2 (OOF Prediction 2)
  Train on Fold 1,2  --> Predict Fold 3 (OOF Prediction 3)
Concat [OOF 1, OOF 2, OOF 3] ===> Clean Input for Meta-Learner (Zero Leakage)
```

---

## 5. 早停机制与动态监控规范 (Early Stopping Protocol)

- **早停容忍步数（Patience）**：在验证集上设置 `patience = 30` 轮；
- **监控指标**：优先监控验证集 **MAE（平均绝对误差）** 或极端沙尘事件的 **加权 F1-Score**，避免以全局 MSE 为唯一早停指标（MSE 对个别极大离群值过分敏感）。
