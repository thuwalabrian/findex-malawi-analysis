# Financial Inclusion in Malawi: Global Findex 2024 Analysis

**Author:** Brian Thuwala  
**Date:** 2025–2026  
**Python:** 3.11+ | **Data:** World Bank Global Findex 2024

---

## Overview

This project analyzes financial inclusion in Malawi using the World Bank's
**Global Findex 2024** nationally representative microdata (n ≈ 1,000 adults).
Four Jupyter notebooks progress from data validation through descriptive
statistics to survey-weighted logistic regression and evidence-based policy
recommendations.

### Key Findings

| Indicator | Value |
|---|---|
| Any account ownership | ~50% |
| Mobile money only | ~35% |
| Formal bank account | ~12% |
| Gender gap (M − F, formal) | ~6 pp |
| Income gap (Q5 − Q1) | ~37 pp |
| Top barrier | Lack of money (~36%) |

> Mobile money is Malawi's dominant inclusion channel. Traditional banking
> reaches only 1 in 8 adults.

---

## Project Structure

```
findex-malawi-analysis/
├── README.md
├── requirements.txt
├── DATA_DICTIONARY.md
├── data/
│   ├── raw/
│   │   ├── Findex_Microdata_2025_updateMalawi.csv
│   │   └── codebook_microdata_2025.pdf
│   └── processed/
├── notebooks/
│   ├── 00_executive_summary.ipynb
│   ├── 01_data_import_and_checks.ipynb
│   ├── 02_descriptive_analysis.ipynb
│   ├── 03_barriers_analysis.ipynb
│   └── 04_from_barriers_to_policy.ipynb
├── dashboard/              ← ✨ NEW: Interactive web dashboard
│   ├── app.py
│   ├── utils.py
│   ├── assets/
│   │   └── style.css
│   └── README.md
└── outputs/
    ├── figures/   ← saved plots (PNG, 200 dpi)
    └── tables/    ← exported CSVs
```

## Notebooks

| # | Notebook | Purpose |
|---|---|---|
| 00 | Executive Summary | Policymaker-friendly overview of key findings and recommendations |
| 01 | Data Import & Checks | Load raw CSV, validate structure, document variables |
| 02 | Descriptive Analysis | Weighted national indicators, disaggregation by gender / residence / income / education |
| 03 | Barriers Analysis | Mobile money barrier prevalence (fin14a–e), demographic segmentation, chi-squared tests |
| 04 | From Barriers to Policy | Survey-weighted logistic regression (dual-outcome), ROC diagnostics, interaction effects, forest plots, policy priority matrix, evidence-based recommendations |

Each notebook is **self-contained** — it reloads data from disk and does not
depend on in-memory objects from previous notebooks.

---

## Methodology

- **Survey weights** (`wgt`) applied to all population-level estimates and to
  the logistic regression via `freq_weights`.
- **Dual-outcome modelling:** Model 1 predicts formal account ownership
  (`account_fin`); Model 2 predicts any-account ownership (`account`).
- **Variable coding verified** against the official Global Findex 2024
  codebook (`codebook_microdata_2025.pdf`).
- **Selection bias documented:** Barrier questions (fin11, fin14) are
  conditional on exclusion. Coefficients are associations within the
  at-risk population, not causal effects.
- **Gender coding:** `female=1` (Female), `female=2` (Male) in raw data;
  recoded to 1/0 binary for regression in Notebook 04.

---

## Setup

### Prerequisites

- Python 3.11+
- Jupyter Notebook or VS Code with Jupyter extension

### Installation

```bash
pip install -r requirements.txt
```

Place the raw data file in `data/raw/` and run notebooks in order: 01 → 04.

### 🚀 Interactive Dashboard

Launch the high-end interactive web dashboard:

```bash
# Option 1: Use the launcher script
python launch_dashboard.py

# Option 2: Direct launch
cd dashboard
python app.py
```

Then open your browser to **http://127.0.0.1:8050/**

**Dashboard Features:**
- 📊 Five interactive tabs: Overview, Demographics, Barriers, Policy, Models
- 📈 Dynamic Plotly visualizations
- 💡 Real-time KPI cards
- 📱 Fully responsive design
- 🎨 Professional UI with Bootstrap theme

### Data

The raw microdata file is not included due to licensing. Download from the
[World Bank Global Findex Database](https://www.worldbank.org/en/publication/globalfindex).

---

## Technical Notes

1. **No global listwise deletion** — missing values handled per-variable.
2. **Composite barrier variables** combine bank (fin11) and mobile money
   (fin14) barriers by theme. In Malawi, fin11a–f have zero valid responses
   (survey routing), so composites derive from fin14a–e only.
3. **ROC threshold optimisation** (Youden's J) addresses severe class
   imbalance in the formal-account model (~12% positive class).
4. **Interaction effects** test whether barriers affect demographic subgroups
   differently (Gender × Cost, Income × Distance, Gender × Money).

---

## Citation

> World Bank. 2024. *Global Findex Database 2024: Malawi Microdata.*
> Washington, DC: World Bank.

---

## Contact

**Brian Thuwala** — thuwalabrian@gmail.com
