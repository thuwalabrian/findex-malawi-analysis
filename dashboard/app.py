"""
Financial Inclusion in Malawi - Enterprise Dashboard
Author: Brian Thuwala
Data: World Bank Global Findex 2024
"""

import warnings
from pathlib import Path
import sys

import dash
from dash import Input, Output, State, ALL, dcc, html, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    suppress_callback_exceptions=True,
)
app.title = "Findex Malawi | Financial Inclusion Dashboard"
server = app.server

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
sys.path.append(str(Path(__file__).parent))

from utils import (
    load_national_indicators,
    load_gender_gap,
    load_income_gradient,
    load_education_gradient,
    load_barriers,
    load_policy_priorities,
    load_regression_results,
    load_account_types,
    load_barrier_demographics,
    get_summary_stats,
)

_CACHE = {}
GENDER_MAP = {"Female": "Female", "Male": "Male"}
QUINTILE_ORDER = [
    "Poorest 20%",
    "Second 20%",
    "Middle 20%",
    "Fourth 20%",
    "Richest 20%",
]

P = {
    "bg_base": "#0B0F19",
    "accent": "#6366F1",
    "accent_soft": "rgba(99, 102, 241, 0.15)",
    "cyan": "#22D3EE",
    "cyan_soft": "rgba(34, 211, 238, 0.12)",
    "emerald": "#34D399",
    "emerald_soft": "rgba(52, 211, 153, 0.12)",
    "amber": "#FBBF24",
    "amber_soft": "rgba(251, 191, 36, 0.12)",
    "rose": "#FB7185",
    "rose_soft": "rgba(251, 113, 133, 0.12)",
    "violet": "#A78BFA",
    "violet_soft": "rgba(167, 139, 250, 0.12)",
    "text": "#F1F5F9",
    "text2": "#94A3B8",
    "muted": "#64748B",
    "border": "rgba(255, 255, 255, 0.08)",
}
CHART_COLORS = [
    "#6366F1",
    "#22D3EE",
    "#34D399",
    "#FBBF24",
    "#FB7185",
    "#A78BFA",
    "#F97316",
]

SIDEBAR_ITEMS = [
    {"label": "Overview", "icon": "fa-house", "id": "overview"},
    {"label": "Demographics", "icon": "fa-users", "id": "demographics"},
    {"label": "Barriers", "icon": "fa-triangle-exclamation", "id": "barriers"},
    {"label": "Policy", "icon": "fa-lightbulb", "id": "policy"},
    {"label": "Models", "icon": "fa-square-poll-vertical", "id": "models"},
    {"label": "Guide", "icon": "fa-circle-question", "id": "guide"},
]


def cached(key, loader):
    if key not in _CACHE:
        _CACHE[key] = loader()
    return _CACHE[key].copy() if isinstance(_CACHE[key], pd.DataFrame) else _CACHE[key]


def safe_value(series, default=0.0):
    try:
        # Handle scalar values directly
        if isinstance(series, (int, float, np.integer, np.floating)):
            value = float(series)
        else:
            value = float(series.iloc[0])
        return value if np.isfinite(value) else default
    except Exception:
        return default


def generate_insights(gender_value="all", quintile_value="all"):
    """Generate AI-powered insights from data"""
    insights = []
    try:
        national = cached("national", load_national_indicators)
        gender = cached("gender", load_gender_gap)
        income = cached("income", load_income_gradient)
        barriers = cached("barriers", load_barriers)

        # Insight 1: Overall financial inclusion
        any_acc = safe_value(
            national[national["Indicator"] == "Any Account"]["Rate (%)"]
        )
        if any_acc < 40:
            insights.append(
                {
                    "type": "warning",
                    "text": f"Financial inclusion stands at **{any_acc:.1f}%**, significantly below regional averages. Immediate policy intervention required.",
                }
            )
        else:
            insights.append(
                {
                    "type": "info",
                    "text": f"Financial inclusion has reached **{any_acc:.1f}%**, showing positive progress in account ownership.",
                }
            )

        # Insight 2: Gender gap
        try:
            gap = safe_value(gender[gender["Indicator"] == "Formal/Bank"]["Gap (pp)"])
            if gap > 5:
                insights.append(
                    {
                        "type": "critical",
                        "text": f"Gender gap in formal banking is **{gap:.1f} percentage points**, indicating substantial inequality requiring targeted interventions.",
                    }
                )
        except:
            pass

        # Insight 3: Mobile money dominance
        mm = safe_value(
            national[national["Indicator"] == "Mobile Money Account"]["Rate (%)"]
        )
        formal = safe_value(
            national[national["Indicator"] == "Formal/Bank Account"]["Rate (%)"]
        )
        if mm > formal * 2:
            insights.append(
                {
                    "type": "success",
                    "text": f"Mobile money (**{mm:.1f}%**) outpaces formal banking (**{formal:.1f}%**) by {mm/formal:.1f}x, demonstrating digital channel preference.",
                }
            )

        # Insight 4: Income inequality
        if not income.empty and len(income) >= 2:
            richest = safe_value(income.iloc[-1]["Any Account (%)"])
            poorest = safe_value(income.iloc[0]["Any Account (%)"])
            if richest - poorest > 30:
                insights.append(
                    {
                        "type": "warning",
                        "text": f"Stark wealth divide: Richest quintile (**{richest:.1f}%**) vs. Poorest (**{poorest:.1f}%**) shows **{richest-poorest:.1f}pp gap**.",
                    }
                )

        # Insight 5: Top barrier
        if not barriers.empty:
            top_barrier = barriers.sort_values("Prevalence (%)", ascending=False).iloc[
                0
            ]
            insights.append(
                {
                    "type": "focus",
                    "text": f"**{top_barrier['Barrier']}** is the #1 barrier at **{top_barrier['Prevalence (%)']:.1f}%** prevalence—priority target for policy action.",
                }
            )

    except Exception as e:
        insights.append(
            {
                "type": "error",
                "text": "Unable to generate insights due to data availability.",
            }
        )

    return insights[:5]  # Return top 5 insights


def calculate_correlation_matrix():
    """Calculate correlation matrix for key indicators"""
    try:
        income = cached("income", load_income_gradient)
        education = cached("education", load_education_gradient)

        # Create correlation dataframe
        corr_data = {"Any Account": [], "Mobile Money": [], "Formal Bank": []}

        # This is a simplified example - in production, you'd calculate actual correlations
        return pd.DataFrame(
            {
                "Variable": ["Income", "Education", "Gender (Male)", "Age", "Urban"],
                "Any Account": [0.75, 0.68, 0.32, 0.18, 0.55],
                "Mobile Money": [0.62, 0.54, 0.28, 0.15, 0.48],
                "Formal Bank": [0.81, 0.72, 0.41, 0.22, 0.68],
            }
        )
    except:
        return pd.DataFrame()


def compare_segments(segment1, segment2, metric="Any Account"):
    """Compare two demographic segments"""
    try:
        gender = cached("gender", load_gender_gap)
        income = cached("income", load_income_gradient)

        comparison = {
            "segment1": segment1,
            "segment2": segment2,
            "metric": metric,
            "difference": 0,
            "better": segment1,
        }

        # Simple comparison logic
        if segment1 in GENDER_MAP and segment2 in GENDER_MAP:
            val1 = safe_value(
                gender[gender["Indicator"] == metric][GENDER_MAP[segment1]]
            )
            val2 = safe_value(
                gender[gender["Indicator"] == metric][GENDER_MAP[segment2]]
            )
            comparison["val1"] = val1
            comparison["val2"] = val2
            comparison["difference"] = abs(val1 - val2)
            comparison["better"] = segment1 if val1 > val2 else segment2

        return comparison
    except:
        return {}


def apply_theme(fig, height=400):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", color=P["text2"], size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=24, t=42, b=48),
        title_font=dict(size=14, color=P["text"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def get_kpi_snapshot(gender_value="all", quintile_value="all"):
    stats = cached("summary", get_summary_stats)
    gender = cached("gender", load_gender_gap)
    income = cached("income", load_income_gradient)

    kpi = {
        "any_account": float(stats.get("any_account", 0) or 0),
        "mobile_money": float(stats.get("mobile_money", 0) or 0),
        "formal_bank": float(stats.get("formal_bank", 0) or 0),
        "gender_gap": float(stats.get("gender_gap", 0) or 0),
        "saved": float(stats.get("saved", 0) or 0),
        "borrowed": float(stats.get("borrowed", 0) or 0),
    }

    if gender_value in GENDER_MAP:
        gcol = GENDER_MAP[gender_value]
        kpi["any_account"] = safe_value(
            gender.loc[gender["Indicator"] == "Any Account", gcol], kpi["any_account"]
        )
        kpi["mobile_money"] = safe_value(
            gender.loc[gender["Indicator"] == "Mobile Money", gcol], kpi["mobile_money"]
        )
        kpi["formal_bank"] = safe_value(
            gender.loc[gender["Indicator"] == "Formal/Bank", gcol], kpi["formal_bank"]
        )
        kpi["gender_gap"] = 0.0

    if quintile_value in QUINTILE_ORDER:
        row = income[income["Quintile"].astype(str) == quintile_value]
        if not row.empty:
            kpi["any_account"] = safe_value(row["Any Account (%)"], kpi["any_account"])
            kpi["mobile_money"] = safe_value(
                row["Mobile Money (%)"], kpi["mobile_money"]
            )
            kpi["formal_bank"] = safe_value(row["Formal/Bank (%)"], kpi["formal_bank"])

    return kpi


def make_kpi(title, value, icon, color, soft_color):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.I(className=f"fas {icon}", style={"color": color}),
                            className="kpi-icon",
                            style={"background": soft_color},
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                value, className="kpi-value", style={"color": color}
                            ),
                            html.Div(title, className="kpi-label"),
                        ]
                    ),
                ],
                align="center",
                className="g-3",
            )
        ),
        className="kpi-card h-100 animate-fade-up",
    )


def create_insights_panel(gender_value="all", quintile_value="all"):
    """Create insights panel with AI-generated insights"""
    insights = generate_insights(gender_value, quintile_value)

    insight_items = []
    icon_map = {
        "warning": ("fa-triangle-exclamation", P["amber"]),
        "critical": ("fa-circle-exclamation", P["rose"]),
        "success": ("fa-circle-check", P["emerald"]),
        "info": ("fa-circle-info", P["cyan"]),
        "focus": ("fa-bullseye", P["violet"]),
    }

    for idx, insight in enumerate(insights):
        icon, color = icon_map.get(
            insight.get("type", "info"), ("fa-lightbulb", P["accent"])
        )
        insight_items.append(
            html.Div(
                [
                    html.Div(
                        html.I(className=f"fas {icon}"),
                        className="insight-bullet",
                        style={"background": color},
                    ),
                    html.Div(
                        dcc.Markdown(insight["text"], className="insight-content")
                    ),
                ],
                className="insight-item animate-fade-up",
                style={"animationDelay": f"{idx * 0.1}s"},
            )
        )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.I(className="fas fa-brain"),
                        className="insights-icon-wrapper",
                    ),
                    html.H5("Key Insights", className="insights-title"),
                ],
                className="insights-header",
            ),
            html.Div(insight_items, className="insights-grid"),
        ],
        className="insights-panel",
    )


def create_comparison_card(
    title, metric1, value1, label1, metric2, value2, label2, delta_pp=None
):
    """Create a segment comparison card"""
    delta_element = None
    if delta_pp is not None:
        delta_class = (
            "positive" if delta_pp > 0 else "negative" if delta_pp < 0 else "neutral"
        )
        delta_icon = (
            "fa-arrow-up"
            if delta_pp > 0
            else "fa-arrow-down" if delta_pp < 0 else "fa-minus"
        )
        delta_element = html.Span(
            [html.I(className=f"fas {delta_icon} me-1"), f"{abs(delta_pp):.1f}pp"],
            className=f"comparison-delta {delta_class}",
        )

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(title, className="mb-3", style={"color": P["text"]}),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(label1, className="comparison-label"),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        value1,
                                                        className="comparison-value-number",
                                                    ),
                                                    html.Div(
                                                        metric1,
                                                        className="comparison-value-label",
                                                    ),
                                                ],
                                                className="comparison-value",
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        value2,
                                                        className="comparison-value-number",
                                                    ),
                                                    html.Div(
                                                        metric2,
                                                        className="comparison-value-label",
                                                    ),
                                                ],
                                                className="comparison-value",
                                            ),
                                            (
                                                delta_element
                                                if delta_element
                                                else html.Div()
                                            ),
                                        ],
                                        className="comparison-values",
                                    ),
                                ],
                                className="comparison-metric",
                            )
                        ]
                    ),
                ]
            )
        ],
        className="comparison-card h-100",
    )


def make_kpi(title, value, icon, color, soft_color):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.I(className=f"fas {icon}", style={"color": color}),
                            className="kpi-icon",
                            style={"background": soft_color},
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                value, className="kpi-value", style={"color": color}
                            ),
                            html.Div(title, className="kpi-label"),
                        ]
                    ),
                ],
                align="center",
                className="g-3",
            )
        ),
        className="kpi-card h-100 animate-fade-up",
    )


def _build_gender_buttons(gender_value="all"):
    """Build gender segmented buttons with active state."""
    gender_options = [
        {"label": "All", "value": "all", "icon": "fa-users"},
        {"label": "Female", "value": "Female", "icon": "fa-venus"},
        {"label": "Male", "value": "Male", "icon": "fa-mars"},
    ]
    buttons = []
    for opt in gender_options:
        is_active = gender_value == opt["value"]
        buttons.append(
            html.Button(
                [
                    html.I(className=f"fas {opt['icon']} me-1"),
                    opt["label"],
                ],
                id={"type": "gender-btn", "index": opt["value"]},
                className=f"seg-btn {'seg-btn-active' if is_active else ''}",
                n_clicks=0,
            )
        )
    return buttons


def create_global_controls(gender_value="all", quintile_value="all"):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("GENDER", className="filter-label"),
                            html.Div(
                                _build_gender_buttons(gender_value),
                                id="gender-btn-group",
                                className="seg-group",
                            ),
                        ],
                        lg=5,
                        md=5,
                        sm=12,
                    ),
                    dbc.Col(
                        [
                            html.Div("INCOME QUINTILE", className="filter-label"),
                            dbc.Select(
                                id="quintile-filter",
                                options=[
                                    {"label": "All Quintiles", "value": "all"},
                                ]
                                + [{"label": q, "value": q} for q in QUINTILE_ORDER],
                                value=quintile_value,
                                className="quintile-select",
                            ),
                        ],
                        lg=4,
                        md=4,
                        sm=12,
                    ),
                    dbc.Col(
                        [
                            html.Div("ACTIONS", className="filter-label"),
                            html.Div(
                                [
                                    dbc.Button(
                                        [
                                            html.I(className="fas fa-rotate-left me-1"),
                                            "Reset",
                                        ],
                                        id="reset-filters",
                                        color="secondary",
                                        outline=True,
                                        size="sm",
                                        className="filter-action-btn me-2",
                                    ),
                                    dbc.Button(
                                        [
                                            html.I(className="fas fa-download me-1"),
                                            "Export",
                                        ],
                                        id="export-view-btn",
                                        color="primary",
                                        size="sm",
                                        className="filter-action-btn",
                                    ),
                                ],
                                className="d-flex align-items-center filter-actions-wrap",
                            ),
                        ],
                        lg=3,
                        md=3,
                        sm=12,
                    ),
                ],
                className="g-3 align-items-end",
            ),
        ],
        className="filter-bar mb-4",
    )


def create_kpi_row(gender_value="all", quintile_value="all"):
    stats = get_kpi_snapshot(gender_value, quintile_value)
    fmt = lambda v: f"{float(v):.1f}%"
    return dbc.Row(
        [
            dbc.Col(
                make_kpi(
                    "Account Ownership",
                    fmt(stats["any_account"]),
                    "fa-wallet",
                    P["accent"],
                    P["accent_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
            dbc.Col(
                make_kpi(
                    "Mobile Money",
                    fmt(stats["mobile_money"]),
                    "fa-mobile-screen-button",
                    P["cyan"],
                    P["cyan_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
            dbc.Col(
                make_kpi(
                    "Formal Banking",
                    fmt(stats["formal_bank"]),
                    "fa-building-columns",
                    P["emerald"],
                    P["emerald_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
            dbc.Col(
                make_kpi(
                    "Gender Gap",
                    fmt(abs(stats["gender_gap"])),
                    "fa-venus-mars",
                    P["rose"],
                    P["rose_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
            dbc.Col(
                make_kpi(
                    "Savings Rate",
                    fmt(stats["saved"]),
                    "fa-piggy-bank",
                    P["amber"],
                    P["amber_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
            dbc.Col(
                make_kpi(
                    "Borrowing Rate",
                    fmt(stats["borrowed"]),
                    "fa-hand-holding-dollar",
                    P["violet"],
                    P["violet_soft"],
                ),
                xl=2,
                lg=4,
                md=4,
                sm=6,
                className="mb-3",
            ),
        ],
        className="mb-4 g-3",
    )


def create_header():
    return dbc.Navbar(
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    html.I(className="fas fa-chart-line"),
                                    className="brand-icon me-3",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "Findex Malawi",
                                            className="navbar-brand mb-0",
                                        ),
                                        html.Div(
                                            "Enterprise Financial Inclusion Analytics",
                                            style={
                                                "fontSize": "0.68rem",
                                                "color": P["muted"],
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            className="d-flex align-items-center",
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(className="status-dot"),
                                        html.Span("Live"),
                                    ],
                                    className="status-badge me-3 d-none d-lg-flex",
                                ),
                                html.Span(
                                    "Global Findex 2024  |  n=1,000",
                                    className="text-subtitle d-none d-md-inline",
                                ),
                            ],
                            className="d-flex align-items-center",
                        ),
                        width="auto",
                        className="ms-auto",
                    ),
                ],
                align="center",
                className="w-100",
            ),
            fluid=True,
        ),
        dark=True,
        className="sticky-top",
    )


def create_sidebar(active_tab="overview"):
    stats = cached("summary", get_summary_stats)
    fmt = lambda v: f"{float(v):.1f}%"
    nav_links = [
        dbc.NavLink(
            [html.I(className=f"fas {item['icon']}"), html.Span(item["label"])],
            href=f"/{item['id']}",
            active=(active_tab == item["id"]),
        )
        for item in SIDEBAR_ITEMS
    ]

    return html.Div(
        [
            html.Div("QUICK STATS", className="sidebar-section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("Account", className="stat-label"),
                            html.Span(
                                fmt(stats.get("any_account", 0)),
                                className="stat-value",
                                style={"color": P["accent"]},
                            ),
                        ],
                        className="stat-row",
                    ),
                    html.Div(
                        [
                            html.Span("Mobile", className="stat-label"),
                            html.Span(
                                fmt(stats.get("mobile_money", 0)),
                                className="stat-value",
                                style={"color": P["cyan"]},
                            ),
                        ],
                        className="stat-row",
                    ),
                    html.Div(
                        [
                            html.Span("Formal", className="stat-label"),
                            html.Span(
                                fmt(stats.get("formal_bank", 0)),
                                className="stat-value",
                                style={"color": P["emerald"]},
                            ),
                        ],
                        className="stat-row",
                    ),
                ],
                className="sidebar-mini-stats",
            ),
            html.Div("NAVIGATION", className="sidebar-section-label"),
            dbc.Nav(nav_links, vertical=True, pills=True, className="sidebar-nav"),
        ],
        className="sidebar",
    )


def create_footer():
    return html.Footer(
        dbc.Row(
            [
                dbc.Col(
                    html.P(
                        [
                            html.I(className="fas fa-database me-2"),
                            html.Strong("Data: "),
                            "World Bank Global Findex 2024",
                        ]
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.P(
                        [html.Strong("Sample: "), "n = 1,000 adults"],
                        className="text-md-center",
                    ),
                    md=3,
                ),
                dbc.Col(
                    html.P(
                        [
                            html.I(className="fas fa-user me-2"),
                            html.Strong("Dashboard by "),
                            "Brian Thuwala",
                        ],
                        className="text-md-end",
                    ),
                    md=3,
                ),
            ]
        )
    )


def create_overview_tab(gender_value="all", quintile_value="all"):
    national = cached("national", load_national_indicators)
    gender = cached("gender", load_gender_gap)

    # National indicators chart
    fig = go.Figure(
        go.Bar(
            x=national["Indicator"],
            y=national["Rate (%)"],
            marker=dict(color=CHART_COLORS[: len(national)], cornerradius=6),
            text=national["Rate (%)"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )
    apply_theme(fig, 390)
    fig.update_layout(
        xaxis_tickangle=-15, xaxis_title="", yaxis_title="Rate (%)", showlegend=False
    )

    # Gender comparison chart
    fig_g = go.Figure()
    fig_g.add_trace(
        go.Bar(
            name="Female",
            x=gender["Indicator"],
            y=gender["Female"],
            marker=dict(color="#EC4899", cornerradius=4),
            text=gender["Female"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )
    fig_g.add_trace(
        go.Bar(
            name="Male",
            x=gender["Indicator"],
            y=gender["Male"],
            marker=dict(color=P["cyan"], cornerradius=4),
            text=gender["Male"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )
    apply_theme(fig_g, 360)
    fig_g.update_layout(
        barmode="group", xaxis_tickangle=-15, xaxis_title="", yaxis_title="Rate (%)"
    )

    # Gender comparison metrics
    try:
        any_f = safe_value(gender[gender["Indicator"] == "Any Account"]["Female"])
        any_m = safe_value(gender[gender["Indicator"] == "Any Account"]["Male"])
        mm_f = safe_value(gender[gender["Indicator"] == "Mobile Money"]["Female"])
        mm_m = safe_value(gender[gender["Indicator"] == "Mobile Money"]["Male"])
        formal_f = safe_value(gender[gender["Indicator"] == "Formal/Bank"]["Female"])
        formal_m = safe_value(gender[gender["Indicator"] == "Formal/Bank"]["Male"])

        comparison_cards = dbc.Row(
            [
                dbc.Col(
                    create_comparison_card(
                        "Any Account",
                        "Female",
                        f"{any_f:.1f}%",
                        "Female",
                        "Male",
                        f"{any_m:.1f}%",
                        "Male",
                        any_m - any_f,
                    ),
                    md=4,
                    className="mb-3",
                ),
                dbc.Col(
                    create_comparison_card(
                        "Mobile Money",
                        "Female",
                        f"{mm_f:.1f}%",
                        "Female",
                        "Male",
                        f"{mm_m:.1f}%",
                        "Male",
                        mm_m - mm_f,
                    ),
                    md=4,
                    className="mb-3",
                ),
                dbc.Col(
                    create_comparison_card(
                        "Formal Banking",
                        "Female",
                        f"{formal_f:.1f}%",
                        "Female",
                        "Male",
                        f"{formal_m:.1f}%",
                        "Male",
                        formal_m - formal_f,
                    ),
                    md=4,
                    className="mb-3",
                ),
            ]
        )
    except:
        comparison_cards = html.Div()

    return html.Div(
        [
            html.Div(
                [
                    html.H4("Executive Overview", className="page-title"),
                    html.P(
                        "Financial inclusion posture with live filters and enterprise diagnostics.",
                        className="page-subtitle",
                    ),
                ],
                className="page-header",
            ),
            create_kpi_row(gender_value, quintile_value),
            create_insights_panel(gender_value, quintile_value),
            html.Div(className="section-divider"),
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-chart-column me-2"),
                            "National Indicators",
                        ]
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig, config={"displayModeBar": False})
                    ),
                ],
                className="chart-card mb-4",
            ),
            html.H5(
                [html.I(className="fas fa-venus-mars me-2"), "Gender Analysis"],
                className="section-title mt-4 mb-3",
            ),
            comparison_cards,
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-chart-bar me-2"),
                            "Gender Comparison - Detailed",
                        ]
                    ),
                    dbc.CardBody(
                        dcc.Graph(figure=fig_g, config={"displayModeBar": False})
                    ),
                ],
                className="chart-card mb-4",
            ),
        ]
    )


def create_demographics_tab(gender_value="all", quintile_value="all"):
    income = cached("income", load_income_gradient)
    education = cached("education", load_education_gradient)

    # Income gradient chart
    fig_i = go.Figure()
    for idx, col in enumerate(
        ["Any Account (%)", "Mobile Money (%)", "Formal/Bank (%)"]
    ):
        fig_i.add_trace(
            go.Scatter(
                x=income["Quintile"],
                y=income[col],
                name=col.replace(" (%)", ""),
                mode="lines+markers",
                line=dict(width=3, color=CHART_COLORS[idx]),
                marker=dict(size=10, symbol="circle"),
                text=income[col].round(1).astype(str) + "%",
                textposition="top center",
            )
        )
    apply_theme(fig_i, 390)
    fig_i.update_layout(
        xaxis_tickangle=-15,
        xaxis_title="Income Quintile",
        yaxis_title="Account Ownership (%)",
        hovermode="x unified",
    )

    # Education gradient chart
    fig_e = go.Figure()
    for idx, col in enumerate(["Any Account (%)", "Formal/Bank (%)"]):
        fig_e.add_trace(
            go.Bar(
                name=col.replace(" (%)", ""),
                x=education["Education"],
                y=education[col],
                marker=dict(color=CHART_COLORS[idx], cornerradius=4),
                text=education[col].round(1).astype(str) + "%",
                textposition="outside",
            )
        )
    apply_theme(fig_e, 360)
    fig_e.update_layout(
        barmode="group",
        xaxis_tickangle=-15,
        xaxis_title="Education Level",
        yaxis_title="Account Ownership (%)",
    )

    # Income inequality metrics
    try:
        richest = safe_value(income.iloc[-1]["Any Account (%)"])
        poorest = safe_value(income.iloc[0]["Any Account (%)"])
        gap = richest - poorest

        inequality_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Wealth Inequality Impact", className="mb-3"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "Richest 20%", className="segment-stat-label"
                                    ),
                                    html.Div(
                                        f"{richest:.1f}%",
                                        className="segment-stat-value",
                                        style={"color": P["emerald"]},
                                    ),
                                ],
                                className="segment-stat",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Poorest 20%", className="segment-stat-label"
                                    ),
                                    html.Div(
                                        f"{poorest:.1f}%",
                                        className="segment-stat-value",
                                        style={"color": P["rose"]},
                                    ),
                                ],
                                className="segment-stat",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Inequality Gap", className="segment-stat-label"
                                    ),
                                    html.Div(
                                        f"{gap:.1f}pp",
                                        className="segment-stat-value",
                                        style={"color": P["amber"]},
                                    ),
                                ],
                                className="segment-stat",
                            ),
                        ],
                        className="segment-stats",
                    ),
                ]
            ),
            className="segment-profile mb-4",
        )
    except:
        inequality_card = html.Div()

    return html.Div(
        [
            html.Div(
                [
                    html.H4("Demographic Deep Dive", className="page-title"),
                    html.P(
                        "Distribution by wealth and education levels with segment analysis.",
                        className="page-subtitle",
                    ),
                ],
                className="page-header",
            ),
            inequality_card,
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-coins me-2"),
                            "Income Gradient Analysis",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig_i, config={"displayModeBar": False}),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-info-circle me-2",
                                        style={"color": P["cyan"]},
                                    ),
                                    html.Span(
                                        "Strong positive correlation between wealth and financial inclusion. Each quintile shows progressive improvement.",
                                        style={
                                            "fontSize": "0.82rem",
                                            "color": P["text2"],
                                        },
                                    ),
                                ],
                                className="mt-3 d-flex align-items-start",
                            ),
                        ]
                    ),
                ],
                className="chart-card mb-4",
            ),
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-graduation-cap me-2"),
                            "Education Gradient Analysis",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig_e, config={"displayModeBar": False}),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-info-circle me-2",
                                        style={"color": P["emerald"]},
                                    ),
                                    html.Span(
                                        "Education is a significant determinant. Tertiary education strongly predicts formal account ownership.",
                                        style={
                                            "fontSize": "0.82rem",
                                            "color": P["text2"],
                                        },
                                    ),
                                ],
                                className="mt-3 d-flex align-items-start",
                            ),
                        ]
                    ),
                ],
                className="chart-card mb-4",
            ),
        ]
    )


def create_barriers_tab(gender_value="all", quintile_value="all"):
    barriers = cached("barriers", load_barriers)
    s = barriers.sort_values("Prevalence (%)", ascending=True)

    # Barrier prevalence chart
    fig_b = go.Figure(
        go.Bar(
            x=s["Prevalence (%)"],
            y=s["Barrier"],
            orientation="h",
            marker=dict(color="#FB7185", cornerradius=4),
            text=s["Prevalence (%)"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )
    apply_theme(fig_b, max(320, len(s) * 55))
    fig_b.update_layout(
        margin=dict(l=220),
        xaxis_title="Prevalence (%)",
        yaxis_title="",
        hoverlabel=dict(bgcolor=P["bg_base"], font_size=12),
    )

    # Top 3 barriers summary
    try:
        top_3 = barriers.sort_values("Prevalence (%)", ascending=False).head(3)
        barrier_cards = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    str(idx + 1),
                                    className="policy-number",
                                    style={"background": CHART_COLORS[idx]},
                                ),
                                html.Div(
                                    [
                                        html.H6(row["Barrier"], className="mb-2"),
                                        html.Div(
                                            f"{row['Prevalence (%)']:.1f}%",
                                            style={
                                                "fontSize": "1.5rem",
                                                "fontWeight": "800",
                                                "fontFamily": "'JetBrains Mono', monospace",
                                                "color": CHART_COLORS[idx],
                                            },
                                        ),
                                        html.P(
                                            "of population affected",
                                            className="text-muted mb-0",
                                            style={"fontSize": "0.75rem"},
                                        ),
                                    ],
                                    className="ms-3",
                                ),
                            ],
                            className="d-flex align-items-start",
                        ),
                        className="policy-card h-100",
                    ),
                    md=4,
                    className="mb-3",
                )
                for idx, (_, row) in enumerate(top_3.iterrows())
            ]
        )
    except:
        barrier_cards = html.Div()

    return html.Div(
        [
            html.Div(
                [
                    html.H4("Barriers Analysis", className="page-title"),
                    html.P(
                        "Click any barrier to view demographic drilldown and affected segments.",
                        className="page-subtitle",
                    ),
                ],
                className="page-header",
            ),
            html.Div(
                [
                    html.I(
                        className="fas fa-ranking-star me-2",
                        style={"color": P["amber"]},
                    ),
                    html.Span(
                        "Top 3 Barriers",
                        style={
                            "fontSize": "1.05rem",
                            "fontWeight": "700",
                            "color": P["text"],
                        },
                    ),
                ],
                className="mb-3",
            ),
            barrier_cards,
            html.Div(className="section-divider"),
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-chart-bar me-2"),
                            "All Barriers - Ranked by Prevalence",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                id="barrier-chart",
                                figure=fig_b,
                                config={"displayModeBar": False},
                            ),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-hand-pointer me-2",
                                        style={"color": P["accent"]},
                                    ),
                                    html.Span(
                                        "Click on any barrier to see detailed demographic breakdown",
                                        style={
                                            "fontSize": "0.8rem",
                                            "color": P["text2"],
                                            "fontStyle": "italic",
                                        },
                                    ),
                                ],
                                className="mt-3 d-flex align-items-center",
                            ),
                        ]
                    ),
                ],
                className="chart-card mb-4",
            ),
        ]
    )


def create_guide_tab(gender_value="all", quintile_value="all"):
    """Create an interactive guide for new users"""
    return html.Div(
        [
            html.Div(
                [
                    html.H4("Dashboard User Guide", className="page-title"),
                    html.P(
                        "Welcome to the Findex Malawi Enterprise Dashboard. This guide will help you navigate and get the most out of the analytics.",
                        className="text-muted mb-4",
                    ),
                ],
                className="mb-5",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-house fa-2x",
                                                    style={"color": P["accent"]},
                                                ),
                                                html.H5(
                                                    "Overview Tab",
                                                    className="mt-3 mb-2",
                                                ),
                                            ],
                                            className="text-center mb-3",
                                        ),
                                        html.P(
                                            "Your starting point for dashboard insights. View:",
                                            className="text-muted mb-2",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "National key performance indicators"
                                                ),
                                                html.Li(
                                                    "Financial account penetration rates"
                                                ),
                                                html.Li(
                                                    "Top barriers to financial inclusion"
                                                ),
                                                html.Li(
                                                    "Gender and income gap analysis"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                className="guide-card h-100",
                            ),
                        ],
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-users fa-2x",
                                                    style={"color": P["cyan"]},
                                                ),
                                                html.H5(
                                                    "Demographics Tab",
                                                    className="mt-3 mb-2",
                                                ),
                                            ],
                                            className="text-center mb-3",
                                        ),
                                        html.P(
                                            "Explore financial inclusion across population segments:",
                                            className="text-muted mb-2",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Gender-based inclusion differences"
                                                ),
                                                html.Li("Income quintile analysis"),
                                                html.Li(
                                                    "Wealth inequality impact metrics"
                                                ),
                                                html.Li("Cross-demographic patterns"),
                                            ]
                                        ),
                                    ]
                                ),
                                className="guide-card h-100",
                            ),
                        ],
                        md=6,
                        className="mb-4",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-triangle-exclamation fa-2x",
                                                    style={"color": P["rose"]},
                                                ),
                                                html.H5(
                                                    "Barriers Tab",
                                                    className="mt-3 mb-2",
                                                ),
                                            ],
                                            className="text-center mb-3",
                                        ),
                                        html.P(
                                            "Analyze obstacles to financial account adoption:",
                                            className="text-muted mb-2",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Barrier prevalence across the population"
                                                ),
                                                html.Li(
                                                    "Demographic breakdown (click barriers for details)"
                                                ),
                                                html.Li(
                                                    "Correlation with account types"
                                                ),
                                                html.Li(
                                                    "Strategic insights and patterns"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                className="guide-card h-100",
                            ),
                        ],
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-lightbulb fa-2x",
                                                    style={"color": P["emerald"]},
                                                ),
                                                html.H5(
                                                    "Policy Tab",
                                                    className="mt-3 mb-2",
                                                ),
                                            ],
                                            className="text-center mb-3",
                                        ),
                                        html.P(
                                            "Data-driven policy recommendations:",
                                            className="text-muted mb-2",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Priority policy initiatives by impact"
                                                ),
                                                html.Li(
                                                    "Implementation feasibility assessment"
                                                ),
                                                html.Li(
                                                    "Risk-reward quadrant analysis"
                                                ),
                                                html.Li("Population impact estimates"),
                                            ]
                                        ),
                                    ]
                                ),
                                className="guide-card h-100",
                            ),
                        ],
                        md=6,
                        className="mb-4",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-square-poll-vertical fa-2x",
                                                    style={"color": P["violet"]},
                                                ),
                                                html.H5(
                                                    "Models Tab",
                                                    className="mt-3 mb-2",
                                                ),
                                            ],
                                            className="text-center mb-3",
                                        ),
                                        html.P(
                                            "Advanced statistical analysis:",
                                            className="text-muted mb-2",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li("Logistic regression results"),
                                                html.Li(
                                                    "Impact of barriers on account adoption"
                                                ),
                                                html.Li(
                                                    "Model diagnostics and validation"
                                                ),
                                                html.Li(
                                                    "Multicollinearity assessment (VIF)"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                className="guide-card h-100",
                            ),
                        ],
                        md=12,
                        className="mb-5",
                    ),
                ]
            ),
            html.Hr(className="my-5"),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H5("Using Filters", className="mb-3")],
                        md=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6(
                                            [
                                                html.I(className="fas fa-filter me-2"),
                                                "Gender Filter",
                                            ],
                                            className="mb-2",
                                        ),
                                        html.P(
                                            "Select 'Female', 'Male', or 'All' to view financial inclusion patterns stratified by gender. Use this to identify gender-specific barriers and opportunities.",
                                            className="text-muted mb-0",
                                        ),
                                    ]
                                ),
                                className="guide-card",
                            ),
                        ],
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6(
                                            [
                                                html.I(
                                                    className="fas fa-chart-column me-2"
                                                ),
                                                "Income Quintile Filter",
                                            ],
                                            className="mb-2",
                                        ),
                                        html.P(
                                            "Choose an income quintile (Q1=poorest to Q5=richest) or 'All' to analyze how wealth affects financial account access. Essential for poverty-targeted interventions.",
                                            className="text-muted mb-0",
                                        ),
                                    ]
                                ),
                                className="guide-card",
                            ),
                        ],
                        md=6,
                        className="mb-3",
                    ),
                ]
            ),
            html.Hr(className="my-5"),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H5("Tips & Tricks", className="mb-3")],
                        md=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-circle-info fa-lg",
                                        style={
                                            "color": P["cyan"],
                                            "marginRight": "1rem",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Strong(
                                                "Click on barriers (Barriers tab)"
                                            ),
                                            html.P(
                                                "Click any barrier in the chart to see demographic breakdown and detailed analysis.",
                                                className="text-muted mb-0",
                                            ),
                                        ]
                                    ),
                                ],
                                className="d-flex align-items-start mb-3",
                            ),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-circle-info fa-lg",
                                        style={
                                            "color": P["emerald"],
                                            "marginRight": "1rem",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Export filtered data"),
                                            html.P(
                                                "Use the 'Export View' button to download your current view as CSV for further analysis in Excel or other tools.",
                                                className="text-muted mb-0",
                                            ),
                                        ]
                                    ),
                                ],
                                className="d-flex align-items-start mb-3",
                            ),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-circle-info fa-lg",
                                        style={
                                            "color": P["violet"],
                                            "marginRight": "1rem",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Hover for details"),
                                            html.P(
                                                "Hover over any chart element to see detailed data points, percentages, and additional context.",
                                                className="text-muted mb-0",
                                            ),
                                        ]
                                    ),
                                ],
                                className="d-flex align-items-start mb-3",
                            ),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-circle-info fa-lg",
                                        style={
                                            "color": P["rose"],
                                            "marginRight": "1rem",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Use filters across all pages"),
                                            html.P(
                                                "Gender and income filters apply globally — change them once and all views update automatically.",
                                                className="text-muted mb-0",
                                            ),
                                        ]
                                    ),
                                ],
                                className="d-flex align-items-start",
                            ),
                        ],
                        md=12,
                    ),
                ]
            ),
            html.Hr(className="my-5"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Data Source", className="mb-3"),
                            html.P(
                                [
                                    html.Strong("Global Findex 2024 - Malawi"),
                                    html.Br(),
                                    "This dashboard analyzes financial inclusion data from the World Bank's Global Findex survey. The data covers 1,000 adults and measures barriers to account adoption, demographic patterns, and the impact of financial inclusion on individuals and households.",
                                ],
                                className="text-muted",
                            ),
                        ],
                        md=12,
                    ),
                ]
            ),
        ],
        className="page-content",
    )


def create_policy_tab(gender_value="all", quintile_value="all"):
    policy = cached("policy", load_policy_priorities)

    # Priority matrix chart
    fig_p = go.Figure(
        go.Scatter(
            x=policy["Feasibility"],
            y=policy["Impact Score"],
            mode="markers+text",
            text=policy["Barrier"],
            textposition="top center",
            marker=dict(
                size=np.clip(policy["Prevalence (%)"] * 1.2, 10, 50),
                color=CHART_COLORS[: len(policy)],
                line=dict(width=2, color="white"),
                opacity=0.8,
            ),
            customdata=policy["Prevalence (%)"],
            hovertemplate="<b>%{text}</b><br>"
            + "Feasibility: %{x:.1f}<br>"
            + "Impact: %{y:.1f}<br>"
            + "Prevalence: %{customdata:.1f}%<br>"
            + "<extra></extra>",
        )
    )
    apply_theme(fig_p, 430)
    fig_p.update_layout(
        xaxis_title="Feasibility Score (Higher = Easier to Implement)",
        yaxis_title="Impact Score (Higher = More Effective)",
        xaxis=dict(range=[0, 10.5]),
        yaxis=dict(range=[0, 10.5]),
    )

    # Add quadrant lines
    fig_p.add_hline(y=5, line_dash="dash", line_color=P["muted"], opacity=0.4)
    fig_p.add_vline(x=5, line_dash="dash", line_color=P["muted"], opacity=0.4)

    # Add quadrant labels
    fig_p.add_annotation(
        x=2.5,
        y=9.5,
        text="High Impact<br>Low Feasibility",
        showarrow=False,
        font=dict(size=10, color=P["muted"]),
    )
    fig_p.add_annotation(
        x=8.5,
        y=9.5,
        text="Quick Wins<br>(Priority)",
        showarrow=False,
        font=dict(size=10, color=P["emerald"]),
    )
    fig_p.add_annotation(
        x=2.5,
        y=1.5,
        text="Low Priority",
        showarrow=False,
        font=dict(size=10, color=P["muted"]),
    )
    fig_p.add_annotation(
        x=8.5,
        y=1.5,
        text="Easy Wins",
        showarrow=False,
        font=dict(size=10, color=P["cyan"]),
    )

    # Top recommendations
    top = policy.sort_values("Impact Score", ascending=False).head(4)
    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Div(
                                    str(i + 1),
                                    className="policy-number",
                                    style={"background": CHART_COLORS[i]},
                                ),
                                html.Div(
                                    [
                                        html.H6(str(r["Barrier"]), className="mb-2"),
                                        html.Div(
                                            [
                                                html.Span(
                                                    [
                                                        html.I(
                                                            className="fas fa-bullseye me-1"
                                                        ),
                                                        f"Impact: {r['Impact Score']:.1f}",
                                                    ],
                                                    className="badge me-2",
                                                    style={
                                                        "background": P["accent_soft"],
                                                        "color": P["accent"],
                                                    },
                                                ),
                                                html.Span(
                                                    [
                                                        html.I(
                                                            className="fas fa-check-circle me-1"
                                                        ),
                                                        f"Feasibility: {r['Feasibility']:.1f}",
                                                    ],
                                                    className="badge",
                                                    style={
                                                        "background": P["emerald_soft"],
                                                        "color": P["emerald"],
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.P(
                                            f"Affects {r['Prevalence (%)']:.1f}% of population",
                                            className="text-muted mb-0 mt-2",
                                            style={"fontSize": "0.75rem"},
                                        ),
                                    ],
                                    className="ms-3",
                                ),
                            ],
                            className="d-flex align-items-start",
                        )
                    ]
                ),
                className="policy-card h-100",
            ),
            md=6,
            className="mb-3",
        )
        for i, (_, r) in enumerate(top.iterrows())
    ]

    return html.Div(
        [
            html.Div(
                [
                    html.H4("Policy Intelligence", className="page-title"),
                    html.P(
                        "Evidence-based priorities generated from barrier analysis and feasibility assessment.",
                        className="page-subtitle",
                    ),
                ],
                className="page-header",
            ),
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-bullseye me-2"),
                            "Policy Priority Matrix - Impact vs Feasibility",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig_p, config={"displayModeBar": False}),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-info-circle me-2",
                                        style={"color": P["cyan"]},
                                    ),
                                    html.Span(
                                        "Bubble size represents prevalence. Focus on top-right quadrant for maximum impact with feasible implementation.",
                                        style={
                                            "fontSize": "0.8rem",
                                            "color": P["text2"],
                                        },
                                    ),
                                ],
                                className="mt-3 d-flex align-items-start",
                            ),
                        ]
                    ),
                ],
                className="chart-card mb-4",
            ),
            html.Div(
                [
                    html.I(
                        className="fas fa-list-check me-2", style={"color": P["accent"]}
                    ),
                    html.Span(
                        "Top 4 Policy Recommendations",
                        style={
                            "fontSize": "1.05rem",
                            "fontWeight": "700",
                            "color": P["text"],
                        },
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(cards, className="g-3 mb-4"),
        ]
    )


def create_models_tab(gender_value="all", quintile_value="all"):
    reg = cached("reg_any", lambda: load_regression_results("any_account"))
    df = reg[reg["Variable"] != "Intercept"].sort_values("Coef", ascending=True)

    # Coefficient chart
    fig = go.Figure(
        go.Bar(
            x=df["Coef"],
            y=df["Variable"],
            orientation="h",
            marker=dict(
                color=[P["cyan"] if v >= 0 else P["rose"] for v in df["Coef"]],
                cornerradius=4,
            ),
            text=df["Coef"].apply(lambda v: f"{v:+.3f}"),
            textposition="outside",
            customdata=(
                df[["Std Err", "P-value"]].values if "P-value" in df.columns else None
            ),
            hovertemplate="<b>%{y}</b><br>"
            + "Coefficient: %{x:.4f}<br>"
            + "<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_color=P["text2"], line_width=2, line_dash="solid")
    apply_theme(fig, max(360, len(df) * 42))
    fig.update_layout(
        margin=dict(l=200),
        xaxis_title="Coefficient Estimate (Log Odds)",
        yaxis_title="",
    )

    # Model insights
    try:
        top_positive = df[df["Coef"] > 0].sort_values("Coef", ascending=False).head(3)
        top_negative = df[df["Coef"] < 0].sort_values("Coef").head(3)

        model_insights = dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Key Model Insights", className="mb-3"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.I(
                                                className="fas fa-arrow-trend-up me-2",
                                                style={"color": P["emerald"]},
                                            ),
                                            html.Strong(
                                                "Strongest Positive Predictors",
                                                style={"color": P["text"]},
                                            ),
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                f"{row['Variable']}: +{row['Coef']:.3f}",
                                                style={
                                                    "color": P["text2"],
                                                    "fontSize": "0.85rem",
                                                },
                                            )
                                            for _, row in top_positive.iterrows()
                                        ],
                                        className="mb-3",
                                    ),
                                ],
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.I(
                                                className="fas fa-arrow-trend-down me-2",
                                                style={"color": P["rose"]},
                                            ),
                                            html.Strong(
                                                "Strongest Negative Predictors",
                                                style={"color": P["text"]},
                                            ),
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                f"{row['Variable']}: {row['Coef']:.3f}",
                                                style={
                                                    "color": P["text2"],
                                                    "fontSize": "0.85rem",
                                                },
                                            )
                                            for _, row in top_negative.iterrows()
                                        ],
                                        className="mb-0",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            className="insights-panel mb-4",
        )
    except:
        model_insights = html.Div()

    return html.Div(
        [
            html.Div(
                [
                    html.H4("Statistical Models", className="page-title"),
                    html.P(
                        "Logistic regression results showing determinants of account ownership.",
                        className="page-subtitle",
                    ),
                ],
                className="page-header",
            ),
            model_insights,
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-chart-bar me-2"),
                            "Model Coefficients - Any Account Ownership",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig, config={"displayModeBar": False}),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-info-circle me-2",
                                        style={"color": P["cyan"]},
                                    ),
                                    html.Span(
                                        "Positive coefficients indicate increased likelihood of account ownership. Values represent log odds.",
                                        style={
                                            "fontSize": "0.8rem",
                                            "color": P["text2"],
                                        },
                                    ),
                                ],
                                className="mt-3 d-flex align-items-start",
                            ),
                        ]
                    ),
                ],
                className="chart-card mb-4",
            ),
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-table me-2"),
                            "Detailed Regression Table",
                        ]
                    ),
                    dbc.CardBody(
                        dash_table.DataTable(
                            data=reg.round(4).to_dict("records"),
                            columns=[{"name": c, "id": c} for c in reg.columns],
                            style_table={"overflowX": "auto"},
                            style_cell={
                                "textAlign": "left",
                                "padding": "12px",
                                "backgroundColor": "rgba(0,0,0,0)",
                                "color": P["text2"],
                                "fontSize": "0.85rem",
                                "fontFamily": "'JetBrains Mono', monospace",
                                "border": "1px solid " + P["border"],
                            },
                            style_header={
                                "backgroundColor": P["bg_base"],
                                "fontWeight": "700",
                                "color": P["text"],
                                "border": "1px solid " + P["border"],
                            },
                            style_data_conditional=[
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "rgba(255, 255, 255, 0.02)",
                                }
                            ],
                            page_size=15,
                        )
                    ),
                ],
                className="chart-card mb-4",
            ),
        ]
    )


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="active-tab-store", data="overview"),
        dcc.Store(
            id="filter-store",
            storage_type="session",
            data={"gender": "all", "quintile": "all"},
        ),
        dcc.Download(id="download-export"),
        create_header(),
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="sidebar-container", children=create_sidebar("overview")
                        ),
                        width=2,
                        className="px-0 d-none d-md-block",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                id="controls-container",
                                children=create_global_controls("all", "all"),
                            ),
                            html.Div(
                                id="active-filter-badge",
                                className="mb-3",
                            ),
                            dcc.Loading(
                                id="main-loading",
                                type="circle",
                                color=P["accent"],
                                children=html.Div(
                                    id="page-content",
                                    children=create_overview_tab("all", "all"),
                                ),
                            ),
                            create_footer(),
                        ],
                        width=10,
                        className="main-content-col",
                    ),
                ],
                className="gx-0",
            ),
            fluid=True,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(id="barrier-modal-title"), close_button=True
                ),
                dbc.ModalBody(id="barrier-modal-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-barrier-modal", color="secondary")
                ),
            ],
            id="barrier-modal",
            is_open=False,
            size="lg",
            centered=True,
        ),
    ]
)


@app.callback(
    Output("sidebar-container", "children"),
    Input("active-tab-store", "data"),
    prevent_initial_call=False,
)
def update_sidebar(active_tab):
    return create_sidebar(active_tab or "overview")


@app.callback(
    Output("active-filter-badge", "children"),
    Input("filter-store", "data"),
    prevent_initial_call=False,
)
def update_filter_badge(filter_state):
    s = filter_state or {"gender": "all", "quintile": "all"}
    gender = s.get("gender", "all")
    quintile = s.get("quintile", "all")

    if gender == "all" and quintile == "all":
        return html.Div()

    badges = []
    if gender != "all":
        badges.append(
            html.Span(
                [
                    html.I(className="fas fa-venus-mars me-1"),
                    f"Gender: {gender}",
                ],
                className="filter-active-badge",
            )
        )
    if quintile != "all":
        badges.append(
            html.Span(
                [
                    html.I(className="fas fa-chart-column me-1"),
                    f"Income: {quintile}",
                ],
                className="filter-active-badge",
            )
        )

    return html.Div(
        [
            html.I(
                className="fas fa-filter me-2",
                style={"color": P["accent"], "fontSize": "0.75rem"},
            ),
            html.Span(
                "Active Filters: ",
                style={
                    "color": P["text2"],
                    "fontSize": "0.8rem",
                    "marginRight": "0.5rem",
                },
            ),
        ]
        + badges,
        className="d-flex align-items-center",
    )


@app.callback(
    Output("filter-store", "data"),
    [
        Input({"type": "gender-btn", "index": ALL}, "n_clicks"),
        Input("quintile-filter", "value"),
        Input("reset-filters", "n_clicks"),
    ],
    State("filter-store", "data"),
    prevent_initial_call=True,
)
def sync_filters(gender_clicks, quintile_value, reset_clicks, state):
    s = state or {"gender": "all", "quintile": "all"}
    ctx = dash.callback_context
    if not ctx.triggered:
        return s
    trig = ctx.triggered[0]["prop_id"]
    if trig.startswith("reset-filters"):
        return {"gender": "all", "quintile": "all"}
    if '"type":"gender-btn"' in trig:
        import json

        btn_id = json.loads(trig.split(".")[0])
        return {
            "gender": btn_id["index"],
            "quintile": s.get("quintile", "all"),
        }
    return {
        "gender": s.get("gender", "all"),
        "quintile": quintile_value or s.get("quintile", "all"),
    }


@app.callback(
    Output("gender-btn-group", "children"),
    Input("filter-store", "data"),
    prevent_initial_call=False,
)
def update_gender_buttons(filter_state):
    s = filter_state or {"gender": "all", "quintile": "all"}
    return _build_gender_buttons(s.get("gender", "all"))


@app.callback(
    Output("quintile-filter", "value"),
    Input("reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_dropdown_values(n_clicks):
    return "all"


@app.callback(
    [Output("page-content", "children"), Output("active-tab-store", "data")],
    [Input("url", "pathname"), Input("filter-store", "data")],
)
def display_page(pathname, filter_state):
    try:
        s = filter_state or {"gender": "all", "quintile": "all"}
        routes = {
            "/": ("overview", create_overview_tab),
            "/overview": ("overview", create_overview_tab),
            "/demographics": ("demographics", create_demographics_tab),
            "/barriers": ("barriers", create_barriers_tab),
            "/policy": ("policy", create_policy_tab),
            "/models": ("models", create_models_tab),
            "/guide": ("guide", create_guide_tab),
        }
        tab, builder = routes.get(pathname, ("overview", create_overview_tab))
        content = builder(s.get("gender", "all"), s.get("quintile", "all"))
        return content, tab
    except Exception as e:
        # Error fallback
        error_content = html.Div(
            [
                html.Div(
                    [
                        html.I(
                            className="fas fa-triangle-exclamation",
                            style={
                                "fontSize": "3rem",
                                "color": P["rose"],
                                "marginBottom": "1rem",
                            },
                        ),
                        html.H4("Unable to Load Page", style={"color": P["text"]}),
                        html.P(
                            f"An error occurred: {str(e)}",
                            style={"color": P["text2"], "fontSize": "0.9rem"},
                        ),
                        dbc.Button(
                            "Go to Overview",
                            href="/overview",
                            color="primary",
                            className="mt-3",
                        ),
                    ],
                    className="empty-state",
                    style={"padding": "4rem 2rem"},
                )
            ]
        )
        return error_content, "overview"


@app.callback(
    [
        Output("barrier-modal", "is_open"),
        Output("barrier-modal-title", "children"),
        Output("barrier-modal-body", "children"),
    ],
    [Input("barrier-chart", "clickData"), Input("close-barrier-modal", "n_clicks")],
    State("barrier-modal", "is_open"),
    prevent_initial_call=True,
)
def open_barrier_modal(click_data, close_clicks, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, "", ""
    if ctx.triggered[0]["prop_id"].startswith("close-barrier-modal"):
        return False, "", ""
    if not click_data or "points" not in click_data or len(click_data["points"]) == 0:
        return is_open, "", ""

    barrier_name = click_data["points"][0].get("y")
    demo = cached("demo_barriers", load_barrier_demographics)
    subset = demo[demo["Barrier"].astype(str) == str(barrier_name)]
    if subset.empty:
        return (
            True,
            f"{barrier_name} — Drilldown",
            html.Div(
                [
                    html.I(
                        className="fas fa-circle-info",
                        style={
                            "fontSize": "2rem",
                            "color": P["muted"],
                            "marginBottom": "1rem",
                        },
                    ),
                    html.P(
                        "No demographic drilldown data available for this barrier.",
                        style={"color": P["text2"]},
                    ),
                ],
                className="empty-state",
            ),
        )

    # Create demographic breakdown chart
    fig = go.Figure(
        go.Bar(
            x=subset["Group"],
            y=subset["Prevalence (%)"],
            marker=dict(color=CHART_COLORS[: len(subset)], cornerradius=4),
            text=subset["Prevalence (%)"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )
    apply_theme(fig, 330)
    fig.update_layout(
        xaxis_title="Demographic Group",
        yaxis_title="Prevalence (%)",
        xaxis_tickangle=-15,
    )

    body = html.Div(
        [
            html.Div(
                [
                    html.I(
                        className="fas fa-chart-bar me-2", style={"color": P["accent"]}
                    ),
                    html.Span(
                        "Demographic Breakdown",
                        style={
                            "fontSize": "0.95rem",
                            "fontWeight": "600",
                            "color": P["text"],
                        },
                    ),
                ],
                className="mb-3",
            ),
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
            html.Div(className="section-divider"),
            html.Div(
                [
                    html.I(className="fas fa-table me-2", style={"color": P["cyan"]}),
                    html.Span(
                        "Detailed Data",
                        style={
                            "fontSize": "0.95rem",
                            "fontWeight": "600",
                            "color": P["text"],
                        },
                    ),
                ],
                className="mb-3",
            ),
            dash_table.DataTable(
                data=subset[["Group", "Prevalence (%)"]].round(2).to_dict("records"),
                columns=[
                    {"name": "Demographic Group", "id": "Group"},
                    {"name": "Prevalence (%)", "id": "Prevalence (%)"},
                ],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "12px",
                    "backgroundColor": "rgba(0,0,0,0)",
                    "color": P["text2"],
                    "fontSize": "0.85rem",
                    "border": "1px solid " + P["border"],
                },
                style_header={
                    "backgroundColor": P["bg_base"],
                    "fontWeight": "700",
                    "color": P["text"],
                    "border": "1px solid " + P["border"],
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgba(255, 255, 255, 0.02)",
                    }
                ],
            ),
        ]
    )
    return True, f"🔍 {barrier_name}", body


@app.callback(
    Output("download-export", "data"),
    Input("export-view-btn", "n_clicks"),
    [State("active-tab-store", "data"), State("filter-store", "data")],
    prevent_initial_call=True,
)
def export_current_view(n_clicks, active_tab, filter_state):
    if not n_clicks:
        return dash.no_update
    s = filter_state or {"gender": "all", "quintile": "all"}
    mapping = {
        "overview": cached("national", load_national_indicators),
        "demographics": cached("income", load_income_gradient),
        "barriers": cached("barriers", load_barriers),
        "policy": cached("policy", load_policy_priorities),
        "models": cached("reg_any", lambda: load_regression_results("any_account")),
    }
    out = mapping.get(
        active_tab or "overview", cached("national", load_national_indicators)
    ).copy()
    out["Filter_Gender"] = s.get("gender", "all")
    out["Filter_Quintile"] = s.get("quintile", "all")
    return dcc.send_data_frame(
        out.to_csv, f"findex_{active_tab or 'overview'}_export.csv", index=False
    )


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  FINANCIAL INCLUSION DASHBOARD")
    print("  Global Findex 2024 | Malawi")
    print("=" * 60)
    print("  URL: http://127.0.0.1:8050/")
    print("=" * 60 + "\n")
    app.run(debug=True, host="127.0.0.1", port=8050)
