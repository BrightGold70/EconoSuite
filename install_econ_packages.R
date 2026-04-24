# ==============================================================================
# EconoSuite: Essential R Packages Installation Script
# Target OS: macOS
# Purpose: Setup R environment for Data Science and Economic Journal Manuscripts
# ==============================================================================

# Function to check and install missing packages
install_if_missing <- function(packages) {
  installed <- packages %in% rownames(installed.packages())
  if (any(!installed)) {
    message("Installing missing packages: ", paste(packages[!installed], collapse = ", "))
    # Using Posit's fast, reliable global mirror
    install.packages(packages[!installed], repos = "https://packagemanager.posit.co/cran/latest", dependencies = TRUE)
  } else {
    message("All specified packages are already installed.")
  }
}

# 1. Data Manipulation, Cleaning & Visualization
data_science <- c(
  "tidyverse",    # Includes dplyr, ggplot2, tidyr, readr, purrr
  "data.table",   # Fast data manipulation for large datasets
  "lubridate"     # Efficient date and time manipulation
)

# 2. Core Econometrics & Statistical Testing
core_econometrics <- c(
  "lmtest",       # Diagnostic tests (e.g., Breusch-Pagan, Durbin-Watson)
  "sandwich",     # Robust standard errors (HC, HAC, clustered)
  "AER",          # Applied Econometrics with R (Instrumental Variables, ivreg)
  "plm",          # Panel Data Econometrics (Fixed/Random effects models)
  "fixest"        # Extremely fast and efficient high-dimensional fixed-effects estimation
)

# 3. Time Series Analysis
time_series <- c(
  "forecast",     # Forecasting functions for time series (ARIMA, exponential smoothing)
  "tseries",      # Time series analysis and computational finance
  "urca",         # Unit root and cointegration tests (Dickey-Fuller, KPSS)
  "vars"          # Vector autoregressive (VAR) models
)

# 4. Causal Inference & Advanced Modeling
causal_inference <- c(
  "MatchIt",      # Propensity score matching and weighting
  "rdrobust",     # Regression Discontinuity Designs
  "Synth",        # Synthetic Control Methods for comparative case studies
  "did",          # Modern Difference-in-Differences (Callaway & Sant'Anna)
  "bacondecomp"   # Goodman-Bacon decomposition for TWFE DiD models
)

# 5. Machine Learning & High-Dimensional Controls
machine_learning <- c(
  "glmnet",       # Lasso and Elastic-Net (regularized regression)
  "grf",          # Generalized Random Forests (causal forests)
  "estimatr",     # Fast estimators for design-based inference (robust SEs)
  "xgboost",      # Extreme Gradient Boosting (high-performance ML prediction)
  "shapviz"       # SHAP values for Explainable AI (interpreting ML models)
)

# 6. Data Fetching APIs (World Bank, FRED, Stocks, WTO)
data_fetching <- c(
  "WDI",          # World Development Indicators (World Bank)
  "quantmod",     # Financial modeling and trading framework
  "fredr",        # Federal Reserve Economic Data (FRED) API
  "httr2",        # Modern HTTP client (essential for querying the WTO API)
  "jsonlite",     # JSON parser (essential for handling API responses)
  "remotes"       # Needed to install non-CRAN packages from GitHub (e.g., wtor)
)

# 7. International Trade & Multi-Nation Economics
international_trade <- c(
  "comtradr",         # UN Comtrade Database API (import/export data)
  "tradestatistics",  # Open Trade Statistics (OTS) API
  "gravity",          # Estimation of gravity models for trade
  "pwt10",            # Penn World Table version 10 (cross-country GDP, productivity)
  "leontief"          # Input-Output analysis for global value chains
)

# 8. Spatial Econometrics
spatial_econometrics <- c(
  "sf",           # Simple Features (modern spatial data handling)
  "spatialreg"    # Spatial regression models
)

# 9. Data Visualization & Interactive Graphics (e.g., Sankey)
data_visualization <- c(
  "networkD3",    # Interactive Sankey and network diagrams
  "ggalluvial",   # Alluvial plots (Sankey-style) for ggplot2
  "plotly",       # Interactive charts, including Sankey diagrams
  "DiagrammeR",   # Flowcharts and node/edge diagrams
  "ggridges",     # Ridgeline plots for visualizing distributions over time
  "ggrepel",      # Automatically repels text labels away from data points
  "viridis"       # Colorblind-friendly, publication-quality color palettes
)

# 10. Basic Statistics & Reporting for Manuscripts
basic_stats <- c(
  "psych",        # Essential descriptive stats (describe()) and reliability
  "Hmisc",        # Advanced correlations (rcorr()) and basic stats
  "car",          # Companion to Applied Regression (ANOVA, VIF, Levene's Test)
  "gtsummary",    # Elegant, publication-ready summary tables ("Table 1")
  "corrplot",     # Visual correlation matrices for manuscripts
  "report"        # Automatically translates statistical models into APA manuscript text
)

# 11. Journal Formatting & Advanced Tables (LaTeX / HTML / Word)
reporting <- c(
  "stargazer",    # Classic tool for generating beautiful LaTeX/HTML regression tables
  "modelsummary", # Modern, highly customizable table generator for models
  "kableExtra",   # Advanced table formatting
  "rmarkdown",    # Reproducible research documents
  "knitr"         # Dynamic report generation
)

# Combine all packages
all_packages <- c(data_science, core_econometrics, time_series, causal_inference, machine_learning, data_fetching, international_trade, spatial_econometrics, data_visualization, basic_stats, reporting)

# Execute the installation
message("Starting EconoSuite package installation for macOS...")
install_if_missing(all_packages)

message("\n=======================================================")
message("EconoSuite: Installation Complete!")
message("You are ready to begin your economic data analysis.")
message("=======================================================")
