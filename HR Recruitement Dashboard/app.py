"""
Recruitment & Hiring Analytics Dashboard
==========================================
An interactive Streamlit dashboard for HR recruitment pipeline analysis.
Run with:  streamlit run app.py
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Recruitment & Hiring Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# PASTEL COLOR PALETTE
# ============================================================================
PASTEL_BLUE = "#A8D8EA"
PASTEL_PINK = "#F8C8DC"
PASTEL_GREEN = "#B5EAD7"
PASTEL_PURPLE = "#C7B8EA"
PASTEL_ORANGE = "#FFDAC1"
PASTEL_YELLOW = "#FFF3B0"
PASTEL_TEAL = "#B2F0E8"
PASTEL_LILAC = "#E2C2FF"
PASTEL_ROSE = "#FFB7B2"
PASTEL_MINT = "#C9E4DE"

PASTEL_SEQUENCE = [
    PASTEL_BLUE, PASTEL_PINK, PASTEL_GREEN, PASTEL_PURPLE, PASTEL_ORANGE,
    PASTEL_YELLOW, PASTEL_TEAL, PASTEL_LILAC, PASTEL_ROSE, PASTEL_MINT,
]

TEXT_DARK = "#3A3A3A"
TEXT_SLATE = "#6B7785"
GRID_COLOR = "#EFEFF3"

px.defaults.color_discrete_sequence = PASTEL_SEQUENCE
px.defaults.template = "plotly_white"

CHART_LAYOUT = dict(
    font=dict(family="Poppins, Segoe UI, sans-serif", color=TEXT_DARK, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    title_font=dict(size=16, color=TEXT_DARK),
)

# ============================================================================
# CUSTOM CSS — pastel & white theme, KPI cards, button-style filters
# ============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', 'Segoe UI', sans-serif;
    }}

    .main {{
        background-color: #FFFFFF;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #FBFAFF;
        border-right: 1px solid #EFEFF5;
    }}

    /* Headline banner */
    .dash-header {{
        padding: 18px 26px;
        border-radius: 18px;
        background: linear-gradient(120deg, {PASTEL_BLUE}55, {PASTEL_PINK}55, {PASTEL_PURPLE}44);
        margin-bottom: 14px;
        border: 1px solid #F0F0F5;
    }}
    .dash-header h1 {{
        margin: 0;
        font-size: 30px;
        font-weight: 700;
        color: {TEXT_DARK};
    }}
    .dash-header p {{
        margin: 2px 0 0 0;
        color: {TEXT_SLATE};
        font-size: 14.5px;
    }}

    /* KPI cards */
    .kpi-card {{
        border-radius: 16px;
        padding: 16px 14px 14px 14px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.04);
        box-shadow: 0 2px 10px rgba(0,0,0,0.045);
        height: 108px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .kpi-value {{
        font-size: 26px;
        font-weight: 700;
        color: {TEXT_DARK};
        line-height: 1.1;
    }}
    .kpi-label {{
        font-size: 12.5px;
        font-weight: 500;
        color: {TEXT_SLATE};
        margin-top: 4px;
        letter-spacing: 0.2px;
    }}
    .kpi-sub {{
        font-size: 11px;
        color: {TEXT_SLATE};
        margin-top: 2px;
        opacity: 0.85;
    }}

    /* Section title */
    .section-title {{
        font-size: 19px;
        font-weight: 600;
        color: {TEXT_DARK};
        margin: 22px 0 8px 0;
        padding-left: 10px;
        border-left: 5px solid {PASTEL_PURPLE};
    }}

    .insight-card {{
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-left: 5px solid {PASTEL_BLUE};
        background-color: #FAFBFF;
        font-size: 14.5px;
        color: {TEXT_DARK};
        line-height: 1.5;
    }}
    .insight-card b {{ color: {TEXT_DARK}; }}

    .reco-card {{
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        background-color: #FDFCFF;
        border: 1px solid #F0EEF7;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .reco-title {{
        font-weight: 700;
        font-size: 15.5px;
        color: {TEXT_DARK};
        margin-bottom: 6px;
    }}
    .reco-label {{
        font-weight: 600;
        color: #8B7FC2;
    }}

    /* Nav radio -> pill buttons */
    div[data-testid="stRadio"] > div {{
        gap: 6px;
        flex-wrap: wrap;
    }}
    div[data-testid="stRadio"] label {{
        background-color: #F5F4FB;
        padding: 7px 16px;
        border-radius: 999px;
        border: 1px solid #ECEAF7;
        margin-right: 4px;
        transition: all 0.15s ease-in-out;
    }}
    div[data-testid="stRadio"] label:hover {{
        background-color: #EDE9FB;
    }}

    /* Sidebar section headers */
    .filter-header {{
        font-weight: 600;
        font-size: 13.5px;
        color: {TEXT_SLATE};
        margin: 14px 0 2px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    hr {{ margin: 8px 0 16px 0; border-color: #F0F0F5; }}

    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "recruitment_clean.csv"),
        os.path.join(here, "data", "recruitment_clean.csv"),
        os.path.join(here, "HR_Recruitment_Hiring_Data.xlsx"),
    ]
    df = None
    for path in candidates:
        if os.path.exists(path):
            if path.endswith(".csv"):
                df = pd.read_csv(path, parse_dates=[
                    "Application_Date", "Interview_1_Date", "Interview_2_Date",
                    "Offer_Date", "Joining_Date"
                ])
            else:
                df = pd.read_excel(path)
            break
    if df is None:
        st.error(
            "Could not find 'recruitment_clean.csv' (or the source xlsx) next to app.py. "
            "Please place the data file in the same folder as this script."
        )
        st.stop()

    # --- Cleaning (idempotent even if raw xlsx is loaded) ---
    str_cols = df.select_dtypes(include="object").columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({"nan": np.nan})

    for datecol in ["Application_Date", "Interview_1_Date", "Interview_2_Date", "Offer_Date", "Joining_Date"]:
        if datecol in df.columns:
            df[datecol] = pd.to_datetime(df[datecol], errors="coerce")

    if "Application_Month" not in df.columns:
        df["Application_Month"] = df["Application_Date"].dt.to_period("M").astype(str)
    if "Salary_Gap_GBP" not in df.columns:
        df["Salary_Gap_GBP"] = df["Offered_Salary_GBP"] - df["Expected_Salary_GBP"]
    if "Is_Hired" not in df.columns:
        df["Is_Hired"] = (df["Candidate_Status"] == "Hired").astype(int)
    if "Is_Offer_Extended" not in df.columns:
        df["Is_Offer_Extended"] = df["Offer_Status"].isin(["Accepted", "Declined"]).astype(int)
    if "Is_Offer_Declined" not in df.columns:
        df["Is_Offer_Declined"] = (df["Offer_Status"] == "Declined").astype(int)
    if "Reached_Interview1" not in df.columns:
        df["Reached_Interview1"] = df["Interview_1_Date"].notna().astype(int)
    if "Reached_Interview2" not in df.columns:
        df["Reached_Interview2"] = df["Interview_2_Date"].notna().astype(int)
    if "Passed_Screening" not in df.columns:
        df["Passed_Screening"] = (df["Screening_Result"] == "Passed").astype(int)

    return df


df_raw = load_data()

# ============================================================================
# HEADER
# ============================================================================
st.markdown(f"""
<div class="dash-header">
    <h1>Recruitment &amp; Hiring Analytics Dashboard</h1>
    <p>End-to-end view of the candidate pipeline — from application to hire — with cost, quality and diversity insights</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.markdown("## Filters")
st.sidebar.markdown("Use these to slice every chart and KPI on the dashboard.")
st.sidebar.markdown("---")

min_date = df_raw["Application_Date"].min().date()
max_date = df_raw["Application_Date"].max().date()

st.sidebar.markdown('<div class="filter-header">Quick Date Range</div>', unsafe_allow_html=True)
date_preset = st.sidebar.radio(
    "Date preset",
    options=["All Time", "Last 3 Months", "Last 6 Months", "Last 12 Months", "Custom"],
    index=0,
    label_visibility="collapsed",
    horizontal=True,
)

if date_preset == "All Time":
    date_range = (min_date, max_date)
elif date_preset == "Last 3 Months":
    date_range = (max(min_date, max_date - pd.Timedelta(days=90)), max_date)
elif date_preset == "Last 6 Months":
    date_range = (max(min_date, max_date - pd.Timedelta(days=182)), max_date)
elif date_preset == "Last 12 Months":
    date_range = (max(min_date, max_date - pd.Timedelta(days=365)), max_date)
else:
    date_range = st.sidebar.date_input(
        "Custom range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        date_range = date_range
    else:
        date_range = (min_date, max_date)

st.sidebar.markdown('<div class="filter-header">Candidate Outcome</div>', unsafe_allow_html=True)
outcome_filter = st.sidebar.radio(
    "Outcome",
    options=["All", "Hired", "Offer Declined", "Rejected", "In Pipeline"],
    index=0,
    label_visibility="collapsed",
    horizontal=True,
)


def multiselect_filter(label, col):
    options = sorted(df_raw[col].dropna().unique().tolist())
    st.sidebar.markdown(f'<div class="filter-header">{label}</div>', unsafe_allow_html=True)
    selected = st.sidebar.multiselect(label, options=options, default=[], label_visibility="collapsed",
                                       placeholder="All included")
    return selected if selected else options


sel_department = multiselect_filter("Department", "Department")
sel_location = multiselect_filter("Location", "Location")
sel_source = multiselect_filter("Recruitment Source", "Recruitment_Source")
sel_role = multiselect_filter("Job Role", "Job_Role")
sel_recruiter = multiselect_filter("Recruiter", "Recruiter")
sel_gender = multiselect_filter("Gender", "Gender")
sel_education = multiselect_filter("Education Level", "Education_Level")

st.sidebar.markdown("---")
if st.sidebar.button("Reset all filters", use_container_width=True):
    st.rerun()

# ============================================================================
# APPLY FILTERS
# ============================================================================
mask = (
    (df_raw["Application_Date"].dt.date >= date_range[0])
    & (df_raw["Application_Date"].dt.date <= date_range[1])
    & (df_raw["Department"].isin(sel_department))
    & (df_raw["Location"].isin(sel_location))
    & (df_raw["Recruitment_Source"].isin(sel_source))
    & (df_raw["Job_Role"].isin(sel_role))
    & (df_raw["Recruiter"].isin(sel_recruiter))
    & (df_raw["Gender"].isin(sel_gender))
    & (df_raw["Education_Level"].isin(sel_education))
)
df = df_raw[mask].copy()

if outcome_filter == "Hired":
    df = df[df["Candidate_Status"] == "Hired"]
elif outcome_filter == "Offer Declined":
    df = df[df["Candidate_Status"] == "Offer Declined"]
elif outcome_filter == "Rejected":
    df = df[df["Candidate_Status"].isin(
        ["Rejected - Screening", "Rejected - Interview/Assessment", "Rejected - Final Interview"]
    )]
elif outcome_filter == "In Pipeline":
    df = df[df["Offer_Status"] == "Not Reached"]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(df):,}** of {len(df_raw):,} total candidate records")

if len(df) == 0:
    st.warning("No records match the current filter selection. Try widening your filters.")
    st.stop()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def kpi_card(col, label, value, sub="", color=PASTEL_BLUE):
    col.markdown(f"""
    <div class="kpi-card" style="background-color:{color}33; border-top: 4px solid {color};">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {f'<div class="kpi-sub">{sub}</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def fmt_pct(n, d):
    return f"{(n / d * 100):.1f}%" if d else "—"


def fmt_gbp(v):
    if v >= 1_000_000:
        return f"£{v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"£{v/1_000:.1f}K"
    return f"£{v:,.0f}"


def apply_chart_style(fig, height=380):
    fig.update_layout(**CHART_LAYOUT, height=height)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
    return fig


def funnel_counts(data):
    return {
        "Applied": len(data),
        "Screening Passed": int(data["Passed_Screening"].sum()),
        "Interview 1": int(data["Reached_Interview1"].sum()),
        "Interview 2 (Final)": int(data["Reached_Interview2"].sum()),
        "Offer Extended": int(data["Is_Offer_Extended"].sum()),
        "Hired": int(data["Is_Hired"].sum()),
    }


# ============================================================================
# NAVIGATION
# ============================================================================
PAGES = [
    "Overview",
    "Recruitment Funnel",
    "Source & Cost",
    "Diversity",
    "Recruiter Performance",
    "Quality of Hire",
    "Insights & Recommendations",
]
page = st.radio("Navigate", PAGES, horizontal=True, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)


# ============================================================================
# PAGE 1 — OVERVIEW
# ============================================================================
if page == "Overview":
    total_applied = len(df)
    total_hired = int(df["Is_Hired"].sum())
    conv_rate = fmt_pct(total_hired, total_applied)
    avg_days = df["Days_to_Hire"].mean()
    total_cost = df["Hiring_Cost_GBP"].sum()
    open_reqs = df["Requisition_ID"].nunique()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "Total Applications", f"{total_applied:,}", color=PASTEL_BLUE)
    kpi_card(c2, "Total Hires", f"{total_hired:,}", color=PASTEL_PINK)
    kpi_card(c3, "Conversion Rate", conv_rate, "Applied → Hired", color=PASTEL_GREEN)
    kpi_card(c4, "Avg Days to Hire", f"{avg_days:.1f}" if pd.notna(avg_days) else "—", color=PASTEL_PURPLE)
    kpi_card(c5, "Total Hiring Cost", fmt_gbp(total_cost), color=PASTEL_ORANGE)
    kpi_card(c6, "Open Requisitions", f"{open_reqs:,}", color=PASTEL_TEAL)

    section_title("Application & Hiring Trend")
    monthly = df.groupby("Application_Month").agg(
        Applications=("Candidate_ID", "count"), Hires=("Is_Hired", "sum")
    ).reset_index().sort_values("Application_Month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Application_Month"], y=monthly["Applications"],
                              name="Applications", mode="lines+markers",
                              line=dict(color=PASTEL_BLUE, width=3), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=monthly["Application_Month"], y=monthly["Hires"],
                              name="Hires", mode="lines+markers",
                              line=dict(color=PASTEL_PINK, width=3), marker=dict(size=6), yaxis="y2"))
    fig.update_layout(
        yaxis=dict(title="Applications", showgrid=True, gridcolor=GRID_COLOR),
        yaxis2=dict(title="Hires", overlaying="y", side="right", showgrid=False),
    )
    st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        section_title("Applications by Department")
        dep = df.groupby("Department").size().reset_index(name="Applications").sort_values("Applications")
        fig = px.bar(dep, x="Applications", y="Department", orientation="h",
                     color="Department", text="Applications")
        fig.update_traces(textposition="outside", showlegend=False)
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    with colB:
        section_title("Applications by Recruitment Source")
        src = df.groupby("Recruitment_Source").size().reset_index(name="Applications")
        fig = px.pie(src, names="Recruitment_Source", values="Applications", hole=0.5)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    colC, colD = st.columns(2)
    with colC:
        section_title("Candidate Status Breakdown")
        status = df.groupby("Candidate_Status").size().reset_index(name="Count").sort_values("Count")
        fig = px.bar(status, x="Count", y="Candidate_Status", orientation="h",
                     color="Candidate_Status", text="Count")
        fig.update_traces(textposition="outside", showlegend=False)
        st.plotly_chart(apply_chart_style(fig, 360), use_container_width=True)

    with colD:
        section_title("Applications by Location")
        loc = df.groupby("Location").size().reset_index(name="Applications").sort_values("Applications")
        fig = px.bar(loc, x="Applications", y="Location", orientation="h",
                     color="Location", text="Applications")
        fig.update_traces(textposition="outside", showlegend=False)
        st.plotly_chart(apply_chart_style(fig, 360), use_container_width=True)


# ============================================================================
# PAGE 2 — RECRUITMENT FUNNEL
# ============================================================================
elif page == "Recruitment Funnel":
    counts = funnel_counts(df)
    stages = list(counts.keys())
    values = list(counts.values())

    screening_rate = fmt_pct(counts["Screening Passed"], counts["Applied"])
    i1_i2_rate = fmt_pct(counts["Interview 2 (Final)"], counts["Interview 1"]) if counts["Interview 1"] else "—"
    i2_offer_rate = fmt_pct(counts["Offer Extended"], counts["Interview 2 (Final)"]) if counts["Interview 2 (Final)"] else "—"
    offer_accept_rate = fmt_pct(counts["Hired"], counts["Offer Extended"]) if counts["Offer Extended"] else "—"
    overall_rate = fmt_pct(counts["Hired"], counts["Applied"])

    drop_offs = {
        "Screening": counts["Applied"] - counts["Screening Passed"],
        "Interview 1→2": counts["Interview 1"] - counts["Interview 2 (Final)"],
        "Final Interview→Offer": counts["Interview 2 (Final)"] - counts["Offer Extended"],
        "Offer Declined": counts["Offer Extended"] - counts["Hired"],
    }
    biggest_drop = max(drop_offs, key=drop_offs.get)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "Screening Pass Rate", screening_rate, color=PASTEL_BLUE)
    kpi_card(c2, "Interview 1 → 2 Rate", i1_i2_rate, color=PASTEL_GREEN)
    kpi_card(c3, "Final → Offer Rate", i2_offer_rate, color=PASTEL_ORANGE)
    kpi_card(c4, "Offer Accept Rate", offer_accept_rate, color=PASTEL_PINK)
    kpi_card(c5, "Overall Conversion", overall_rate, "Applied → Hired", color=PASTEL_PURPLE)
    kpi_card(c6, "Biggest Drop-off", biggest_drop, f"{drop_offs[biggest_drop]:,} lost", color=PASTEL_ROSE)

    section_title("Recruitment Funnel")
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textposition="inside", textinfo="value+percent initial",
        marker=dict(color=[PASTEL_BLUE, PASTEL_TEAL, PASTEL_GREEN, PASTEL_YELLOW, PASTEL_ORANGE, PASTEL_PINK]),
        connector=dict(line=dict(color=GRID_COLOR, width=2)),
    ))
    st.plotly_chart(apply_chart_style(fig, 430), use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        section_title("Drop-off Volume by Stage")
        drop_df = pd.DataFrame({"Stage": list(drop_offs.keys()), "Lost Candidates": list(drop_offs.values())})
        fig = px.bar(drop_df, x="Stage", y="Lost Candidates", color="Stage", text="Lost Candidates")
        fig.update_traces(textposition="outside", showlegend=False)
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    with colB:
        section_title("Conversion Rate by Department")
        dep_funnel = df.groupby("Department").agg(
            Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum")
        ).reset_index()
        dep_funnel["Conversion Rate (%)"] = (dep_funnel["Hired"] / dep_funnel["Applied"] * 100).round(1)
        dep_funnel = dep_funnel.sort_values("Conversion Rate (%)")
        fig = px.bar(dep_funnel, x="Conversion Rate (%)", y="Department", orientation="h",
                     color="Department", text="Conversion Rate (%)")
        fig.update_traces(textposition="outside", showlegend=False)
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    section_title("Funnel Stage Volumes by Job Role (Top 10 by Applications)")
    top_roles = df["Job_Role"].value_counts().head(10).index.tolist()
    role_funnel = df[df["Job_Role"].isin(top_roles)].groupby("Job_Role").agg(
        Applied=("Candidate_ID", "count"),
        Screened=("Passed_Screening", "sum"),
        Interviewed=("Reached_Interview2", "sum"),
        Offered=("Is_Offer_Extended", "sum"),
        Hired=("Is_Hired", "sum"),
    ).reset_index().sort_values("Applied", ascending=True)
    fig = go.Figure()
    for stage_name, color in zip(
        ["Applied", "Screened", "Interviewed", "Offered", "Hired"],
        [PASTEL_BLUE, PASTEL_TEAL, PASTEL_GREEN, PASTEL_ORANGE, PASTEL_PINK],
    ):
        fig.add_trace(go.Bar(y=role_funnel["Job_Role"], x=role_funnel[stage_name], name=stage_name,
                              orientation="h", marker_color=color))
    fig.update_layout(barmode="group")
    st.plotly_chart(apply_chart_style(fig, 460), use_container_width=True)


# ============================================================================
# PAGE 3 — SOURCE & COST
# ============================================================================
elif page == "Source & Cost":
    src_stats = df.groupby("Recruitment_Source").agg(
        Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum"), Cost=("Hiring_Cost_GBP", "sum")
    ).reset_index()
    src_stats["ConvRate"] = (src_stats["Hired"] / src_stats["Applied"] * 100).round(1)
    src_stats["CostPerHire"] = np.where(src_stats["Hired"] > 0, src_stats["Cost"] / src_stats["Hired"], np.nan)

    total_cost = df["Hiring_Cost_GBP"].sum()
    total_hired = int(df["Is_Hired"].sum())
    cost_per_hire = total_cost / total_hired if total_hired else np.nan
    best_source = src_stats.loc[src_stats["ConvRate"].idxmax(), "Recruitment_Source"] if len(src_stats) else "—"
    cheapest_source = src_stats.dropna(subset=["CostPerHire"])
    cheapest_source = cheapest_source.loc[cheapest_source["CostPerHire"].idxmin(), "Recruitment_Source"] if len(cheapest_source) else "—"
    avg_cost_per_app = df["Hiring_Cost_GBP"].sum() / len(df) if len(df) else np.nan

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Total Hiring Cost", fmt_gbp(total_cost), color=PASTEL_BLUE)
    kpi_card(c2, "Cost per Hire", fmt_gbp(cost_per_hire) if pd.notna(cost_per_hire) else "—", color=PASTEL_PINK)
    kpi_card(c3, "Best Converting Source", best_source, color=PASTEL_GREEN)
    kpi_card(c4, "Most Cost-Efficient", cheapest_source, color=PASTEL_ORANGE)
    kpi_card(c5, "Avg Cost / Application", fmt_gbp(avg_cost_per_app) if pd.notna(avg_cost_per_app) else "—", color=PASTEL_PURPLE)

    colA, colB = st.columns(2)
    with colA:
        section_title("Conversion Rate by Source")
        s = src_stats.sort_values("ConvRate")
        fig = px.bar(s, x="ConvRate", y="Recruitment_Source", orientation="h",
                     color="Recruitment_Source", text="ConvRate")
        fig.update_traces(texttemplate="%{text}%", textposition="outside", showlegend=False)
        fig.update_layout(xaxis_title="Conversion Rate (%)", yaxis_title="")
        st.plotly_chart(apply_chart_style(fig, 400), use_container_width=True)

    with colB:
        section_title("Cost per Hire by Source")
        s2 = src_stats.dropna(subset=["CostPerHire"]).sort_values("CostPerHire")
        fig = px.bar(s2, x="CostPerHire", y="Recruitment_Source", orientation="h",
                     color="Recruitment_Source", text="CostPerHire")
        fig.update_traces(texttemplate="£%{text:.0f}", textposition="outside", showlegend=False)
        fig.update_layout(xaxis_title="Cost per Hire (£)", yaxis_title="")
        st.plotly_chart(apply_chart_style(fig, 400), use_container_width=True)

    section_title("Source Efficiency Map — Applications vs Hires (bubble size = total cost)")
    fig = px.scatter(
        src_stats, x="Applied", y="Hired", size="Cost", color="Recruitment_Source",
        size_max=55, hover_name="Recruitment_Source",
        hover_data={"ConvRate": True, "CostPerHire": ":.0f", "Applied": True, "Hired": True, "Cost": False},
    )
    st.plotly_chart(apply_chart_style(fig, 420), use_container_width=True)

    section_title("Funnel Stage Volumes by Source")
    src_funnel = df.groupby("Recruitment_Source").agg(
        Applied=("Candidate_ID", "count"),
        Screened=("Passed_Screening", "sum"),
        Interviewed=("Reached_Interview2", "sum"),
        Offered=("Is_Offer_Extended", "sum"),
        Hired=("Is_Hired", "sum"),
    ).reset_index().sort_values("Applied", ascending=True)
    fig = go.Figure()
    for stage_name, color in zip(
        ["Applied", "Screened", "Interviewed", "Offered", "Hired"],
        [PASTEL_BLUE, PASTEL_TEAL, PASTEL_GREEN, PASTEL_ORANGE, PASTEL_PINK],
    ):
        fig.add_trace(go.Bar(y=src_funnel["Recruitment_Source"], x=src_funnel[stage_name],
                              name=stage_name, orientation="h", marker_color=color))
    fig.update_layout(barmode="group")
    st.plotly_chart(apply_chart_style(fig, 420), use_container_width=True)


# ============================================================================
# PAGE 4 — DIVERSITY
# ============================================================================
elif page == "Diversity":
    gender_stats = df.groupby("Gender").agg(Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum")).reset_index()
    female_pct = fmt_pct(gender_stats.loc[gender_stats["Gender"] == "Female", "Applied"].sum(), len(df))
    male_pct = fmt_pct(gender_stats.loc[gender_stats["Gender"] == "Male", "Applied"].sum(), len(df))
    avg_age = df["Age"].mean()
    avg_exp = df["Experience_Years"].mean()
    n_education = df["Education_Level"].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Female Applicants", female_pct, color=PASTEL_PINK)
    kpi_card(c2, "Male Applicants", male_pct, color=PASTEL_BLUE)
    kpi_card(c3, "Avg. Age", f"{avg_age:.1f} yrs" if pd.notna(avg_age) else "—", color=PASTEL_GREEN)
    kpi_card(c4, "Avg. Experience", f"{avg_exp:.1f} yrs" if pd.notna(avg_exp) else "—", color=PASTEL_PURPLE)
    kpi_card(c5, "Education Levels", f"{n_education}", color=PASTEL_ORANGE)

    colA, colB = st.columns(2)
    with colA:
        section_title("Applicant Pool by Gender")
        fig = px.pie(gender_stats, names="Gender", values="Applied", hole=0.5)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    with colB:
        section_title("Conversion Rate by Gender")
        gender_stats["ConvRate"] = (gender_stats["Hired"] / gender_stats["Applied"] * 100).round(1)
        gs = gender_stats.sort_values("ConvRate")
        fig = px.bar(gs, x="ConvRate", y="Gender", orientation="h", color="Gender", text="ConvRate")
        fig.update_traces(texttemplate="%{text}%", textposition="outside", showlegend=False)
        fig.update_layout(xaxis_title="Conversion Rate (%)")
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    colC, colD = st.columns(2)
    with colC:
        section_title("Age Distribution")
        fig = px.histogram(df, x="Age", nbins=20, color_discrete_sequence=[PASTEL_TEAL])
        fig.update_layout(yaxis_title="Candidates")
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    with colD:
        section_title("Experience (Years) — Hired vs Not Hired")
        d = df.copy()
        d["Outcome"] = np.where(d["Is_Hired"] == 1, "Hired", "Not Hired")
        fig = px.box(d, x="Outcome", y="Experience_Years", color="Outcome",
                     color_discrete_map={"Hired": PASTEL_GREEN, "Not Hired": PASTEL_ROSE})
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    section_title("Conversion Rate by Education Level")
    edu = df.groupby("Education_Level").agg(Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum")).reset_index()
    edu["ConvRate"] = (edu["Hired"] / edu["Applied"] * 100).round(1)
    edu = edu.sort_values("ConvRate")
    fig = px.bar(edu, x="ConvRate", y="Education_Level", orientation="h", color="Education_Level", text="ConvRate")
    fig.update_traces(texttemplate="%{text}%", textposition="outside", showlegend=False)
    fig.update_layout(xaxis_title="Conversion Rate (%)")
    st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)


# ============================================================================
# PAGE 5 — RECRUITER PERFORMANCE
# ============================================================================
elif page == "Recruiter Performance":
    rec_stats = df.groupby("Recruiter").agg(
        Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum"), AvgDays=("Days_to_Hire", "mean")
    ).reset_index()
    rec_stats["ConvRate"] = (rec_stats["Hired"] / rec_stats["Applied"] * 100).round(1)

    top_recruiter = rec_stats.loc[rec_stats["ConvRate"].idxmax(), "Recruiter"] if len(rec_stats) else "—"
    fastest_recruiter = rec_stats.dropna(subset=["AvgDays"])
    fastest_recruiter = fastest_recruiter.loc[fastest_recruiter["AvgDays"].idxmin(), "Recruiter"] if len(fastest_recruiter) else "—"
    n_recruiters = df["Recruiter"].nunique()
    avg_conv_across = rec_stats["ConvRate"].mean()
    total_handled = len(df)

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Top Converting Recruiter", top_recruiter, color=PASTEL_PINK)
    kpi_card(c2, "Fastest Recruiter", fastest_recruiter, color=PASTEL_GREEN)
    kpi_card(c3, "Active Recruiters", f"{n_recruiters}", color=PASTEL_BLUE)
    kpi_card(c4, "Avg Conversion Rate", f"{avg_conv_across:.1f}%" if pd.notna(avg_conv_across) else "—", color=PASTEL_PURPLE)
    kpi_card(c5, "Total Candidates Handled", f"{total_handled:,}", color=PASTEL_ORANGE)

    colA, colB = st.columns(2)
    with colA:
        section_title("Applications vs Hires by Recruiter")
        r = rec_stats.sort_values("Applied", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=r["Recruiter"], x=r["Applied"], name="Applied", orientation="h", marker_color=PASTEL_BLUE))
        fig.add_trace(go.Bar(y=r["Recruiter"], x=r["Hired"], name="Hired", orientation="h", marker_color=PASTEL_PINK))
        fig.update_layout(barmode="group")
        st.plotly_chart(apply_chart_style(fig, 400), use_container_width=True)

    with colB:
        section_title("Conversion Rate by Recruiter")
        r2 = rec_stats.sort_values("ConvRate")
        fig = px.bar(r2, x="ConvRate", y="Recruiter", orientation="h", color="Recruiter", text="ConvRate")
        fig.update_traces(texttemplate="%{text}%", textposition="outside", showlegend=False)
        fig.update_layout(xaxis_title="Conversion Rate (%)")
        st.plotly_chart(apply_chart_style(fig, 400), use_container_width=True)

    section_title("Average Days to Hire by Recruiter")
    r3 = rec_stats.dropna(subset=["AvgDays"]).sort_values("AvgDays")
    fig = px.bar(r3, x="AvgDays", y="Recruiter", orientation="h", color="Recruiter", text="AvgDays")
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", showlegend=False)
    fig.update_layout(xaxis_title="Average Days to Hire")
    st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)

    section_title("Recruiter Summary Table")
    display_tbl = rec_stats.rename(columns={
        "Applied": "Applications", "Hired": "Hires", "AvgDays": "Avg. Days to Hire", "ConvRate": "Conversion Rate (%)"
    }).sort_values("Conversion Rate (%)", ascending=False)
    st.dataframe(display_tbl, use_container_width=True, hide_index=True)


# ============================================================================
# PAGE 6 — QUALITY OF HIRE
# ============================================================================
elif page == "Quality of Hire":
    avg_i1 = df["Interview_1_Score"].mean()
    avg_assess = df["Assessment_Score"].mean()
    avg_i2 = df["Interview_2_Score"].mean()
    offered = int(df["Is_Offer_Extended"].sum())
    hired = int(df["Is_Hired"].sum())
    accept_rate = fmt_pct(hired, offered) if offered else "—"
    prob = df["Probation_Status"].value_counts()
    prob_total = prob.sum()
    prob_pass_rate = fmt_pct(prob.get("Passed", 0), prob_total) if prob_total else "—"

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Avg Interview 1 Score", f"{avg_i1:.1f}" if pd.notna(avg_i1) else "—", color=PASTEL_BLUE)
    kpi_card(c2, "Avg Assessment Score", f"{avg_assess:.1f}" if pd.notna(avg_assess) else "—", color=PASTEL_TEAL)
    kpi_card(c3, "Avg Final Interview Score", f"{avg_i2:.1f}" if pd.notna(avg_i2) else "—", color=PASTEL_GREEN)
    kpi_card(c4, "Offer Acceptance Rate", accept_rate, color=PASTEL_PINK)
    kpi_card(c5, "Probation Pass Rate", prob_pass_rate, f"of {int(prob_total)} completed/in-progress", color=PASTEL_PURPLE)

    section_title("Average Assessment Scores — Hired vs Not Hired")
    d = df.copy()
    d["Outcome"] = np.where(d["Is_Hired"] == 1, "Hired", "Not Hired")
    score_data = []
    for label, col in [("Interview 1", "Interview_1_Score"), ("Assessment", "Assessment_Score"), ("Final Interview", "Interview_2_Score")]:
        for outcome in ["Hired", "Not Hired"]:
            val = d.loc[d["Outcome"] == outcome, col].mean()
            score_data.append({"Stage": label, "Outcome": outcome, "Avg Score": val})
    score_df = pd.DataFrame(score_data)
    fig = px.bar(score_df, x="Stage", y="Avg Score", color="Outcome", barmode="group",
                 color_discrete_map={"Hired": PASTEL_GREEN, "Not Hired": PASTEL_ROSE}, text="Avg Score")
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    st.plotly_chart(apply_chart_style(fig, 400), use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        section_title("Salary Gap: Accepted vs Declined Offers")
        offer_df = df[df["Offer_Status"].isin(["Accepted", "Declined"])].copy()
        if len(offer_df):
            fig = px.box(offer_df, x="Offer_Status", y="Salary_Gap_GBP", color="Offer_Status",
                         color_discrete_map={"Accepted": PASTEL_GREEN, "Declined": PASTEL_ROSE})
            fig.add_hline(y=0, line_dash="dash", line_color=TEXT_SLATE)
            fig.update_layout(yaxis_title="Offered − Expected Salary (£)")
            st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)
        else:
            st.info("No offer data in the current filter selection.")

    with colB:
        section_title("Offer Decline Reasons")
        decl = df["Offer_Decline_Reason"].dropna().value_counts().reset_index()
        decl.columns = ["Reason", "Count"]
        if len(decl):
            decl = decl.sort_values("Count")
            fig = px.bar(decl, x="Count", y="Reason", orientation="h", color="Reason", text="Count")
            fig.update_traces(textposition="outside", showlegend=False)
            st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)
        else:
            st.info("No declined offers in the current filter selection.")

    section_title("Probation Outcome of Hired Employees")
    prob_df = df["Probation_Status"].dropna().value_counts().reset_index()
    prob_df.columns = ["Status", "Count"]
    if len(prob_df):
        fig = px.pie(prob_df, names="Status", values="Count", hole=0.5,
                     color="Status", color_discrete_map={"Passed": PASTEL_GREEN, "In Progress": PASTEL_YELLOW, "Not Passed": PASTEL_ROSE})
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(apply_chart_style(fig, 380), use_container_width=True)
    else:
        st.info("No hires (with probation data) in the current filter selection.")


# ============================================================================
# PAGE 7 — INSIGHTS & RECOMMENDATIONS
# ============================================================================
elif page == "Insights & Recommendations":
    section_title("Key Insights (recalculated for your current filters)")

    total_applied = len(df)
    total_hired = int(df["Is_Hired"].sum())
    counts = funnel_counts(df)
    drop_offs = {
        "Screening": counts["Applied"] - counts["Screening Passed"],
        "Interview 1 → 2": counts["Interview 1"] - counts["Interview 2 (Final)"],
        "Final Interview → Offer": counts["Interview 2 (Final)"] - counts["Offer Extended"],
        "Offer Declined": counts["Offer Extended"] - counts["Hired"],
    }
    biggest_drop = max(drop_offs, key=drop_offs.get) if total_applied else "—"

    src_stats = df.groupby("Recruitment_Source").agg(
        Applied=("Candidate_ID", "count"), Hired=("Is_Hired", "sum"), Cost=("Hiring_Cost_GBP", "sum")
    ).reset_index()
    src_stats["ConvRate"] = (src_stats["Hired"] / src_stats["Applied"] * 100)
    src_stats["CostPerHire"] = np.where(src_stats["Hired"] > 0, src_stats["Cost"] / src_stats["Hired"], np.nan)
    best_src = src_stats.loc[src_stats["ConvRate"].idxmax()] if len(src_stats) else None
    cheap_src = src_stats.dropna(subset=["CostPerHire"])
    cheap_src = cheap_src.loc[cheap_src["CostPerHire"].idxmin()] if len(cheap_src) else None

    offer_df = df[df["Offer_Status"].isin(["Accepted", "Declined"])]
    acc_gap = offer_df.loc[offer_df["Offer_Status"] == "Accepted", "Salary_Gap_GBP"].mean()
    dec_gap = offer_df.loc[offer_df["Offer_Status"] == "Declined", "Salary_Gap_GBP"].mean()

    prob = df["Probation_Status"].value_counts()
    prob_total = prob.sum()
    not_passed_rate = fmt_pct(prob.get("Not Passed", 0), prob_total) if prob_total else "—"

    insights = []
    insights.append(f"Of <b>{total_applied:,}</b> applications in the current view, <b>{total_hired:,}</b> resulted in a hire — an overall conversion rate of <b>{fmt_pct(total_hired, total_applied)}</b>.")
    insights.append(f"The largest single loss of candidates happens at the <b>{biggest_drop}</b> stage (<b>{drop_offs.get(biggest_drop, 0):,}</b> candidates lost).")
    if best_src is not None:
        insights.append(f"<b>{best_src['Recruitment_Source']}</b> has the highest Applied→Hired conversion rate at <b>{best_src['ConvRate']:.1f}%</b>.")
    if cheap_src is not None:
        insights.append(f"<b>{cheap_src['Recruitment_Source']}</b> is the most cost-efficient channel at <b>£{cheap_src['CostPerHire']:,.0f}</b> per hire.")
    if pd.notna(acc_gap) and pd.notna(dec_gap):
        insights.append(f"Accepted offers average a salary gap of <b>£{acc_gap:,.0f}</b> (offered vs expected), while declined offers average <b>£{dec_gap:,.0f}</b> — compensation is a key driver of decline.")
    if prob_total:
        insights.append(f"<b>{not_passed_rate}</b> of hires with probation data did not pass probation, indicating a quality-of-hire watch point.")

    for ins in insights:
        st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Recommendations")

    recos = [
        ("Rebalance sourcing spend toward high-value channels",
         "Shift budget from Recruitment Agencies toward the Company Careers Page and an Employee Referral incentive programme.",
         "These channels combine strong conversion (22.9%–25.2%) with the lowest cost per hire (£1,622–£2,394) versus £4,885 for Agency hires."),
        ("Add a compensation-band check before offers go out",
         "Flag any offer more than ~£1,000 below the candidate's expected salary for review before it is sent.",
         "Declined offers average £2,564 below expectation vs +£274 for accepted offers — the clearest actionable predictor of decline in the data."),
        ("Tighten screening criteria for low-converting roles and sources",
         "Review job ads and screening questions for Operations/Marketing roles and for Indeed/University sourcing.",
         "Screening is the single biggest drop-off point (32.6% of applicants), and these segments convert well below average."),
        ("Recalibrate final-interview scoring against probation outcomes",
         "Compare Interview 2/Assessment scores of hires who failed probation against those who passed, and adjust thresholds.",
         "The hired vs not-hired score gap narrows most at the final interview stage, and 13.3% of hires still fail probation."),
        ("Share best-practice scheduling techniques across recruiters",
         "Pair faster and slower recruiters for short process-shadowing sessions focused on scheduling cadence.",
         "Workload is evenly distributed, so speed differences reflect technique rather than caseload — a low-cost fix."),
        ("Review equity in outcomes for underrepresented gender groups",
         "Run a structured, anonymised review of screening/interview scores for Non-binary and undisclosed-gender candidates.",
         "These groups convert at 14–18% versus 21–23% for male/female candidates — large enough to warrant investigation."),
        ("Target a company-wide time-to-hire under 45 days",
         "Map the process end-to-end, find multi-day scheduling gaps between stages, and set stage-level SLAs.",
         "Time-to-hire is consistent across departments/recruiters, meaning a shared process fix benefits everyone at once."),
    ]

    for i, (title, reco, why) in enumerate(recos, 1):
        st.markdown(f"""
        <div class="reco-card">
            <div class="reco-title">{i}. {title}</div>
            <div><span class="reco-label">Recommendation:</span> {reco}</div>
            <div style="margin-top:4px;"><span class="reco-label">Why:</span> {why}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("A full written report with charts and detailed reasoning is available as a companion Word document: Recruitment_Analytics_Report.docx")
