"""
Financial Inclusion in Malawi - Interactive Dashboard
Author: Brian Thuwala
Data: World Bank Global Findex 2024
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from utils import (
    load_national_indicators,
    load_gender_gap,
    load_income_gradient,
    load_education_gradient,
    load_barriers,
    load_policy_priorities,
    load_regression_results,
    get_summary_stats,
    format_percentage,
)

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Financial Inclusion in Malawi | Global Findex 2024"

# Color scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8",
    "dark": "#2c3e50",
    "light": "#ecf0f1",
    "mobile_money": "#9467bd",
    "formal_bank": "#e377c2",
}

# ============================================================================
# HEADER COMPONENT
# ============================================================================


def create_header():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.I(className="fas fa-chart-line me-2"),
                                        html.Span(
                                            "Financial Inclusion in Malawi",
                                            className="navbar-brand mb-0 h1",
                                        ),
                                    ]
                                )
                            ],
                            width="auto",
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Small(
                                    "Global Findex 2024 Analysis | n ≈ 1,000",
                                    className="text-muted",
                                )
                            ]
                        )
                    ]
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-4",
    )


# ============================================================================
# KPI CARDS
# ============================================================================


def create_kpi_card(title, value, icon, color, subtitle=None):
    """Create a KPI card component"""
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className=f"fas {icon} fa-2x",
                                        style={"color": color},
                                    ),
                                ],
                                className="col-auto",
                            ),
                            html.Div(
                                [
                                    html.H3(
                                        value, className="mb-0", style={"color": color}
                                    ),
                                    html.P(title, className="text-muted mb-0"),
                                    html.Small(
                                        subtitle if subtitle else "",
                                        className="text-muted",
                                    ),
                                ],
                                className="col",
                            ),
                        ],
                        className="row align-items-center",
                    )
                ]
            )
        ],
        className="shadow-sm h-100",
    )


def create_kpi_section():
    """Create the KPI cards section"""
    stats = get_summary_stats()

    return dbc.Row(
        [
            dbc.Col(
                [
                    create_kpi_card(
                        "Any Account",
                        format_percentage(stats["any_account"]),
                        "fa-user-check",
                        COLORS["primary"],
                        "Any financial account",
                    )
                ],
                md=4,
                sm=6,
                xs=12,
            ),
            dbc.Col(
                [
                    create_kpi_card(
                        "Mobile Money",
                        format_percentage(stats["mobile_money"]),
                        "fa-mobile-alt",
                        COLORS["mobile_money"],
                        "Dominant channel",
                    )
                ],
                md=4,
                sm=6,
                xs=12,
            ),
            dbc.Col(
                [
                    create_kpi_card(
                        "Formal Bank",
                        format_percentage(stats["formal_bank"]),
                        "fa-university",
                        COLORS["formal_bank"],
                        "Traditional banking",
                    )
                ],
                md=4,
                sm=6,
                xs=12,
            ),
        ],
        className="mb-4 g-3",
    )


# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================


def create_overview_tab():
    """Create the overview tab with national indicators and trends"""

    # Load data
    national = load_national_indicators()
    gender = load_gender_gap()

    # National indicators bar chart
    fig_national = px.bar(
        national,
        x="Indicator",
        y="Rate (%)",
        title="National Financial Inclusion Indicators",
        color="Rate (%)",
        color_continuous_scale="Blues",
        text="Rate (%)",
    )
    fig_national.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_national.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Percentage (%)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
    )

    # Gender gap chart
    gender_melted = gender.melt(
        id_vars="Indicator",
        value_vars=["Female", "Male"],
        var_name="Gender",
        value_name="Rate",
    )

    fig_gender = px.bar(
        gender_melted,
        x="Indicator",
        y="Rate",
        color="Gender",
        barmode="group",
        title="Gender Gap in Financial Inclusion",
        color_discrete_map={"Female": COLORS["danger"], "Male": COLORS["primary"]},
        text="Rate",
    )
    fig_gender.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_gender.update_layout(
        xaxis_title="",
        yaxis_title="Percentage (%)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
    )

    return html.Div(
        [
            create_kpi_section(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_national,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_gender,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ],
                        md=6,
                    ),
                ],
                className="mb-4 g-3",
            ),
            # Key insights
            dbc.Card(
                [
                    dbc.CardHeader(html.H5("Key Insights", className="mb-0")),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-mobile-alt fa-2x text-primary mb-2"
                                                    ),
                                                    html.H6("Mobile Money Dominance"),
                                                    html.P(
                                                        "Mobile money accounts (47%) far exceed formal bank accounts (12%), showing technology's role in financial inclusion.",
                                                        className="text-muted small",
                                                    ),
                                                ]
                                            )
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-venus-mars fa-2x text-danger mb-2"
                                                    ),
                                                    html.H6("Gender Gap Persists"),
                                                    html.P(
                                                        "Men are 6.2 percentage points more likely to have formal accounts, indicating persistent inequality.",
                                                        className="text-muted small",
                                                    ),
                                                ]
                                            )
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-piggy-bank fa-2x text-success mb-2"
                                                    ),
                                                    html.H6("High Borrowing Activity"),
                                                    html.P(
                                                        "76.5% borrowed from any source, showing strong demand for financial services despite low formal access.",
                                                        className="text-muted small",
                                                    ),
                                                ]
                                            )
                                        ],
                                        md=4,
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
                className="shadow-sm",
            ),
        ]
    )


# ============================================================================
# TAB 2: DEMOGRAPHICS
# ============================================================================


def create_demographics_tab():
    """Create demographics analysis tab"""

    # Load data
    income = load_income_gradient()
    education = load_education_gradient()

    # Income gradient
    fig_income = go.Figure()

    for col in ["Any Account (%)", "Mobile Money (%)", "Formal/Bank (%)"]:
        fig_income.add_trace(
            go.Scatter(
                x=income["Quintile"],
                y=income[col],
                name=col.replace(" (%)", ""),
                mode="lines+markers",
                marker=dict(size=10),
                line=dict(width=3),
            )
        )

    fig_income.update_layout(
        title="Financial Inclusion by Income Quintile",
        xaxis_title="Income Quintile",
        yaxis_title="Percentage (%)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        height=450,
    )

    # Education gradient
    fig_education = go.Figure()

    education_data = []
    # Only use columns that exist in the education data
    edu_cols = ["Any Account (%)", "Formal/Bank (%)"]
    for col in edu_cols:
        if col in education.columns:
            education_data.append(
                go.Bar(
                    name=col.replace(" (%)", ""),
                    x=education["Education"],
                    y=education[col],
                    text=education[col],
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                )
            )

    fig_education = go.Figure(data=education_data)
    fig_education.update_layout(
        title="Financial Inclusion by Education Level",
        xaxis_title="Education Level",
        yaxis_title="Percentage (%)",
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_income,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_education,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ],
                        lg=6,
                    ),
                ],
                className="mb-4 g-3",
            ),
            # Insights card
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Demographic Disparities", className="mb-0")
                    ),
                    dbc.CardBody(
                        [
                            dbc.Alert(
                                [
                                    html.I(
                                        className="fas fa-exclamation-triangle me-2"
                                    ),
                                    html.Strong("Income Inequality: "),
                                    "Richest quintile has 37pp higher formal account ownership than poorest quintile, highlighting severe financial exclusion among low-income groups.",
                                ],
                                color="warning",
                                className="mb-3",
                            ),
                            dbc.Alert(
                                [
                                    html.I(className="fas fa-graduation-cap me-2"),
                                    html.Strong("Education Gradient: "),
                                    "Tertiary-educated adults have 3x the formal account ownership of those with primary education or less.",
                                ],
                                color="info",
                            ),
                        ]
                    ),
                ],
                className="shadow-sm",
            ),
        ]
    )


# ============================================================================
# TAB 3: BARRIERS
# ============================================================================


def create_barriers_tab():
    """Create barriers analysis tab"""

    # Load data
    barriers = load_barriers()
    policy = load_policy_priorities()

    # Sort barriers by prevalence
    barriers_sorted = barriers.sort_values("Prevalence (%)", ascending=True)

    # Horizontal bar chart
    fig_barriers = go.Figure(
        go.Bar(
            x=barriers_sorted["Prevalence (%)"],
            y=barriers_sorted["Barrier"],
            orientation="h",
            text=barriers_sorted["Prevalence (%)"],
            texttemplate="%{text:.1f}%",
            textposition="outside",
            marker_color=COLORS["danger"],
        )
    )

    fig_barriers.update_layout(
        title="Prevalence of Barriers to Financial Inclusion",
        xaxis_title="Percentage of Adults (%)",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
    )

    # Policy priority matrix
    fig_policy = px.scatter(
        policy,
        x="Prevalence (%)",
        y="Impact Score",
        size="Prevalence (%)",
        color="Significant",
        text="Barrier",
        title="Policy Priority Matrix: Prevalence vs. Impact",
        color_discrete_map={True: COLORS["danger"], False: COLORS["secondary"]},
        size_max=30,
    )

    fig_policy.update_traces(textposition="top center")
    fig_policy.update_layout(
        xaxis_title="Prevalence (% of Adults)",
        yaxis_title="Impact Score",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
        showlegend=True,
    )

    # Add quadrant lines
    median_prev = policy["Prevalence (%)"].median()
    median_impact = policy["Impact Score"].median()

    fig_policy.add_hline(
        y=median_impact, line_dash="dash", line_color="gray", opacity=0.5
    )
    fig_policy.add_vline(
        x=median_prev, line_dash="dash", line_color="gray", opacity=0.5
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_barriers,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Top Barriers", className="card-title"
                                            ),
                                            html.Hr(),
                                            dbc.ListGroup(
                                                [
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Strong(
                                                                        "1. Lack of Money"
                                                                    ),
                                                                    html.Span(
                                                                        " — 35.9%",
                                                                        className="text-muted float-end",
                                                                    ),
                                                                ]
                                                            ),
                                                            html.Small(
                                                                "Most critical barrier to address",
                                                                className="text-muted",
                                                            ),
                                                        ],
                                                        color="danger",
                                                    ),
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Strong(
                                                                        "2. Documentation"
                                                                    ),
                                                                    html.Span(
                                                                        " — 15.3%",
                                                                        className="text-muted float-end",
                                                                    ),
                                                                ]
                                                            ),
                                                            html.Small(
                                                                "ID requirements limiting access",
                                                                className="text-muted",
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Strong(
                                                                        "3. Trust/Security"
                                                                    ),
                                                                    html.Span(
                                                                        " — 12.6%",
                                                                        className="text-muted float-end",
                                                                    ),
                                                                ]
                                                            ),
                                                            html.Small(
                                                                "Confidence in financial system",
                                                                className="text-muted",
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Strong(
                                                                        "4. Cost/Expense"
                                                                    ),
                                                                    html.Span(
                                                                        " — 11.9%",
                                                                        className="text-muted float-end",
                                                                    ),
                                                                ]
                                                            ),
                                                            html.Small(
                                                                "Account fees and transaction costs",
                                                                className="text-muted",
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.ListGroupItem(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Strong(
                                                                        "5. Distance/Access"
                                                                    ),
                                                                    html.Span(
                                                                        " — 6.4%",
                                                                        className="text-muted float-end",
                                                                    ),
                                                                ]
                                                            ),
                                                            html.Small(
                                                                "Geographic barriers",
                                                                className="text-muted",
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                flush=True,
                                            ),
                                        ]
                                    )
                                ],
                                className="shadow-sm h-100",
                            )
                        ],
                        lg=6,
                    ),
                ],
                className="mb-4 g-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_policy,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ]
                    )
                ],
                className="mb-4",
            ),
        ]
    )


# ============================================================================
# TAB 4: POLICY RECOMMENDATIONS
# ============================================================================


def create_policy_tab():
    """Create policy recommendations tab"""

    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="fas fa-lightbulb me-2"),
                            html.H5(
                                "Evidence-Based Policy Recommendations",
                                className="d-inline mb-0",
                            ),
                        ]
                    ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "1. Economic Empowerment Programs",
                                                        className="text-primary",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Priority: High"
                                                            ),
                                                            " | ",
                                                            html.Strong("Target: "),
                                                            "Poorest 40%",
                                                        ],
                                                        className="text-muted",
                                                    ),
                                                    html.Ul(
                                                        [
                                                            html.Li(
                                                                "Cash transfer programs to build savings capacity"
                                                            ),
                                                            html.Li(
                                                                "Income-generating activities for low-income households"
                                                            ),
                                                            html.Li(
                                                                "Digital wallets for G2P payments"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Badge(
                                                        "Addresses 35.9% barrier",
                                                        color="danger",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                className="mb-4",
                                            )
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "2. Mobile Money Expansion",
                                                        className="text-primary",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Priority: High"
                                                            ),
                                                            " | ",
                                                            html.Strong("Target: "),
                                                            "Rural & Women",
                                                        ],
                                                        className="text-muted",
                                                    ),
                                                    html.Ul(
                                                        [
                                                            html.Li(
                                                                "Leverage 47% mobile money adoption"
                                                            ),
                                                            html.Li(
                                                                "Agent network expansion in rural areas"
                                                            ),
                                                            html.Li(
                                                                "Fee reduction for basic accounts"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Badge(
                                                        "Build on success",
                                                        color="success",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                className="mb-4",
                                            )
                                        ],
                                        md=6,
                                    ),
                                ]
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "3. Simplified Documentation",
                                                        className="text-primary",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Priority: Medium"
                                                            ),
                                                            " | ",
                                                            html.Strong("Target: "),
                                                            "Undocumented adults",
                                                        ],
                                                        className="text-muted",
                                                    ),
                                                    html.Ul(
                                                        [
                                                            html.Li(
                                                                "Tiered KYC requirements for low-value accounts"
                                                            ),
                                                            html.Li(
                                                                "Digital ID integration initiatives"
                                                            ),
                                                            html.Li(
                                                                "Alternative documentation acceptance"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Badge(
                                                        "Addresses 15.3% barrier",
                                                        color="warning",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                className="mb-4",
                                            )
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "4. Financial Literacy Programs",
                                                        className="text-primary",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Priority: Medium"
                                                            ),
                                                            " | ",
                                                            html.Strong("Target: "),
                                                            "Women & Low-education",
                                                        ],
                                                        className="text-muted",
                                                    ),
                                                    html.Ul(
                                                        [
                                                            html.Li(
                                                                "Gender-specific outreach programs"
                                                            ),
                                                            html.Li(
                                                                "Trust-building campaigns"
                                                            ),
                                                            html.Li(
                                                                "Consumer protection awareness"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Badge(
                                                        "Build confidence",
                                                        color="info",
                                                        className="mb-2",
                                                    ),
                                                ],
                                                className="mb-4",
                                            )
                                        ],
                                        md=6,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                className="shadow-sm mb-4",
            ),
            # Implementation priorities
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Implementation Priority Matrix", className="mb-0")
                    ),
                    dbc.CardBody(
                        [
                            dbc.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [
                                                html.Th("Intervention"),
                                                html.Th("Target Population"),
                                                html.Th("Expected Impact"),
                                                html.Th("Timeline"),
                                                html.Th("Priority"),
                                            ]
                                        )
                                    ),
                                    html.Tbody(
                                        [
                                            html.Tr(
                                                [
                                                    html.Td("Economic empowerment"),
                                                    html.Td("Poorest 40%"),
                                                    html.Td("Very High"),
                                                    html.Td("2-3 years"),
                                                    html.Td(
                                                        dbc.Badge(
                                                            "High", color="danger"
                                                        )
                                                    ),
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Mobile money expansion"),
                                                    html.Td("Rural areas, women"),
                                                    html.Td("High"),
                                                    html.Td("1-2 years"),
                                                    html.Td(
                                                        dbc.Badge(
                                                            "High", color="danger"
                                                        )
                                                    ),
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Simplified documentation"),
                                                    html.Td("Undocumented adults"),
                                                    html.Td("Medium"),
                                                    html.Td("1 year"),
                                                    html.Td(
                                                        dbc.Badge(
                                                            "Medium", color="warning"
                                                        )
                                                    ),
                                                ]
                                            ),
                                            html.Tr(
                                                [
                                                    html.Td("Financial literacy"),
                                                    html.Td("Women, low education"),
                                                    html.Td("Medium"),
                                                    html.Td("Ongoing"),
                                                    html.Td(
                                                        dbc.Badge(
                                                            "Medium", color="warning"
                                                        )
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                                bordered=True,
                                hover=True,
                                responsive=True,
                                striped=True,
                            )
                        ]
                    ),
                ],
                className="shadow-sm",
            ),
        ]
    )


# ============================================================================
# TAB 5: STATISTICAL MODELS
# ============================================================================


def create_models_tab():
    """Create statistical models tab"""

    # Load regression results
    reg_any = load_regression_results("any_account")
    reg_formal = load_regression_results("formal_account")

    # Create coefficient comparison
    fig_coeffs = go.Figure()

    fig_coeffs.add_trace(
        go.Bar(
            name="Any Account",
            x=reg_any["Coef"],
            y=reg_any["Variable"],
            orientation="h",
            error_x=dict(type="data", array=reg_any["SE"], visible=True),
        )
    )

    fig_coeffs.add_trace(
        go.Bar(
            name="Formal Account",
            x=reg_formal["Coef"],
            y=reg_formal["Variable"],
            orientation="h",
            error_x=dict(type="data", array=reg_formal["SE"], visible=True),
        )
    )

    fig_coeffs.update_layout(
        title="Logistic Regression Coefficients with Standard Errors",
        xaxis_title="Coefficient",
        yaxis_title="",
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        height=600,
    )

    return html.Div(
        [
            dbc.Alert(
                [
                    html.I(className="fas fa-info-circle me-2"),
                    "Statistical models use survey-weighted logistic regression to identify factors associated with financial account ownership.",
                ],
                color="info",
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(
                                                figure=fig_coeffs,
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                ],
                                className="shadow-sm",
                            )
                        ]
                    )
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H5(
                                            "Model: Any Account Ownership",
                                            className="mb-0",
                                        )
                                    ),
                                    dbc.CardBody(
                                        [
                                            dbc.Table.from_dataframe(
                                                reg_any[
                                                    [
                                                        "Variable",
                                                        "Coef",
                                                        "SE",
                                                        "p-value",
                                                    ]
                                                ].round(4),
                                                striped=True,
                                                bordered=True,
                                                hover=True,
                                                responsive=True,
                                            )
                                        ]
                                    ),
                                ],
                                className="shadow-sm",
                            )
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H5(
                                            "Model: Formal Account Ownership",
                                            className="mb-0",
                                        )
                                    ),
                                    dbc.CardBody(
                                        [
                                            dbc.Table.from_dataframe(
                                                reg_formal[
                                                    [
                                                        "Variable",
                                                        "Coef",
                                                        "SE",
                                                        "p-value",
                                                    ]
                                                ].round(4),
                                                striped=True,
                                                bordered=True,
                                                hover=True,
                                                responsive=True,
                                            )
                                        ]
                                    ),
                                ],
                                className="shadow-sm",
                            )
                        ],
                        md=6,
                    ),
                ],
                className="mb-4 g-3",
            ),
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5(
                            "Key Findings from Statistical Models", className="mb-0"
                        )
                    ),
                    dbc.CardBody(
                        [
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            html.Strong("Income: "),
                                            "Strong positive association with both account types (higher income → higher likelihood)",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Education: "),
                                            "Significant predictor, especially for formal accounts",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Gender: "),
                                            "Male gender associated with higher formal account ownership",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Age: "),
                                            "Non-linear relationship, peaks in middle age",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Urban/Rural: "),
                                            "Urban residents more likely to have formal accounts",
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
                className="shadow-sm",
            ),
        ]
    )


# ============================================================================
# MAIN LAYOUT
# ============================================================================

app.layout = dbc.Container(
    [
        create_header(),
        dbc.Tabs(
            [
                dbc.Tab(
                    create_overview_tab(),
                    label="Overview",
                    tab_id="overview",
                    label_style={"cursor": "pointer"},
                ),
                dbc.Tab(
                    create_demographics_tab(),
                    label="Demographics",
                    tab_id="demographics",
                    label_style={"cursor": "pointer"},
                ),
                dbc.Tab(
                    create_barriers_tab(),
                    label="Barriers",
                    tab_id="barriers",
                    label_style={"cursor": "pointer"},
                ),
                dbc.Tab(
                    create_policy_tab(),
                    label="Policy Recommendations",
                    tab_id="policy",
                    label_style={"cursor": "pointer"},
                ),
                dbc.Tab(
                    create_models_tab(),
                    label="Statistical Models",
                    tab_id="models",
                    label_style={"cursor": "pointer"},
                ),
            ],
            id="tabs",
            active_tab="overview",
            className="mb-4",
        ),
        # Footer
        html.Hr(),
        html.Footer(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        html.I(className="fas fa-database me-2"),
                                        html.Strong("Data Source: "),
                                        "World Bank Global Findex 2024",
                                    ],
                                    className="text-muted small mb-1",
                                ),
                                html.P(
                                    [
                                        html.I(className="fas fa-user me-2"),
                                        html.Strong("Author: "),
                                        "Brian Thuwala",
                                    ],
                                    className="text-muted small mb-1",
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        html.I(className="fas fa-users me-2"),
                                        html.Strong("Sample: "),
                                        "n ≈ 1,000 adults (nationally representative)",
                                    ],
                                    className="text-muted small mb-1 text-md-end",
                                ),
                                html.P(
                                    [
                                        html.I(className="fas fa-calendar me-2"),
                                        html.Strong("Updated: "),
                                        "February 2026",
                                    ],
                                    className="text-muted small mb-1 text-md-end",
                                ),
                            ],
                            md=6,
                        ),
                    ]
                )
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
    className="px-4",
)


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Financial Inclusion Dashboard Starting...")
    print("=" * 60)
    print(f"📊 Dashboard URL: http://127.0.0.1:8050/")
    print("=" * 60 + "\n")

    app.run(debug=True, host="127.0.0.1", port=8050)
