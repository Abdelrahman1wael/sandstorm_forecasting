# 📐 IBM SPSS AMOS: Complete Structural Equation Modeling (SEM) Roadmap
### *From Confirmatory Factor Analysis (CFA) to Mediation, Moderation, and Multi-Group Invariance*

---

## 🌟 Executive Overview & Role in Empirical Research

**IBM SPSS AMOS (Analysis of Moment Structures)** is a visual covariance-based Structural Equation Modeling (CB-SEM) software. Unlike standard regression in SPSS which treats measured variables as perfectly reliable, AMOS provides two revolutionary capabilities:
1. **Explicit Modeling of Measurement Error**: Distinguishes true latent construct variance from random measurement noise.
2. **Simultaneous Estimation of Complex Multi-Stage Systems**: Tests multiple interrelated dependent variables, mediators, and moderators in a unified mathematical model rather than running separate stepwise regressions.

```
+-----------------------------------------------------------------------------------+
|                        AMOS STRUCTURAL MODELING LIFECYCLE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Clean Survey Data (.sav from SPSS)]                                             |
|                     |                                                             |
|                     v                                                             |
|  [Stage 1: Model Specification]       Draw Latents (Ellipses) & Items (Rectangles)|
|                                       Fix Reference Indicators (Loading = 1.0)    |
|                     |                                                             |
|                     v                                                             |
|  [Stage 2: Measurement Model (CFA)]   Standardized Loadings (λ ≥ 0.60, p < 0.001) |
|                                       Composite Reliability (CR ≥ 0.70)           |
|                                       Convergent Validity (AVE ≥ 0.50)            |
|                                       Discriminant Validity (Fornell-Larcker/HTMT)|
|                     |                                                             |
|                     v                                                             |
|  [Stage 3: Full Structural SEM]       Connect Causal Directed Paths (γ, β)        |
|                                       5,000-Resample Bias-Corrected Bootstrapping |
|                                       Direct, Indirect & Total Effects            |
|                     |                                                             |
|                     v                                                             |
|  [Stage 4: Model Fit Diagnostics]     CMIN/DF < 3.0 • CFI ≥ 0.95 • TLI ≥ 0.95     |
|                                       RMSEA < 0.06 • SRMR < 0.08                  |
|                     |                                                             |
|                     v                                                             |
|  [Stage 5: Advanced Diagnostics]      Multi-Group Invariance • Common Latent Factor|
|                     |                                                             |
|                     v                                                             |
|  [Export Latent Factor Scores]        Ready for Spatial Econometrics & GIS Mapping|
+-----------------------------------------------------------------------------------+
```

---

## 📐 Phase 1: Model Specification & Measurement Theory

### 1.1 The Fundamental Distinction: EFA vs. CFA
* **Exploratory Factor Analysis (SPSS)**: Data-driven and exploratory. Items are free to load on any extracted factor without a predefined hypothesis.
* **Confirmatory Factor Analysis (AMOS)**: Strictly theory-driven. You explicitly restrict item $X_1, X_2, X_3$ to load *only* onto Latent Construct $\xi_1$, fixing loadings on all other latent constructs to zero.

### 1.2 Graphic Interface Conventions in AMOS
| Shape / Symbol | AMOS Object Name | Statistical Meaning |
| :---: | :--- | :--- |
| **Ellipse / Circle** | Latent Variable ($\xi, \eta$) | Unobserved theoretical construct (e.g., Risk Perception, Adaptive Capacity). |
| **Rectangle** | Observed / Manifest Variable ($X, Y$) | Survey questionnaire item or physical sensor reading. |
| **Small Circle** | Measurement Error ($\delta, \epsilon$) / Disturbance ($\zeta$) | Unique variance unexplained by the latent factor or structural equations. |
| **Single-Headed Arrow** | Regression Path ($\rightarrow$) | Hypothesized directional causal influence ($X \rightarrow Y$). |
| **Double-Headed Curved Arrow** | Covariance / Correlation ($\leftrightarrow$) | Non-directional association between exogenous constructs. |

### 1.3 Model Identification Rules (The Degrees of Freedom)
A model can only be estimated if it is **over-identified** ($df > 0$):
$$df = \frac{p(p + 1)}{2} - q > 0$$
* Where $p$ is the number of observed indicator variables, $\frac{p(p+1)}{2}$ is the number of distinct sample moments in the covariance matrix, and $q$ is the number of parameters to estimate (loadings, factor variances, error variances, structural paths).
* **Scale-Setting Rule**: Every unobserved latent variable must have its metric established. By default, fix one indicator's regression weight to **$1.0$** (called the *Reference Indicator*). Alternatively, fix the latent variable's variance to $1.0$ (standardized latent variable).
* **Three-Indicator Rule**: Each latent construct should have at least **3 observed indicators** to avoid local identification issues.

---

## 🔬 Phase 2: Confirmatory Factor Analysis (CFA) & Construct Validity

Before testing structural regression paths between constructs, the **Measurement Model** must be verified independently.

### 2.1 Standardized Factor Loadings
* In AMOS `Analysis Properties > Output`, enable:
  * *Standardized estimates*
  * *Squared multiple correlations ($R^2$)*
  * *Modification indices*
* **Benchmark**: Each standardized item loading ($\lambda_i$) must be statistically significant ($p < 0.001$), ideally $\lambda \ge 0.70$ (minimum acceptable: $0.60$).
* **Item Reliability ($R^2$ / Communality)**:
  $$R_i^2 = \lambda_i^2 \ge 0.50$$
  This confirms that at least 50% of the indicator's variance is explained by the latent construct.

### 2.2 Convergent Validity
Convergent validity proves that indicators representing a theoretical construct share a high proportion of common variance.

1. **Composite Reliability (CR)**:
   $$\text{CR} = \frac{\left(\sum_{i=1}^n \lambda_i\right)^2}{\left(\sum_{i=1}^n \lambda_i\right)^2 + \sum_{i=1}^n (1 - \lambda_i^2)}$$
   * **Threshold**: $\text{CR} \ge 0.70$ (Hair et al., 2019). Superior to Cronbach’s alpha because it does not assume equal item weightings (tau-equivalence).
2. **Average Variance Extracted (AVE)**:
   $$\text{AVE} = \frac{\sum_{i=1}^n \lambda_i^2}{n}$$
   * **Threshold**: $\text{AVE} \ge 0.50$. Confirms that the latent construct explains more variance than is left in the measurement error.

### 2.3 Discriminant Validity
Discriminant validity proves that each theoretical construct is empirically unique and does not conflate with other latent constructs.

1. **Fornell-Larcker Criterion**:
   * For every pair of latent constructs, the square root of the AVE ($\sqrt{\text{AVE}}$) must be **strictly greater** than the inter-construct correlation ($r$):
     $$\sqrt{\text{AVE}_j} > |r_{jk}| \quad \forall k \ne j$$
2. **HTMT (Heterotrait-Monotrait Ratio of Correlations)**:
   * Considered the gold-standard modern criterion (Henseler et al., 2015).
   * **Threshold**: $\text{HTMT} < 0.85$ (strict) or $< 0.90$ (liberal). Any value $\ge 0.90$ indicates redundancy between constructs.

---

## 🌐 Phase 3: Full Structural Model, Path Analysis & Bootstrapping

Once the measurement model passes all validity criteria, replace covariances between latent constructs with hypothesized causal directed paths.

### 3.1 Structural Equation Estimation
* Exogenous Constructs ($\xi$): Latent independent variables (no single-headed arrows pointing to them).
* Endogenous Constructs ($\eta$): Latent dependent/mediating variables (arrows pointing to them). Every endogenous construct must have a disturbance/error term ($\zeta$).
* Report standardized path coefficients ($\beta$), unstandardized weights ($B$), standard errors ($SE$), critical ratios ($CR = B/SE \approx t$), and $p$-values.

### 3.2 Non-Parametric Bootstrapping for Indirect Effects (Mediation)
Traditional Sobel tests assume a normal distribution for the indirect effect product ($a \times b$), which is mathematically flawed because products of coefficients are skewed. AMOS utilizes **Bias-Corrected Bootstrapping**:

```
+---------------------------------------------------------------------------------+
|                        AMOS BOOTSTRAPPING SETUP PROTOCOL                        |
+---------------------------------------------------------------------------------+
|  1. Open: View > Analysis Properties > Bootstrap                                |
|  2. Check: "Perform bootstrap" -> Number of bootstrap samples: 5,000            |
|  3. Check: "Bias-corrected confidence intervals" -> Confidence level: 95%       |
|  4. In View > Analysis Properties > Output:                                     |
|     • Check "Indirect, direct & total effects"                                  |
|                                                                                 |
|  5. Decision Rule:                                                              |
|     • If the 95% Bias-Corrected Confidence Interval [Lower, Upper] does NOT     |
|       contain 0.0, the indirect effect (mediation) is statistically significant |
|       at p < 0.05.                                                              |
|                                                                                 |
|  6. Types of Mediation (Zhao, Lynch & Chen, 2010):                              |
|     • Complementary (Partial): a*b is significant, and c' is significant (same) |
|     • Competitive (Partial): a*b is significant, and c' is significant (opp.)   |
|     • Indirect-Only (Full Mediation): a*b is significant, c' is non-significant |
|     • Direct-Only (No Mediation): a*b is non-significant, c' is significant     |
|     • No Effect: Neither a*b nor c' is significant                              |
+---------------------------------------------------------------------------------+
```

---

## 📊 Phase 4: Goodness-of-Fit Benchmarks & Model Diagnostics

Evaluating how closely the model's implied covariance matrix ($\Sigma(\theta)$) matches the empirical sample covariance matrix ($S$).

### 4.1 Master Goodness-of-Fit Index Table
| Category | Fit Index | Full Name | Acceptable Range | Excellent Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Parsimonious** | **$\chi^2/df$** | Normed Chi-Square (CMIN/DF) | $< 5.0$ | $< 3.0$ (or $< 2.0$) |
| **Incremental** | **CFI** | Comparative Fit Index | $\ge 0.90$ | $\ge 0.95$ |
| | **TLI** | Tucker-Lewis Index (NNFI) | $\ge 0.90$ | $\ge 0.95$ |
| | **IFI** | Incremental Fit Index | $\ge 0.90$ | $\ge 0.95$ |
| **Absolute** | **RMSEA** | Root Mean Square Error of Approximation | $< 0.08$ | $< 0.06$ (PCLOSE $> 0.05$) |
| | **SRMR** | Standardized Root Mean Square Residual | $< 0.08$ | $< 0.05$ |
| | **GFI** | Goodness-of-Fit Index | $\ge 0.90$ | $\ge 0.95$ |

> [!IMPORTANT]
> The absolute Chi-Square test ($\chi^2$) is virtually always statistically significant ($p < 0.05$) in samples $N > 200$, leading to false model rejection. Therefore, top-tier journals prioritize **CMIN/DF, CFI, TLI, and RMSEA** as the primary golden criteria.

### 4.2 Diagnostic Strain & Model Modification
* **Standardized Residual Covariances**:
  * Reflects localized strain between pairs of indicators.
  * Inspect `View > Text Output > Residuals > Standardized Residual Covariances`.
  * Values $|Z| > 2.58$ indicate statistically significant localized misfit ($p < 0.01$).
* **Modification Indices (MI)**:
  * Estimates how much $\chi^2$ will decrease if a currently fixed parameter is freed.
  * **Golden Rule of Error Covariances**: Never correlate error terms across different latent constructs just to improve fit (this is unprincipled data dredging). You may correlate errors *within the same construct* only if items share demonstrably parallel wording or specific methodological overlap.

---

## 🏆 Phase 5: Advanced AMOS Modeling

### 5.1 Multi-Group Measurement Invariance Testing
Tests whether an instrument and structural paths operate equivalently across distinct groups (e.g., Arid Desert Basin vs. Urban Downstream Metropolis):

1. **Configural Invariance (Equal Form)**: Identical factor structure across groups without constraining parameters. Baseline fit must be acceptable.
2. **Metric / Weak Invariance (Equal Factor Loadings)**: Constrain factor loadings ($\lambda$) to be equal across groups.
   * Criterion: $\Delta\text{CFI} \le 0.010$ and $\Delta\text{RMSEA} \le 0.015$ (Cheung & Rensvold, 2002).
3. **Scalar / Strong Invariance (Equal Indicator Intercepts)**: Constrain item intercepts to be equal. Required for valid latent mean comparisons.
4. **Structural Path Invariance**: Constrain specific structural regression paths ($\beta$) to test whether a relationship (e.g., Warning Time $\rightarrow$ Evacuation) is significantly stronger in one group than another.

### 5.2 Common Method Bias (CMB)
When all variables are collected via self-report surveys at the same time:
* **Harman's Single Factor Test** (SPSS): EFA unrotated solution should have the first factor explain $< 50\%$ of total variance.
* **Common Latent Factor (CLF) in AMOS**:
  * Add a global zero-mean, unit-variance latent factor connected to all manifest indicators.
  * Constrain all CLF loadings to be equal ($a$).
  * Compare standardized item loadings with and without the CLF. If differences are $< 0.20$, Common Method Bias is not a substantial threat.

---

## ⚠️ Common AMOS Traps & Solutions

| Error / Pitfall | Root Cause | Exact Solution |
| :--- | :--- | :--- |
| **"The model is probably unidentified..."** | $df < 0$ or missing reference loading. | Ensure at least 3 indicators per latent; verify each latent has one loading fixed to $1.0$. |
| **Negative Error Variance (Heywood Case)** | Sampling error, extreme collinearity, or outlier. | Check outliers in SPSS; constrain error variance to a tiny positive constant ($0.005$) if marginally negative. |
| **Covariance Matrix is Not Positive Definite** | Perfectly correlated variables ($r > 0.95$) or linear dependency. | Remove redundant indicator; inspect correlation matrix in SPSS. |
| **Low Model Fit ($\text{CFI} < 0.85$, $\text{RMSEA} > 0.10$)** | Weak factor loadings or cross-loading items. | Prune items with $\lambda < 0.60$; inspect standardized residual covariances $> 2.58$. |

---

## 📚 Recommended Resources

* **Software**: IBM SPSS AMOS version 26.0 or higher.
* **Key Literature**:
  1. Byrne, B. M. (2016). *Structural Equation Modeling with AMOS: Basic Concepts, Applications, and Programming* (3rd Edition). Routledge.
  2. Kline, R. B. (2015). *Principles and Practice of Structural Equation Modeling* (4th Edition). Guilford Press.
  3. Hair, J. F., et al. (2019). *Multivariate Data Analysis* (8th Edition). Cengage.
