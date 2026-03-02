"""
Data Loading Utilities for Findex Malawi Dashboard
Loads and processes all analysis outputs for visualization
"""

import pandas as pd
import os
from pathlib import Path

# Define project root - go up one level from dashboard directory
PROJECT_ROOT = Path(__file__).parent.parent
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def load_national_indicators():
    """Load national-level financial inclusion indicators"""
    df = pd.read_csv(TABLES_DIR / "national_indicators.csv")
    return df


def load_gender_gap():
    """Load gender-disaggregated statistics"""
    df = pd.read_csv(TABLES_DIR / "gender_gap.csv")
    return df


def load_income_gradient():
    """Load financial inclusion by income quintile"""
    df = pd.read_csv(TABLES_DIR / "income_gradient.csv", index_col=0)
    df = df.reset_index()
    df.columns = ["Quintile"] + list(df.columns[1:])
    # Ensure proper ordering
    quintile_order = [
        "Poorest 20%",
        "Second 20%",
        "Middle 20%",
        "Fourth 20%",
        "Richest 20%",
    ]
    df["Quintile"] = pd.Categorical(
        df["Quintile"], categories=quintile_order, ordered=True
    )
    df = df.sort_values("Quintile")
    return df


def load_education_gradient():
    """Load financial inclusion by education level"""
    df = pd.read_csv(TABLES_DIR / "education_gradient.csv", index_col=0)
    df = df.reset_index()
    df.columns = ["Education"] + list(df.columns[1:])
    # Ensure proper ordering
    edu_order = ["Primary or less", "Secondary", "Tertiary+"]
    df["Education"] = pd.Categorical(
        df["Education"], categories=edu_order, ordered=True
    )
    df = df.sort_values("Education")
    return df


def load_account_types():
    """Load account type breakdown"""
    df = pd.read_csv(TABLES_DIR / "account_type_breakdown.csv")
    return df


def load_barriers():
    """Load barrier analysis data"""
    df = pd.read_csv(TABLES_DIR / "mm_barrier_prevalence.csv")
    return df


def load_barrier_demographics():
    """Load barriers by demographic groups"""
    df = pd.read_csv(TABLES_DIR / "barrier_by_demographics.csv")
    return df


def load_policy_priorities():
    """Load policy priority matrix"""
    df = pd.read_csv(TABLES_DIR / "policy_priority_matrix.csv")
    
    # Calculate Feasibility score if not present (scale 0-10)
    # Higher OR Formal = more feasible to address with formal account interventions
    if "Feasibility" not in df.columns:
        # Normalize OR Formal to 0-10 scale
        or_max = df["OR Formal"].max()
        df["Feasibility"] = (df["OR Formal"] / or_max * 10).clip(0, 10)
    
    return df


def load_regression_results(model_type="any_account"):
    """
    Load regression model results

    Parameters:
    -----------
    model_type : str
        'any_account' or 'formal_account'
    """
    filename = f"regression_{model_type}.csv"
    df = pd.read_csv(TABLES_DIR / filename)
    return df


def load_vif_diagnostics():
    """Load VIF multicollinearity diagnostics"""
    df = pd.read_csv(TABLES_DIR / "vif_diagnostics.csv")
    return df


def get_summary_stats():
    """Generate summary statistics for dashboard cards"""
    national = load_national_indicators()
    gender = load_gender_gap()

    stats = {
        "any_account": national[national["Indicator"] == "Any Account"][
            "Rate (%)"
        ].iloc[0],
        "mobile_money": national[national["Indicator"] == "Mobile Money Account"][
            "Rate (%)"
        ].iloc[0],
        "formal_bank": national[national["Indicator"] == "Formal/Bank Account"][
            "Rate (%)"
        ].iloc[0],
        "gender_gap": gender[gender["Indicator"] == "Formal/Bank"]["Gap (pp)"].iloc[0],
        "saved": national[national["Indicator"] == "Saved (Any Method)"][
            "Rate (%)"
        ].iloc[0],
        "borrowed": national[national["Indicator"] == "Borrowed (Any Source)"][
            "Rate (%)"
        ].iloc[0],
    }

    return stats


def format_percentage(value, decimals=1):
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"


def format_odds_ratio(value, decimals=2):
    """Format value as odds ratio"""
    return f"{value:.{decimals}f}"
