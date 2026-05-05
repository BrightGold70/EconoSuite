# EconoSuite R Reference Manual

This manual provides an overview of the essential R packages downloaded and configured for the **EconoSuite** project. These packages are specifically curated for data science, econometric modeling, and formatting statistical results for Economic journal manuscripts.

## 1. Installation

To set up your Mac environment, run the provided script in your R console or RStudio:
```R
source("install_econ_packages.R")
```

---

## 2. Package Categories & Purposes

### A. Core Econometrics & Inference
*   **`plm`**: The standard package for **Panel Data**. Use it to estimate Fixed Effects (FE), Random Effects (RE), and First Difference (FD) models.
*   **`fixest`**: A modern powerhouse for econometrics. It estimates regressions with multiple fixed effects extremely fast. It also natively handles robust/clustered standard errors.
*   **`AER`**: Contains tools for **Instrumental Variables (IV)** regression (`ivreg`), which is essential for addressing endogeneity.
*   **`sandwich` & `lmtest`**: Used together to compute and apply robust standard errors (Heteroskedasticity-consistent (HC) and cluster-robust errors) to standard OLS models (`lm`).
*   **`marginaleffects`**: The modern standard for computing marginal effects, adjusted predictions, and contrasts for almost any model (especially crucial for non-linear models like Logit/Probit).
*   **`quantreg`**: Essential for estimating Quantile Regressions (estimating the median or other quantiles rather than the conditional mean).
*   **`mlogit`**: The primary package for estimating Multinomial Logit models (discrete choice modeling).
*   **`sampleSelection`**: Provides tools for estimating Heckman selection models to correct for non-random sample selection bias.
*   **`gmm`**: A complete framework for Generalized Method of Moments (GMM) estimation.
*   **`np`**: The primary package for Nonparametric econometrics. Essential for flexible distributions, kernel regression, and nearest-neighbor weights without relying on rigid functional forms.

### B. Time Series Analysis
*   **`urca`**: Essential for testing stationarity (e.g., Augmented Dickey-Fuller, KPSS) and cointegration (e.g., Johansen test).
*   **`vars`**: For estimating and forecasting Vector Autoregression (VAR) and Vector Error Correction (VECM) models.
*   **`forecast`**: Provides automated time-series forecasting (e.g., `auto.arima`).

### C. Causal Inference & Difference-in-Differences
*   **`MatchIt`**: Used for propensity score matching to reduce selection bias in observational data.
*   **`rdrobust`**: The standard toolkit for Regression Discontinuity (RD) designs.
*   **`Synth`**: Used for Synthetic Control Methods, popular for state-level policy evaluation.
*   **`did`**: The industry standard package for modern **staggered Difference-in-Differences** models, implementing the Callaway and Sant'Anna (2021) estimator.
*   **`bacondecomp`**: Used to perform the Goodman-Bacon decomposition to diagnose bias in traditional Two-Way Fixed Effects (TWFE) DiD models.

### D. Machine Learning & Explainable AI (XAI)
*   **`glmnet`**: The standard package for Lasso and Elastic-Net regularized regression, often used for selecting controls in high-dimensional datasets.
*   **`grf`**: Generalized Random Forests. Used for estimating heterogeneous treatment effects using causal forests.
*   **`xgboost`**: The absolute workhorse for gradient boosting prediction models. Often outperforms standard linear models for forecasting.
*   **`shapviz`**: Critical for Explainable AI (XAI). Provides visual and analytical tools to compute **SHAP values**, explaining exactly how your ML models (like XGBoost) make their predictions.
*   **`estimatr`**: Provides extremely fast estimators for design-based inference, including robust standard errors (`lm_robust`) and linear-in-means models.
*   **`MCMCpack`**: Contains frameworks for Markov Chain Monte Carlo (MCMC) and Metropolis-Hastings (MH) samplers for computationally intensive Bayesian simulation.

### E. Data Fetching & Web APIs
*   **`rdbnomics`**: The ultimate "super-API" for macroeconomics. It aggregates 85+ databases including the ECB, BIS, Eurostat, IMF, OECD, and World Bank into a single, unified interface.
*   **`WDI`**: Directly downloads data from the World Bank's World Development Indicators into your R environment.
*   **`OECD`**: Official API wrapper to extract data from the Organisation for Economic Co-operation and Development.
*   **`imfr`**: Explores and downloads datasets from the International Monetary Fund.
*   **`eurostat`**: Direct access to the European Union's statistical office data.
*   **`fredr`**: API client for Federal Reserve Economic Data (FRED), perfect for fetching macroeconomic series.
*   **`quantmod`**: Quantitative Financial Modeling framework. Great for downloading daily stock prices, FX rates, and other financial data via Yahoo/Google Finance.
*   **`rvest` & `httr2`**: The core tools for scraping data from custom government websites that lack a dedicated API. (`httr2` and `jsonlite` are also essential for querying the [WTO API](https://apiportal.wto.org) directly).
    *   *(Warning: The CRAN package named `wTO` is for genetics, not trade! If you want a dedicated WTO package, you can use the unofficial `wtor` package. You can install it over the internet using `remotes::install_github("fabiansalazares/wtor")`, or install it offline using the backup source file provided in the `data/statistics` folder.)*

### F. International Trade & Multi-Nation Economics
*   **`comtradr`**: The official R client for the UN Comtrade API. Essential for downloading bilateral import and export data between countries.
*   **`tradestatistics`**: Provides access to the Open Trade Statistics API, offering cleaned and formatted international trade data.
*   **`gravity`**: A dedicated package for estimating gravity models of trade (including PPML, Anderson & van Wincoop models). Note: The `fixest` package (with `fepois()`) is also frequently used for modern gravity models.
*   **`pwt10`**: Provides the Penn World Table (Version 10) dataset directly in R. The gold standard for cross-country comparisons of relative levels of income, output, input, and productivity.
*   **`leontief`**: Used for Input-Output analysis, which is critical for measuring Global Value Chains (GVCs) and multi-nation trade linkages.

### G. Spatial Econometrics
*   **`sf`**: "Simple Features" - the modern, fast, and tidyverse-compatible way to handle spatial data and maps in R.
*   **`spatialreg`**: Contains advanced models for spatial regression (e.g., spatial lag and spatial error models).

### H. Data Visualization & Interactive Graphics
*   **`networkD3`**: Outstanding tool for rendering interactive **Sankey diagrams** and network graphs using D3.js.
*   **`ggalluvial`**: An extension for `ggplot2` to make static alluvial plots, which are effectively Sankey diagrams for categorical variables.
*   **`plotly`**: A powerhouse for interactive visualizations. It can seamlessly convert most `ggplot2` objects into interactive web graphs, and supports its own Sankey diagram builders.
*   **`ggridges`**: Creates ridgeline plots, which are fantastic for visualizing changing distributions (like income or wages) over time.
*   **`ggrepel`**: Crucial for any scatter plot. It prevents text labels from overlapping with data points.
*   **`viridis`**: Provides color palettes that are perceptually uniform, colorblind-friendly, and look great even when printed in grayscale.

### I. Basic Statistics & Manuscript Reporting
*   **`psych`** & **`Hmisc`**: Provide robust functions like `describe()` and `rcorr()` for essential descriptive statistics and correlation matrices with p-values.
*   **`car`**: Essential for basic diagnostic tests in manuscripts (e.g., ANOVA, Variance Inflation Factors (VIF) for multicollinearity, Levene's test).
*   **`gtsummary`**: Extremely powerful for generating a manuscript's "Table 1" (baseline characteristics and descriptive summary tables).
*   **`corrplot`**: Generates the classic, highly-visual correlation matrix plots seen in many publications.
*   **`report`**: A unique package that takes a statistical model and automatically writes an APA-formatted text summary for your manuscript.

### J. Journal Formatting & Advanced Tables
*   **`stargazer`**: Converts R regression output directly into publication-quality LaTeX code or HTML tables. It is the most widely used tool in economics for creating side-by-side regression tables.
*   **`modelsummary`**: A modern alternative to `stargazer` that creates beautiful tables and integrates seamlessly with `gt` and `kableExtra`.

---

## 3. Quick Reference Code Snippets

### Scenario 1: OLS with Robust Standard Errors
In economic journals, standard errors must almost always be robust.
```R
library(lmtest)
library(sandwich)

# Fit normal OLS
model <- lm(wage ~ education + experience, data = my_data)

# Print summary with HC1 robust standard errors
coeftest(model, vcov = vcovHC(model, type = "HC1"))
```

### Scenario 2: Panel Data Fixed Effects (The Modern Way)
Using `fixest` for fast, multi-dimensional fixed effects:
```R
library(fixest)

# Estimate effect of X on Y, with Individual and Year fixed effects.
# Standard errors are automatically clustered by 'id' (the first fixed effect).
fe_model <- feols(Y ~ X1 + X2 | id + year, data = panel_data)
summary(fe_model)
```

### Scenario 3: Exporting a Publication-Ready Table to LaTeX
When you need to export your results to your LaTeX manuscript:
```R
library(stargazer)

model1 <- lm(wage ~ education, data = my_data)
model2 <- lm(wage ~ education + experience, data = my_data)

# Generate LaTeX code for the manuscript
stargazer(model1, model2, 
          title = "Effect of Education on Wages",
          align = TRUE,
          type = "latex", # Change to "html" or "text" as needed
          out = "regression_results.tex")
```

### Scenario 4: Creating a "Table 1" Summary Table
Manuscripts often require a descriptive statistics table (Table 1).
```R
library(gtsummary)

# Creates a publication-ready summary table grouped by a specific variable
my_data %>%
  select(wage, education, experience, gender) %>%
  tbl_summary(by = gender) %>%
  add_p() # Automatically adds p-values for differences between groups
```

### Scenario 5: Automated APA Text Reporting
If you need help writing the results section for your manuscript:
```R
library(report)

model <- lm(wage ~ education, data = my_data)
# Generates a written, APA-formatted paragraph describing the model results
report(model)
```

### Scenario 6: Creating a Basic Interactive Sankey Diagram
Visualizing flows (e.g., migration, employment transitions) is best done with a Sankey diagram.
```R
library(networkD3)

# Define nodes (categories)
nodes <- data.frame(name = c("Employed", "Unemployed", "Retired"))

# Define links (flows between categories). Source and Target are 0-indexed!
links <- data.frame(
  source = c(0, 1, 0, 1), 
  target = c(1, 0, 2, 2),
  value =  c(10, 5, 20, 15)
)

# Generate the interactive diagram
sankeyNetwork(Links = links, Nodes = nodes, Source = "source",
              Target = "target", Value = "value", NodeID = "name",
              units = "People", fontSize = 14, nodeWidth = 30)
```

### Scenario 7: Installing GitHub Packages Offline (e.g., `wtor` for WTO data)
If a package is only available on GitHub (like the `wtor` package for World Trade Organization data), but you need to install it while offline or behind a strict firewall, you can use the `.tar.gz` source backup provided in your `data/statistics` folder.
```R
# Provide the absolute or relative path to the downloaded GitHub source tarball
install.packages("data/statistics/wtor_github_source.tar.gz", 
                 repos = NULL, 
                 type = "source")
```

### Scenario 8: Unifying Plot Outputs for the UnifiedFigureEngine
To seamlessly integrate R-generated statistical figures (like ROC or Kaplan-Meier curves) into the `UnifiedFigureEngine`, you must export both the figure and a "sidecar" JSON metadata file. The engine uses this JSON to autonomously generate mandatory Alt-Text and handle DOCX formatting.
```R
library(ggplot2)
library(jsonlite)

# 1. Generate plot using the universal EconoSuite theme
p <- ggplot(survival_data, aes(x = time, y = survival, color = treatment)) +
  geom_step() +
  theme_minimal() + # Use the standard EconoSuite theme here
  labs(title = "Overall Survival")

# 2. Export isolated figure with strict alphanumeric name
ggsave("outputs/figures/fig_km_overall.pdf", plot = p, width = 7, height = 5, dpi = 300)

# 3. Generate sidecar JSON metadata for the UnifiedFigureEngine
metadata <- list(
  figure_id = "fig_km_overall",
  type = "km_survival_curve",
  title = "Overall Survival by Treatment Cohort",
  key_statistics = list(
    log_rank_p_value = 0.024,
    median_survival_groupA = "14.2 months",
    median_survival_groupB = "18.5 months"
  ),
  source_data = "analysis_cohort_final.csv"
)
write_json(metadata, "outputs/figures/fig_km_overall.json", auto_unbox = TRUE)
```

---
*Created for the EconoSuite Project.*
