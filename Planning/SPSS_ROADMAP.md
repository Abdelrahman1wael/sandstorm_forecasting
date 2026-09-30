# 📊 IBM SPSS Statistics: Complete Research Master Roadmap
### *From Data Hygiene & Exploratory Analysis to Advanced Psychometrics & Hayes PROCESS*

---

## 🌟 Executive Overview & Role in Empirical Research

**IBM SPSS Statistics** serves as the primary quantitative command center in environmental, public health, and socioeconomic research. While GIS extracts spatial exposure and AMOS tests structural causal equations, SPSS is responsible for:
1. **Data Hygiene & Screening:** Missing value diagnosis, univariate/multivariate outlier detection, and distribution transformations.
2. **Diagnostic Assumptions:** Normality screening, homoscedasticity, and multicollinearity checks.
3. **Parametric & Non-Parametric Hypothesis Testing:** Comparing disaster impacts across regions, demographic cohorts, and time periods.
4. **Psychometric Dimension Reduction:** Internal consistency reliability (Cronbach's $\alpha$) and Exploratory Factor Analysis (EFA) to discover latent survey constructs.
5. **Advanced Regression & Conditional Process Analysis:** Multiple linear regression, logistic hazard modeling, and the Hayes PROCESS macro (mediation and moderation).

```
+-----------------------------------------------------------------------------------+
|                        SPSS RESEARCH WORKFLOW PIPELINE                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Raw Field Surveys / Ground Sensors / Socioeconomic Census]                      |
|                                |                                                  |
|                                v                                                  |
|  [Stage 1: Data Preparation]   Variable Coding • Little's MCAR • Mahalanobis D²   |
|                                |                                                  |
|                                v                                                  |
|  [Stage 2: Assumption Checks]  Shapiro-Wilk • Skew/Kurtosis • Levene's • VIF      |
|                                |                                                  |
|                                v                                                  |
|  [Stage 3: Group Tests]        t-test • ANOVA • ANCOVA • Kruskal-Wallis           |
|                                |                                                  |
|                                v                                                  |
|  [Stage 4: Psychometrics]      Cronbach's Alpha (≥ 0.70) • EFA (KMO ≥ 0.70, PAF)  |
|                                |                                                  |
|                                v                                                  |
|  [Stage 5: Regression & PROCESS] OLS • Logistic • Hayes PROCESS Model 4 / Model 1 |
|                                |                                                  |
|                                v                                                  |
|  [Export to AMOS (.sav)]       Clean Indicator Variables Ready for CFA / SEM      |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Phase 1: Data Preparation, Hygiene & Outlier Screening

Before running any statistical test, the raw dataset must pass strict hygiene protocols.

### 1.1 Variable View Definition
* **Name & Label**: Short code names (`risk_perc_01`) with clear descriptive labels (*"I feel dust storms threaten my respiratory health"*).
* **Measurement Levels**:
  * **Scale (Continuous)**: Physical sensor records (PM10 $\mu\text{g/m}^3$, wind speed m/s), household income, age.
  * **Ordinal**: Likert scales (1 = Strongly Disagree to 5 = Strongly Agree).
  * **Nominal**: Categorical groups (Gender, Province: Gansu = 1, Ningxia = 2, Beijing = 3).
* **Missing Value Codes**: Explicitly code discrete missing values (`-99`, `-999`) to prevent numeric corruption of calculations.

### 1.2 Missing Value Analysis (MVA)
* **Missing Data Mechanisms**:
  * **MCAR (Missing Completely at Random)**: Missingness is purely stochastic.
  * **MAR (Missing at Random)**: Missingness depends on observed variables (e.g., elderly residents skip online app questions).
  * **MNAR (Missing Not at Random)**: Missingness depends on the unobserved value itself (e.g., high-income households refuse income disclosure).
* **Statistical Test**: Run **Little’s MCAR Test** (`Analyze > Missing Value Analysis`):
  * If $p > 0.05$, missingness is completely random.
* **Imputation Protocols**:
  * $< 5\%$ missing on large sample: Listwise deletion or Mean Substitution.
  * $5\% - 15\%$ missing: **Expectation-Maximization (EM)** algorithm or **Linear Trend**.
  * $> 15\%$ missing: **Multiple Imputation (MI)** generating 5 pooled imputations.

### 1.3 Univariate & Multivariate Outlier Detection
* **Univariate Outliers**:
  * Standardized $Z$-scores (`Descriptives > Save standardized values as variables`):
    $$Z = \frac{X - \mu}{\sigma}$$
    Flag cases where $|Z| > 3.29$ ($p < 0.001$).
  * Inspect Boxplots: points beyond $1.5 \times \text{IQR}$ (outliers) and $3.0 \times \text{IQR}$ (extreme outliers).
* **Multivariate Outliers**:
  * **Mahalanobis Distance ($D^2$)**: Run a dummy linear regression with case ID as dependent and all scale indicators as independents (`Save > Mahalanobis`).
  * Compute $p$-value in SPSS via Compute Variable:
    $$\text{p\_val} = 1 - \text{CDF.CHISQ}(mah\_1, df)$$
    Flag cases with $p < 0.001$.
  * Inspect **Cook’s Distance** ($> 1.0$ indicates influential distortion) and **Leverage** values.

### 1.4 Data Transformation & Index Computation
* **Reverse-Scoring Negative Items**:
  $$\text{Item}_{\text{reversed}} = (\text{Max\_Scale} + 1) - \text{Item}_{\text{original}}$$
  *(e.g., for a 5-point scale: $6 - X$)*.
* **Logarithmic / Square-Root Transformation**:
  For severely right-skewed atmospheric sensor concentrations:
  $$\text{PM10}_{\text{log}} = \ln(\text{PM10} + 1)$$

---

## 🔍 Phase 2: Exploratory Data Analysis & Diagnostic Assumptions

Statistical validity requires verifying underlying mathematical distribution assumptions.

### 2.1 Normality Screening
* **Sample Size Rules**:
  * $N < 50$: **Shapiro-Wilk Test** (`Analyze > Descriptive Statistics > Explore > Plots > Normality plots with tests`).
  * $N \ge 50$: **Kolmogorov-Smirnov Test** (with Lilliefors significance correction).
  * In large datasets ($N > 300$), significance tests often reject normality due to extreme statistical power. Therefore, rely on **Skewness and Kurtosis ratios**:
    $$\text{Ratio} = \frac{\text{Skewness}}{\text{Std. Error of Skewness}}$$
    Acceptable absolute value range: **Skewness between $-2.0$ and $+2.0$**, **Kurtosis between $-7.0$ and $+7.0$** (Kline, 2015).
* **Visual Diagnostics**:
  * Q-Q Plots (points should adhere tightly to the 45-degree diagonal).
  * Detrended Normal Q-Q plots (points should scatter randomly around 0).

### 2.2 Homogeneity of Variance (Homoscedasticity)
* **Levene’s Test of Equality of Variances**:
  * If $p > 0.05$, homogeneity assumption holds.
  * If $p < 0.05$, equal variances cannot be assumed $\rightarrow$ use **Welch’s $t$-test** or **Brown-Forsythe ANOVA**.

### 2.3 Multicollinearity Screening
* Before fitting multiple regression, collinearity diagnostics must be enabled (`Linear Regression > Statistics > Collinearity diagnostics`):
  * **Tolerance** ($1 - R_j^2$): Should be $> 0.10$ (ideally $> 0.20$).
  * **Variance Inflation Factor (VIF)**:
    $$\text{VIF} = \frac{1}{\text{Tolerance}}$$
    Threshold: $\text{VIF} < 5.0$ (strict) or $< 10.0$ (maximum acceptable). Condition Index should be $< 30$.

---

## 📈 Phase 3: Inferential Statistics & Group Differences

Testing whether environmental exposure or disaster warnings produce statistically significant differences.

### 3.1 Comparing Two Groups
* **Independent Samples $t$-Test**:
  * Compares means between two independent cohorts (e.g., Warning Received vs. No Warning).
  * Report: $t(df) = \text{value}$, $p$-value, and effect size **Cohen’s $d$**:
    $$d = \frac{\bar{X}_1 - \bar{X}_2}{s_{\text{pooled}}}$$
    *(Small: 0.2, Medium: 0.5, Large: 0.8)*.
* **Paired Samples $t$-Test**:
  * Pre-disaster vs. Post-disaster measurements on the same respondents.
* **Non-Parametric Equivalents (for non-normal / ordinal data)**:
  * Two independent groups: **Mann-Whitney $U$ Test**.
  * Two paired groups: **Wilcoxon Signed-Rank Test**.

### 3.2 Comparing Three or More Groups
* **One-Way ANOVA**:
  * Compares means across multiple regions (e.g., Desert Source vs. Hexi Corridor vs. Downstream Plain).
  * Effect size: Partial Eta Squared ($\eta_p^2$):
    $$\eta_p^2 = \frac{SS_{\text{effect}}}{SS_{\text{effect}} + SS_{\text{error}}}$$
* **Post-Hoc Pairwise Comparisons**:
  * Equal Variances Assumed: **Tukey’s HSD** (balanced samples) or **Scheffé** (conservative).
  * Unequal Variances: **Games-Howell** test.
* **ANCOVA (Analysis of Covariance)**:
  * Controls for continuous confounding covariates (e.g., household baseline income or distance to desert).
* **Non-Parametric Equivalent**:
  * **Kruskal-Wallis $H$ Test** with Dunn-Bonferroni post-hoc tests.

---

## 🧬 Phase 4: Psychometrics & Exploratory Factor Analysis (EFA)

Validating survey instruments before constructing structural equations in AMOS.

### 4.1 Internal Consistency Reliability
* **Cronbach’s Alpha ($\alpha$)** (`Analyze > Scale > Reliability Analysis`):
  $$\alpha = \frac{k}{k - 1} \left(1 - \frac{\sum \sigma_i^2}{\sigma_X^2}\right)$$
* **Evaluation Benchmarks**:
  * $\alpha \ge 0.90$: Excellent.
  * $0.80 \le \alpha < 0.90$: Good.
  * $0.70 \le \alpha < 0.80$: Acceptable for empirical research.
  * $\alpha < 0.70$: Questionable / Unacceptable.
* **Diagnostics**:
  * **Corrected Item-Total Correlation**: Must be $> 0.30$. Any item with correlation $< 0.30$ should be considered for deletion.
  * **"Cronbach’s Alpha if Item Deleted"**: If deleting an item increases $\alpha$ significantly, the item is degrading scale cohesion.

### 4.2 Exploratory Factor Analysis (EFA)
EFA identifies the underlying latent dimensions among measured survey items without imposing a prior structural model.

```
+---------------------------------------------------------------------------------+
|                               EFA EXECUTION PROTOCOL                            |
+---------------------------------------------------------------------------------+
|  1. Suitability Checks:                                                         |
|     • Kaiser-Meyer-Olkin (KMO) Measure of Sampling Adequacy:                    |
|       - KMO ≥ 0.80: Meritorious                                                 |
|       - KMO ≥ 0.70: Middling / Acceptable                                       |
|       - KMO < 0.60: Inadmissible for factor analysis                            |
|     • Bartlett's Test of Sphericity:                                            |
|       - Must be statistically significant (p < 0.001)                           |
|                                                                                 |
|  2. Factor Extraction:                                                          |
|     • Principal Axis Factoring (PAF) or Maximum Likelihood (ML)                 |
|       (Preferred over PCA when targeting latent constructs for AMOS SEM)        |
|                                                                                 |
|  3. Retention Rules:                                                            |
|     • Kaiser Criterion: Retain factors with Eigenvalues > 1.0                   |
|     • Scree Plot: Identify the "elbow" point before leveling off                |
|     • Cumulative Variance Explained: Target ≥ 50% to 60%                        |
|                                                                                 |
|  4. Factor Rotation:                                                            |
|     • Oblique (Promax / Direct Oblimin): Standard when psychological/social     |
|       constructs correlate with each other (Correlation r > 0.32).              |
|     • Orthogonal (Varimax): Only when factors are theoretically uncorrelated.   |
|                                                                                 |
|  5. Item Pruning Rules:                                                         |
|     • Factor Loading threshold: λ ≥ 0.50 on the primary factor                  |
|     • Cross-loadings: Difference between primary and secondary loading < 0.20   |
|       indicates cross-loading; prune cross-loading items.                       |
+---------------------------------------------------------------------------------+
```

---

## 🌲 Phase 5: Regression & Hayes PROCESS Macro

Modeling direct, indirect, and moderated relationships.

### 5.1 Multiple Linear Regression (OLS)
* Model specification:
  $$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_k X_k + \epsilon$$
* **Hierarchical Regression**:
  * Block 1: Demographic control variables (Age, Gender, Education, Income).
  * Block 2: Environmental exposure variables (Distance to corridor, 5-yr mean PM10).
  * Block 3: Primary psychological predictors (Risk Perception, Early Warning Trust).
  * Evaluate $\Delta R^2$ and $F$-change significance at each step.

### 5.2 Logistic Regression
* Used when the outcome is binary (e.g., Disaster Evacuation / Protective Action Taken: 1 = Yes, 0 = No):
  $$\text{logit}(P) = \ln\left(\frac{P}{1 - P}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k$$
* Report **Odds Ratios ($\text{Exp}(\beta)$)** with 95% Confidence Intervals.
* Model fit: **Hosmer-Lemeshow Goodness-of-Fit Test** ($p > 0.05$ indicates good fit), Cox & Snell $R^2$, Nagelkerke $R^2$.

### 5.3 Hayes PROCESS Macro (Mediation & Moderation)
The PROCESS macro by Andrew F. Hayes automates path analysis with non-parametric bootstrapping.

* **Model 4: Simple / Parallel Mediation**:
  * Tests whether an intermediate variable ($M$, e.g., Community Preparedness) transmits the effect of $X$ (Warning Lead Time) to $Y$ (Economic Loss Reduction).
  * Bootstrapping: 5,000 resamples, 95% Bias-Corrected Confidence Intervals.
  * Mediation is established if the **Indirect Effect CI does not include zero**.
* **Model 1: Simple Moderation**:
  * Tests whether the effect of $X$ on $Y$ changes as a function of moderator $W$ (e.g., Household Income or Government Subsidy).
  * Significant interaction term ($X \times W$, $p < 0.05$).
  * Probe interaction via **Johnson-Neyman Floodlight Analysis** to identify exact threshold values of $W$ where $X$'s effect becomes significant.
* **Model 7 / 8 / 14: Moderated Mediation**:
  * Tests conditional indirect effects (e.g., warning lead time reduces losses via preparedness, but only for communities with high infrastructure access).

---

## ⚠️ Common SPSS Traps & Best Practice Remedies

| Pitfall | Consequence | Professional Remedy |
| :--- | :--- | :--- |
| **Using PCA instead of PAF/ML for survey constructs** | Inflates variance explained and factor loadings spuriously. | Use Principal Axis Factoring (PAF) or Maximum Likelihood (ML) when preparing for AMOS CFA. |
| **Treating Likert items as continuous without normality check** | Distorts covariance matrices and inflates Type I errors. | Check skewness/kurtosis. If non-normal, use robust estimators or non-parametric tests. |
| **Ignoring Multicollinearity ($\text{VIF} > 5$)** | Unstable regression coefficients with flipped signs. | Prune redundant items or combine collinear items into a composite mean index. |
| **Applying Listwise deletion to $20\%$ missing data** | Severe sample loss and systematic attrition bias. | Run Little’s MCAR test; apply Expectation-Maximization (EM) or Multiple Imputation. |
| **Correlating items during EFA across unrelated dimensions** | Unstable factor solution with cross-loadings. | Ensure clean survey construction; eliminate ambiguous questions with low communalities ($< 0.30$). |

---

## 📚 Recommended Software & Reference Literature

* **Software**: IBM SPSS Statistics version 26.0 or higher + **Hayes PROCESS Macro v4.3+**.
* **Key Literature**:
  1. Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). *Multivariate Data Analysis* (8th Edition). Cengage Learning.
  2. Field, A. (2018). *Discovering Statistics Using IBM SPSS Statistics* (5th Edition). SAGE Publications.
  3. Hayes, A. F. (2022). *Introduction to Mediation, Moderation, and Conditional Process Analysis: A Regression-Based Approach* (3rd Edition). Guilford Press.
