# 📋 Survey Data Hygiene & Psychometric Screening (SPSS & AMOS Preparation)
### *Unengaged Respondent Detection, Straight-Lining, Reverse Coding & Speeder Elimination*
**Theoretical Foundation:** Psychometric Survey Methodology (Curran, 2016; Meade & Craig, 2012)  
**Target Modalities:** Public Risk Perception Questionnaires, Willingness-to-Pay (WTP) Censuses, Household Surveys  
**Output Target:** Verified, Clean `.sav` Dataset Ready for EFA in SPSS and CFA/SEM in AMOS

---

## 🎯 1. Operational Goal & Survey Vulnerabilities

In socio-ecological disaster research, structural equation models (SEM) are only as valid as the empirical survey responses feeding them.

Unmonitored online and field surveys inevitably suffer from **Careless / Insufficient Effort Responding (C/IER)**:
1. **Straight-Lining (Zero-Variance Responding):** An unengaged respondent clicks `"3, 3, 3, 3, 3"` or `"5, 5, 5, 5, 5"` across an entire battery of 35 Likert scale questions to quickly claim a survey reward.
2. **Speeders:** Participants who finish a 15-minute survey in under 2 minutes, clicking randomly without reading the item prompts.
3. **Un-Recoded Reverse Items:** Survey batteries include reverse-worded questions (e.g., *"I feel dust storm alerts are completely useless"*). Failing to reverse-code these items generates negative factor loadings, catastrophic Cronbach's $\alpha < 0.30$, and failure of CFA model convergence in AMOS.

This module provides the automated screening filters to purge careless respondents prior to statistical factor analysis.

---

## 📐 2. Mathematical Detection Rules & Hygiene Protocols

```
+---------------------------------------------------------------------------------------------------+
|                        5-STAGE SURVEY DECONTAMINATION PIPELINE                                    |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [STAGE 1: Attention Check Verification]       Trap items: "Select 'Strongly Agree' to continue"  |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [STAGE 2: Speeder Duration Screening]         Completion Time < 30% of Sample Median -> Purged   |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [STAGE 3: Straight-Lining Variance Filter]    Within-case variance: Var_items < 0.20 -> Purged   |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [STAGE 4: Reverse Item Recoding]              Recode: X_new = (Scale_Max + 1) - X_old           |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [STAGE 5: Multivariate Outlier Screen]        Mahalanobis D² across latent indicators (p < .001) |
+---------------------------------------------------------------------------------------------------+
```

---

### 2.1 Attention Check (Trap Question) Audit
Questionnaires must embed at least two explicit instruction-verification items:
* *"To demonstrate you are reading carefully, please choose 'Disagree' for this statement."*
* Failure rule: Any respondent who fails either trap question is immediately discarded from the sample pool.

---

### 2.2 Speeder Duration Filtering (The $30\%$ Page Rule)
Reading and answering a standard psychological questionnaire requires a physiological minimum cognitive processing time (approximately $1.5\text{ seconds}$ per item). 

A submission is flagged as a speeder and excluded if:
$$T_{\text{completion}} < 0.30 \times \text{Median}\left(T_{\text{all\_respondents}}\right)$$
*Example: If the median completion time is 12 minutes ($720\text{s}$), any submission finished in under $3.6\text{ minutes}$ ($216\text{s}$) is deleted.*

---

### 2.3 Straight-Lining: Within-Person Variance & Longstring Index
1. **Within-Person Variance ($\text{Var}_{\text{person}}$):**  
   Calculates the sample variance across the 5-point Likert battery for respondent $i$:
   $$\text{Var}_{\text{person}}(i) = \frac{1}{K - 1} \sum_{k=1}^K \left(x_{ik} - \bar{x}_i\right)^2$$
   $$\text{Is Straight-Liner}: \quad \text{Var}_{\text{person}}(i) < 0.20$$
2. **Longstring Index:**  
   The maximum number of consecutive identical answers given by respondent $i$. If a respondent answers the same option for $\ge 12$ consecutive items in a 15-item battery, they are flagged as unengaged.

---

### 2.4 Reverse-Coded Item Transformation
For a 5-point Likert scale ($1 = \text{Strongly Disagree}, \ 5 = \text{Strongly Agree}$):

$$\text{Item}_{\text{recoded}} = (5 + 1) - \text{Item}_{\text{original}} = 6 - \text{Item}_{\text{original}}$$

*Transformation Map: $1 \to 5, \ 2 \to 4, \ 3 \to 3, \ 4 \to 2, \ 5 \to 1$.*

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Description / Standard |
| :--- | :---: | :---: | :---: | :--- |
| `speeder_ratio_cutoff`| `float` | `0.30` | `0.25 - 0.40` | Fraction of median duration below which a survey is discarded. |
| `min_within_person_var`|`float`| `0.20` | `0.15 - 0.25` | Minimum within-case Likert variance separating straight-liners from genuine respondents. |
| `max_longstring_ratio`| `float` | `0.75` | `0.65 - 0.80` | Maximum fraction of consecutive identical answers allowed in a subscale. |
| `likert_scale_max` | `int` | `5` | `5` or `7` | Maximum value of the Likert rating scale for reverse re-coding. |

---

## 💻 4. SPSS Syntax & Python Automated Cleaning Script

### SPSS Syntax (`.sps`):
```sps
* --- 1. REVERSE CODE NEGATIVELY PHRASED ITEMS ---.
RECODE risk_avoid_03 trust_gov_04 (1=5) (2=4) (3=3) (4=2) (5=1) INTO risk_avoid_03_rev trust_gov_04_rev.
VARIABLE LABELS risk_avoid_03_rev 'Reverse Coded: Dust storm alerts are not useful'.
EXECUTE.

* --- 2. CALCULATE WITHIN-PERSON VARIANCE ---.
COMPUTE Person_Var = VARIANCE(q1 TO q35).
EXECUTE.

* --- 3. FILTER OUT STRAIGHT-LINERS ---.
FILTER OFF.
USE ALL.
SELECT IF (Person_Var >= 0.20 AND Duration_Seconds >= 240).
EXECUTE.
```

### Python Preprocessing Implementation:
```python
import numpy as np
import pandas as pd

def clean_survey_data(
    df: pd.DataFrame, 
    likert_cols: list, 
    duration_col: str, 
    reverse_cols: list = None
) -> pd.DataFrame:
    """
    Purges speeders, straight-liners, and recodes reverse-phrased survey items.
    """
    df_clean = df.copy()

    # 1. Speeder filter: Drop responses finished in < 30% of median time
    median_time = df_clean[duration_col].median()
    time_cutoff = 0.30 * median_time
    df_clean = df_clean[df_clean[duration_col] >= time_cutoff]

    # 2. Straight-lining filter: Check within-person variance across Likert items
    within_person_var = df_clean[likert_cols].var(axis=1)
    df_clean = df_clean[within_person_var >= 0.20]

    # 3. Reverse-code specified negative polarity items (5-point scale)
    if reverse_cols:
        for col in reverse_cols:
            if col in df_clean.columns:
                df_clean[col] = 6 - df_clean[col]

    return df_clean
```
