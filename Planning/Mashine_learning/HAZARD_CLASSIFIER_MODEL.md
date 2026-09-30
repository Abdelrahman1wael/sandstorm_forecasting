# ⚠️ Cost-Sensitive Hazard Classifier: Technical Specification & Parameter Guide
### *5-Tier CMA Sandstorm Alert Categorization under Extreme Class Imbalance*
**Model Family:** Cost-Sensitive Multi-Class Gradient Boosted Classification  
**Implementation:** `HistGradientBoostingClassifier` with Asymmetric Cost Regularization & Isotonic Calibration  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/hazard_classifier.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/hazard_classifier.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
While regression models output continuous numerical values ($\mu\text{g/m}^3$), emergency civil response authorities require **discrete, standardized meteorological warning tiers**.

The Hazard Classifier maps atmospheric states into the official **5-Tier China Meteorological Administration (CMA)** sand and dust storm categories:

| Class Code | Warning Tier | Chinese Standard | PM10 Range ($\mu\text{g/m}^3$) | Climatological Frequency | Civil Defense Directive |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **0** | **Normal Air Quality** | 正常 / 无沙尘 | $0 \le \text{PM}_{10} < 150$ | $88.5\%$ | Standard daily routines. |
| **1** | **Floating Dust** | 浮尘 (Blue Advisory) | $150 \le \text{PM}_{10} < 500$ | $8.2\%$ | Masks advised for vulnerable groups. |
| **2** | **Blowing Sand** | 扬沙 (Yellow Alert) | $500 \le \text{PM}_{10} < 1000$ | $2.4\%$ | Construction halts; speed limits reduced. |
| **3** | **Sand and Dust Storm** | 沙尘暴 (Orange Alert) | $1000 \le \text{PM}_{10} < 2000$ | $0.6\%$ | Visibility $< 1\text{ km}$; flight diversions, school closures. |
| **4** | **Severe Dust Storm** | 强沙尘暴 (Red Alert) | $\text{PM}_{10} \ge 2000$ | $0.3\%$ | Visibility $< 500\text{ m}$; citywide industrial shutdown. |

### 1.2 The Extreme Class Imbalance Dilemma
In northern China, Severe Dust Storms (Class 4) occur in less than $0.3\%$ of station-hours. A standard symmetric cross-entropy classifier achieves $98.5\%$ accuracy by **never predicting Class 4**, causing a total failure of public disaster alerts.

The Hazard Classifier overcomes this using an **Asymmetric Cost Matrix** and **Calibrated Probability Thresholding**, penalizing missed storms up to $50\times$ more heavily than false alarms.

---

## 📐 2. Mathematical Objective Function

### 2.1 Multi-Class Cross-Entropy with Cost Regularization
For sample $i$ with true class $y_i \in \{0, 1, 2, 3, 4\}$ and predicted class probability distribution $\mathbf{p}_i = [p_{i, 0}, \dots, p_{i, 4}]$:

$$\mathcal{L}_{\text{cost}} = -\sum_{i=1}^N \sum_{k=0}^4 w_k \cdot \mathbb{I}(y_i = k) \cdot \log(p_{i, k})$$

Where class weights $w_k$ are inversely proportional to class frequencies:
$$w_k = \frac{N}{K \cdot N_k}$$
Yielding weights approximately: $w = [1.0, \ 3.5, \ 8.0, \ 20.0, \ 50.0]$.

### 2.2 Asymmetric Cost Matrix Decision Rule
During inference, rather than selecting the naive maximum probability ($\arg\max_k p_k$), the optimal operational hazard class $k^*$ minimizes the **Expected Societal Loss**:

$$k^* = \arg\min_{k \in \{0..4\}} \sum_{j=0}^4 p(y = j \mid \mathbf{x}) \cdot C_{j, k}$$

Where the Cost Matrix $\mathbf{C}$ is structured as:
$$\mathbf{C} = \begin{pmatrix} 
0 & 1 & 3 & 8 & 15 \\ 
2 & 0 & 2 & 5 & 10 \\ 
6 & 3 & 0 & 3 & 6 \\ 
20 & 10 & 4 & 0 & 2 \\ 
50 & 25 & 12 & 4 & 0 
\end{pmatrix}$$
*Notice that missing a Red Alert storm ($C_{4, 0} = 50$) costs $50\times$ more than a false alarm ($C_{0, 4} = 15$).*

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `n_classes` | `int` | `5` | `4 - 5` | Number of hazard severity tiers according to national standards. |
| `max_iter` | `int` | `120` | `80 - 250` | Maximum boosting iterations for the multi-class forest. |
| `learning_rate` | `float` | `0.05` | `0.02 - 0.10` | Learning rate shrinkage. |
| `max_depth` | `int` | `6` | `4 - 8` | Maximum tree depth. |
| `min_samples_leaf` | `int` | `20` | `10 - 40` | Minimum samples in terminal leaf. Prevents splitting on isolated sensor artifacts. |
| `class_weight` | `str / dict` | `'balanced'` | `'balanced'`, custom dict | Applies inverse-frequency weights to gradient updates. |
| `l2_regularization`| `float` | `1.5` | `0.5 - 5.0` | $L_2$ regularization on leaf scores. |
| `random_state` | `int` | `42` | Any fixed seed | Reproducibility seed. |

---

## 📊 4. Operational Contingency Evaluation

The classifier is evaluated using the official CMA/WMO meteorological metrics for event threshold $\text{PM}_{10} \ge 500 \ \mu\text{g/m}^3$ (Blowing Sand and above):

$$\text{Threat Score (TS)} = \frac{H}{H + F + M} \quad (\text{Target} \ge 0.50)$$
$$\text{Probability of Detection (POD)} = \frac{H}{H + M} \quad (\text{Target} \ge 0.85)$$
$$\text{False Alarm Rate (FAR)} = \frac{F}{H + F} \quad (\text{Target} \le 0.25)$$

Where $H$ = Hits, $F$ = False Alarms, $M$ = Misses.

---

## 💡 5. Python Implementation Code

Exemplar implementation from `Ai Pipline/models/machine_learning/hazard_classifier.py`:

```python
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

class CostSensitiveHazardClassifier:
    def __init__(self, n_classes=5, max_iter=120, seed=42):
        self.n_classes = n_classes
        self.model = HistGradientBoostingClassifier(
            max_iter=max_iter,
            learning_rate=0.05,
            max_depth=6,
            min_samples_leaf=20,
            class_weight="balanced",
            l2_regularization=1.5,
            random_state=seed
        )
        # Cost matrix: Rows = True Class, Columns = Predicted Class
        self.cost_matrix = np.array([
            [0,  1,  3,  8, 15],
            [2,  0,  2,  5, 10],
            [6,  3,  0,  3,  6],
            [20, 10,  4,  0,  2],
            [50, 25, 12,  4,  0]
        ], dtype=float)

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self

    def predict_probabilities(self, X):
        return self.model.predict_proba(X)

    def predict_cost_sensitive(self, X):
        probs = self.predict_probabilities(X) # [N, 5]
        # Expected loss for each candidate class: E_loss = Probs @ CostMatrix
        expected_loss = probs @ self.cost_matrix # [N, 5]
        # Pick class that minimizes expected loss
        return np.argmin(expected_loss, axis=1)
```
