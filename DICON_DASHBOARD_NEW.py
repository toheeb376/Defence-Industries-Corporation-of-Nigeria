import os
import warnings
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="DICON | Production Intelligence",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

MILITARY_GREEN = "rgb(154,204,153)"
FOREST_GREEN   = "rgb(34,139,34)"
BLACK          = "rgb(0,0,0)"
SILVER         = "rgb(192,192,192)"
ALERT_RED      = "rgb(255,0,0)"

CHART_PALETTE = [
    "#9ACC99",
    "#228B22",
    "#5FAD8E",
    "#BDC3C7",
    "#FF0000",
    "#4A90D9",
    "#E8A838",
    "#7D9B76",
]

TIER_COLORS = {
    "Elite":          "#9ACC99",
    "Standard":       "#BDC3C7",
    "Below Standard": "#FF0000",
}


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

        .stApp {
            background-color: rgb(0,0,0);
            font-family: 'Rajdhani', sans-serif;
        }
        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgb(20,80,20) 0%, rgb(34,139,34) 40%, rgb(20,80,20) 100%);
            border-right: 2px solid rgb(154,204,153);
        }
        section[data-testid="stSidebar"] * {
            color: rgb(0,0,0) !important;
            font-family: 'Rajdhani', sans-serif !important;
        }
        section[data-testid="stSidebar"] label {
            font-weight: 700 !important;
            font-size: 0.78rem !important;
            letter-spacing: 0.07em !important;
            text-transform: uppercase !important;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(0,0,0,0.35) !important;
        }
        [data-testid="stMetric"] {
            background-color: rgb(0,0,0);
            border: 1px solid rgb(154,204,153);
            border-radius: 6px;
            padding: 14px 16px !important;
            box-shadow: 0 0 12px rgba(154,204,153,0.15);
        }
        [data-testid="stMetric"] label {
            color: rgb(192,192,192) !important;
            font-weight: 600 !important;
            font-size: 0.72rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            font-family: 'Rajdhani', sans-serif !important;
        }
        [data-testid="stMetricValue"] {
            color: rgb(154,204,153) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-size: 1.45rem !important;
        }
        h1, h2, h3, h4 {
            font-family: 'Rajdhani', sans-serif !important;
            color: rgb(154,204,153) !important;
            letter-spacing: 0.05em !important;
        }
        h1 { font-weight: 700 !important; }
        h2 { font-weight: 700 !important; }
        h3 { font-weight: 600 !important; }
        p, span, li { color: rgb(192,192,192); font-family: 'Rajdhani', sans-serif; }
        hr { border-color: rgb(34,139,34) !important; margin: 0.7rem 0 !important; }
        [data-testid="stExpander"] {
            background-color: rgb(10,10,10);
            border: 1px solid rgb(34,139,34) !important;
            border-radius: 6px !important;
        }
        [data-testid="stExpander"] summary {
            color: rgb(154,204,153) !important;
            font-weight: 700 !important;
            font-family: 'Rajdhani', sans-serif !important;
            letter-spacing: 0.06em !important;
        }
        .section-card {
            background-color: rgb(8,8,8);
            border: 1px solid rgb(34,139,34);
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 0 8px rgba(34,139,34,0.2);
        }
        .section-title {
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            color: rgb(154,204,153);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border-left: 3px solid rgb(34,139,34);
            padding-left: 8px;
            margin-bottom: 6px;
        }
        .dicon-header {
            background: linear-gradient(135deg, rgb(0,0,0) 0%, rgb(10,40,10) 50%, rgb(0,0,0) 100%);
            border: 1px solid rgb(154,204,153);
            border-radius: 8px;
            padding: 20px 28px;
            margin-bottom: 18px;
            box-shadow: 0 0 20px rgba(154,204,153,0.12);
        }
        .dicon-header h1 {
            color: rgb(154,204,153) !important;
            font-size: 1.75rem !important;
            margin: 0 !important;
            letter-spacing: 0.1em !important;
        }
        .dicon-header p {
            color: rgb(192,192,192) !important;
            margin: 4px 0 0 0 !important;
            font-size: 0.88rem !important;
        }
        .kpi-label {
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.68rem;
            font-weight: 700;
            color: rgb(34,139,34);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 8px;
        }
        .alert-badge {
            background-color: rgba(255,0,0,0.15);
            border: 1px solid rgb(255,0,0);
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.72rem;
            color: rgb(255,0,0) !important;
            font-weight: 700;
            letter-spacing: 0.06em;
        }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: rgb(0,0,0); }
        ::-webkit-scrollbar-thumb { background: rgb(34,139,34); border-radius: 3px; }
        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data():
    filepath = "Defence_Industries_Corporation_of_Nigeria__DICON_.xlsx"
    if not os.path.exists(filepath):
        return None, "File not found: " + filepath

    try:
        df = pd.read_excel(filepath, engine="openpyxl")
    except Exception as exc:
        return None, "Could not open Excel file: " + str(exc)

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    df["Production Date"] = pd.to_datetime(df["Production Date"], errors="coerce")
    df["Month_dt"] = df["Production Date"].dt.to_period("M").dt.to_timestamp()
    df["Month"]    = df["Production Date"].dt.to_period("M").astype(str)
    df["Year"]     = df["Production Date"].dt.year

    numeric_cols = [
        "Units Produced",
        "Unit Cost (NGN)",
        "Total Production Cost (NGN)",
        "Units Allocated - Army",
        "Units Allocated - Navy",
        "Units Allocated - Air Force",
        "Remaining Inventory",
        "Quality Inspection Score",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Total_Allocated"] = (
        df["Units Allocated - Army"]
        + df["Units Allocated - Navy"]
        + df["Units Allocated - Air Force"]
    )

    safe_produced  = df["Units Produced"].replace(0, float("nan"))
    safe_allocated = df["Total_Allocated"].replace(0, float("nan"))

    df["Allocation_Rate_Pct"] = (df["Total_Allocated"] / safe_produced * 100).fillna(0).round(2)
    df["Inventory_Retention_Pct"] = (df["Remaining Inventory"] / safe_produced * 100).fillna(0).round(2)
    df["Cost_Per_Allocated_Unit"] = (df["Total Production Cost (NGN)"] / safe_allocated).fillna(0).round(0)

    def classify_tier(score):
        if score >= 90:
            return "Elite"
        elif score >= 75:
            return "Standard"
        return "Below Standard"

    df["Quality_Tier"] = df["Quality Inspection Score"].apply(classify_tier)

    df["Efficiency_Score"] = (
        df["Total_Allocated"] / safe_produced * df["Quality Inspection Score"]
    ).fillna(0).round(2)

    df["Date_Ordinal"] = df["Production Date"].apply(
        lambda x: x.toordinal() if pd.notnull(x) else None
    )

    return df, None


def dark_theme(fig, title="", height=380):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Rajdhani", size=14, color=MILITARY_GREEN),
            x=0.01,
            xanchor="left",
        ),
        paper_bgcolor=BLACK,
        plot_bgcolor="rgb(8,8,8)",
        font=dict(family="Rajdhani", color=SILVER, size=12),
        height=height,
        margin=dict(l=10, r=10, t=44, b=10),
        legend=dict(
            font=dict(size=11, color=SILVER),
            bgcolor="rgba(0,0,0,0.85)",
            bordercolor=FOREST_GREEN,
            borderwidth=1,
        ),
        xaxis=dict(
            gridcolor="rgb(20,50,20)",
            linecolor=FOREST_GREEN,
            tickfont=dict(color=MILITARY_GREEN, size=11),
            title_font=dict(color=SILVER, size=12),
            zerolinecolor=FOREST_GREEN,
        ),
        yaxis=dict(
            gridcolor="rgb(20,50,20)",
            linecolor=FOREST_GREEN,
            tickfont=dict(color=MILITARY_GREEN, size=11),
            title_font=dict(color=SILVER, size=12),
            zerolinecolor=FOREST_GREEN,
        ),
        hoverlabel=dict(
            bgcolor=BLACK,
            font_color=MILITARY_GREEN,
            font_family="Rajdhani",
            bordercolor=FOREST_GREEN,
        ),
    )
    return fig


def render_sidebar(df):
    with st.sidebar:
        logo_path = "Defence_Industries_Corporation_of_Nigeria__DICON_.png"
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown("## DICON")

        st.markdown("---")
        st.markdown(
            "<div style='color:rgba(0,0,0,0.8);font-size:0.7rem;"
            "text-transform:uppercase;letter-spacing:0.12em;font-weight:700;"
            "margin-bottom:10px'>Operational Filters</div>",
            unsafe_allow_html=True,
        )

        def opts(col):
            return sorted(df[col].dropna().astype(str).unique().tolist())

        facilities  = opts("Facility")
        categories  = opts("Product Category")
        products    = opts("Product Name")
        tiers       = opts("Quality_Tier")
        supervisors = opts("Production Supervisor")

        sel_facility   = st.multiselect("Facility",          facilities,  default=facilities,  key="ff")
        sel_category   = st.multiselect("Product Category",  categories,  default=categories,  key="fc")
        sel_product    = st.multiselect("Product Name",      products,    default=products,    key="fp")
        sel_tier       = st.multiselect("Quality Tier",      tiers,       default=tiers,       key="ft")
        sel_supervisor = st.multiselect("Supervisor",        supervisors, default=supervisors, key="fs")

        st.markdown("**Production Date Range**")
        min_d = df["Production Date"].min().date()
        max_d = df["Production Date"].max().date()
        date_start = st.date_input("From", value=min_d, min_value=min_d, max_value=max_d, key="ds")
        date_end   = st.date_input("To",   value=max_d, min_value=min_d, max_value=max_d, key="de")

        st.markdown("---")
        st.markdown(
            "<div style='color:rgba(0,0,0,0.55);font-size:0.65rem;"
            "text-align:center;line-height:1.7;font-weight:600'>"
            "DICON PRODUCTION INTELLIGENCE<br>"
            "CLASSIFIED - INTERNAL USE ONLY</div>",
            unsafe_allow_html=True,
        )

    return (sel_facility, sel_category, sel_product,
            sel_tier, sel_supervisor, date_start, date_end)


def apply_filters(df, sel_facility, sel_category, sel_product,
                  sel_tier, sel_supervisor, date_start, date_end):
    fdf = df.copy()
    if sel_facility:   fdf = fdf[fdf["Facility"].isin(sel_facility)]
    if sel_category:   fdf = fdf[fdf["Product Category"].isin(sel_category)]
    if sel_product:    fdf = fdf[fdf["Product Name"].isin(sel_product)]
    if sel_tier:       fdf = fdf[fdf["Quality_Tier"].isin(sel_tier)]
    if sel_supervisor: fdf = fdf[fdf["Production Supervisor"].isin(sel_supervisor)]
    fdf = fdf[fdf["Production Date"].notna()]
    fdf = fdf[
        (fdf["Production Date"].dt.date >= date_start) &
        (fdf["Production Date"].dt.date <= date_end)
    ]
    return fdf.reset_index(drop=True)


def render_kpis(fdf):
    n          = len(fdf)
    units      = int(fdf["Units Produced"].sum())
    cost       = float(fdf["Total Production Cost (NGN)"].sum())
    avg_qual   = float(fdf["Quality Inspection Score"].mean()) if n > 0 else 0.0
    alloc_rate = float(fdf["Allocation_Rate_Pct"].mean()) if n > 0 else 0.0
    army       = int(fdf["Units Allocated - Army"].sum())
    navy       = int(fdf["Units Allocated - Navy"].sum())
    af_units   = int(fdf["Units Allocated - Air Force"].sum())

    st.markdown("<div class='kpi-label'>Command KPI Overview</div>", unsafe_allow_html=True)

    row1 = st.columns(4)
    row1[0].metric("PRODUCTION RECORDS",   f"{n:,}")
    row1[1].metric("TOTAL UNITS PRODUCED", f"{units:,}")
    row1[2].metric("TOTAL COST (NGN)",     f"NGN {cost:,.0f}")
    row1[3].metric("AVG QUALITY SCORE",    f"{avg_qual:.2f}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    row2 = st.columns(4)
    row2[0].metric("AVG ALLOCATION RATE", f"{alloc_rate:.1f}%")
    row2[1].metric("ARMY ALLOCATED",      f"{army:,}")
    row2[2].metric("NAVY ALLOCATED",      f"{navy:,}")
    row2[3].metric("AIR FORCE ALLOCATED", f"{af_units:,}")


def chart_units_by_facility(fdf):
    d = fdf.groupby("Facility")["Units Produced"].sum().reset_index()
    d.columns = ["Facility", "Units"]
    fig = px.bar(d, x="Facility", y="Units",
                 color="Facility", color_discrete_sequence=CHART_PALETTE, text="Units")
    fig.update_traces(textposition="outside", textfont_color=SILVER, marker_line_width=0)
    fig = dark_theme(fig, "Units Produced by Facility")
    fig.update_layout(showlegend=False)
    return fig


def chart_cost_by_category(fdf):
    d = (fdf.groupby("Product Category")["Total Production Cost (NGN)"]
         .sum().reset_index().sort_values("Total Production Cost (NGN)"))
    d.columns = ["Category", "Cost"]
    fig = px.bar(d, y="Category", x="Cost", orientation="h",
                 color="Cost",
                 color_continuous_scale=["rgb(20,60,20)", MILITARY_GREEN],
                 text=d["Cost"].apply(lambda v: "NGN " + f"{v/1e9:.2f}B"))
    fig.update_traces(textposition="outside", textfont_color=SILVER, marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return dark_theme(fig, "Production Cost by Product Category")


def chart_monthly_trend(fdf):
    d = (fdf.groupby("Month_dt")["Units Produced"]
         .sum().reset_index().sort_values("Month_dt"))
    d.columns = ["Month", "Units"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=d["Month"], y=d["Units"],
        mode="lines+markers",
        line=dict(color=MILITARY_GREEN, width=2.5),
        marker=dict(size=7, color=FOREST_GREEN,
                    line=dict(width=2, color=MILITARY_GREEN)),
        fill="tozeroy",
        fillcolor="rgba(34,139,34,0.12)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Units: %{y:,}<extra></extra>",
    ))
    return dark_theme(fig, "Monthly Production Volume Trend")


def chart_branch_allocation(fdf):
    d = (fdf.groupby("Product Name")[
        ["Units Allocated - Army", "Units Allocated - Navy", "Units Allocated - Air Force"]
    ].sum().reset_index().sort_values("Units Allocated - Army", ascending=False).head(8))
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Army", x=d["Product Name"],
                         y=d["Units Allocated - Army"], marker_color=MILITARY_GREEN))
    fig.add_trace(go.Bar(name="Navy", x=d["Product Name"],
                         y=d["Units Allocated - Navy"], marker_color=FOREST_GREEN))
    fig.add_trace(go.Bar(name="Air Force", x=d["Product Name"],
                         y=d["Units Allocated - Air Force"], marker_color=SILVER))
    fig = dark_theme(fig, "Service Branch Allocation by Product")
    fig.update_layout(barmode="group")
    fig.update_xaxes(tickangle=-25)
    return fig


def chart_top10_products(fdf):
    d = (fdf.groupby("Product Name")["Units Produced"]
         .sum().nlargest(10).reset_index().sort_values("Units Produced"))
    d.columns = ["Product", "Units"]
    fig = px.bar(d, y="Product", x="Units", orientation="h",
                 color="Units",
                 color_continuous_scale=["rgb(20,60,20)", MILITARY_GREEN],
                 text=d["Units"].apply(lambda v: f"{v:,}"))
    fig.update_traces(textposition="outside", textfont_color=SILVER, marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return dark_theme(fig, "Top 10 Products by Units Produced", height=400)


def chart_quality_histogram(fdf):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=fdf["Quality Inspection Score"],
        nbinsx=20,
        marker_color=MILITARY_GREEN,
        marker_line_color=FOREST_GREEN,
        marker_line_width=1,
        opacity=0.85,
        hovertemplate="Score: %{x}<br>Count: %{y}<extra></extra>",
    ))
    fig.add_vline(x=90, line_dash="dash", line_color="rgb(255,255,0)",
                  annotation_text="Elite 90+", annotation_font_color="rgb(255,255,0)")
    fig.add_vline(x=75, line_dash="dash", line_color=ALERT_RED,
                  annotation_text="Standard 75+", annotation_font_color=ALERT_RED)
    return dark_theme(fig, "Quality Inspection Score Distribution")


def chart_inventory_by_facility(fdf):
    d = fdf.groupby("Facility")["Remaining Inventory"].sum().reset_index()
    d.columns = ["Facility", "Inventory"]
    fig = px.bar(d, x="Facility", y="Inventory",
                 color="Inventory",
                 color_continuous_scale=["rgb(180,0,0)", MILITARY_GREEN],
                 text=d["Inventory"].apply(lambda v: f"{v:,}"))
    fig.update_traces(textposition="outside", textfont_color=SILVER, marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return dark_theme(fig, "Remaining Inventory by Facility")


def chart_supervisor_performance(fdf):
    d = (fdf.groupby("Production Supervisor")["Units Produced"]
         .sum().reset_index().sort_values("Units Produced", ascending=False))
    d.columns = ["Supervisor", "Units"]
    fig = px.bar(d, x="Supervisor", y="Units",
                 color="Units",
                 color_continuous_scale=["rgb(20,60,20)", MILITARY_GREEN],
                 text=d["Units"].apply(lambda v: f"{v:,}"))
    fig.update_traces(textposition="outside", textfont_color=SILVER, marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    return dark_theme(fig, "Production Supervisor Performance")


def chart_quality_tier_donut(fdf):
    d = fdf["Quality_Tier"].value_counts().reset_index()
    d.columns = ["Tier", "Count"]
    fig = px.pie(d, names="Tier", values="Count", hole=0.55,
                 color="Tier", color_discrete_map=TIER_COLORS)
    fig.update_traces(textposition="outside", textfont_size=12,
                      textfont_color=SILVER, pull=[0.04] * len(d))
    fig = dark_theme(fig, "Quality Tier Distribution", height=360)
    fig.update_layout(
        legend=dict(orientation="v", x=1.0, y=0.5),
        annotations=[dict(text="Quality<br>Tiers", x=0.5, y=0.5,
                          font_size=13, font_color=MILITARY_GREEN,
                          font_family="Rajdhani", showarrow=False)],
    )
    return fig


def chart_3d_scatter(fdf):
    d = fdf.dropna(subset=["Date_Ordinal", "Units Produced",
                            "Total Production Cost (NGN)"]).copy()
    if d.empty:
        return None

    tier_color_map = {
        "Elite":          "#9ACC99",
        "Standard":       "#BDC3C7",
        "Below Standard": "#FF0000",
    }

    fig = go.Figure()
    for tier_name, grp in d.groupby("Quality_Tier"):
        tier_str = str(tier_name)
        fig.add_trace(go.Scatter3d(
            x=grp["Date_Ordinal"],
            y=grp["Units Produced"],
            z=grp["Total Production Cost (NGN)"],
            mode="markers",
            name=tier_str,
            marker=dict(
                size=5,
                color=tier_color_map.get(tier_str, "#BDC3C7"),
                opacity=0.85,
                line=dict(width=0.5, color=BLACK),
            ),
            customdata=grp[["Record ID", "Product Name", "Facility",
                             "Batch Number", "Production Supervisor"]].values,
            hovertemplate=(
                "<b>%{customdata[1]}</b><br>"
                "Record: %{customdata[0]}<br>"
                "Facility: %{customdata[2]}<br>"
                "Batch: %{customdata[3]}<br>"
                "Supervisor: %{customdata[4]}<br>"
                "Units: %{y:,}<br>"
                "Cost: NGN %{z:,.0f}<extra></extra>"
            ),
        ))

    fig.update_layout(
        title=dict(
            text="3D Intelligence Scatter - Date x Units x Production Cost",
            font=dict(family="Rajdhani", size=14, color=MILITARY_GREEN),
            x=0.01,
        ),
        paper_bgcolor=BLACK,
        height=540,
        margin=dict(l=0, r=0, t=50, b=0),
        scene=dict(
            bgcolor="rgb(5,5,5)",
            xaxis=dict(title="Date (Ordinal)", backgroundcolor="rgb(10,30,10)",
                       gridcolor=FOREST_GREEN, color=MILITARY_GREEN, showbackground=True),
            yaxis=dict(title="Units Produced", backgroundcolor="rgb(10,30,10)",
                       gridcolor=FOREST_GREEN, color=MILITARY_GREEN, showbackground=True),
            zaxis=dict(title="Cost (NGN)", backgroundcolor="rgb(10,30,10)",
                       gridcolor=FOREST_GREEN, color=MILITARY_GREEN, showbackground=True),
        ),
        legend=dict(font=dict(size=11, color=SILVER), bgcolor="rgba(0,0,0,0.85)",
                    bordercolor=FOREST_GREEN, borderwidth=1),
        hoverlabel=dict(bgcolor=BLACK, font_color=MILITARY_GREEN, font_family="Rajdhani"),
    )
    return fig


def render_insights(fdf):
    n         = len(fdf)
    units     = int(fdf["Units Produced"].sum())
    cost      = float(fdf["Total Production Cost (NGN)"].sum())
    avg_qual  = float(fdf["Quality Inspection Score"].mean()) if n > 0 else 0.0
    alloc_r   = float(fdf["Allocation_Rate_Pct"].mean()) if n > 0 else 0.0
    inv_total = int(fdf["Remaining Inventory"].sum())

    top_fac  = fdf.groupby("Facility")["Units Produced"].sum().idxmax() if n else "N/A"
    top_prod = fdf.groupby("Product Name")["Units Produced"].sum().idxmax() if n else "N/A"
    top_sup  = fdf.groupby("Production Supervisor")["Units Produced"].sum().idxmax() if n else "N/A"

    elite_count = int((fdf["Quality_Tier"] == "Elite").sum())
    elite_pct   = elite_count / n * 100 if n else 0.0

    quality_msg = "Quality is mission-ready." if avg_qual >= 88 else "Quality improvement protocols required."
    inv_msg     = "Inventory buffer is adequate." if inv_total > 1000 else "CRITICAL: buffer low - escalate procurement."
    alloc_msg   = "within target." if alloc_r >= 80 else "below target - review allocation pipeline."

    with st.expander("Command Intelligence Summary - Click to Expand", expanded=False):
        st.markdown(
            f"""
            <div style='font-family:Rajdhani,sans-serif;color:rgb(192,192,192);line-height:1.9;font-size:1rem'>
            <h4 style='color:rgb(154,204,153);font-family:Rajdhani,sans-serif;margin-top:0;letter-spacing:0.08em'>
                OPERATIONAL PRODUCTION INTELLIGENCE BRIEF
            </h4>
            <p>Filtered view: <strong style='color:rgb(154,204,153)'>{n:,} records</strong>
            | {units:,} units | NGN {cost:,.0f}</p>
            <hr style='border-color:rgb(34,139,34)'>
            <p><strong style='color:rgb(154,204,153)'>Facility Leadership:</strong>
            {top_fac} leads output. Prioritise maintenance and supply allocation here.</p>
            <p><strong style='color:rgb(154,204,153)'>Quality Posture:</strong>
            Avg score {avg_qual:.2f}. {elite_pct:.1f}% batches are Elite tier. {quality_msg}</p>
            <p><strong style='color:rgb(154,204,153)'>Allocation Efficiency:</strong>
            Avg rate {alloc_r:.1f}% - {alloc_msg} Inventory: {inv_total:,} units. {inv_msg}</p>
            <p><strong style='color:rgb(154,204,153)'>Top Product:</strong> {top_prod}</p>
            <p><strong style='color:rgb(154,204,153)'>Supervisor Intelligence:</strong>
            {top_sup} leads volume. Consider cross-facility rotation.</p>
            <p><strong style='color:rgb(154,204,153)'>Cost Intelligence:</strong>
            NGN {cost:,.0f} total. Benchmark cost-per-unit monthly.</p>
            <p><strong style='color:rgb(154,204,153)'>Command Action:</strong>
            Monitor Branch Allocation weekly. Use 3D scatter for capacity planning.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section_chart(title, fig):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Insufficient data for this chart with current filters.")


def main():
    inject_css()

    with st.spinner("Loading DICON production data..."):
        df, err = load_data()

    if err:
        st.error(err)
        st.info(
            "SETUP GUIDE\n\n"
            "1. Open terminal and run:\n"
            "   pip install streamlit pandas plotly openpyxl\n\n"
            "2. Place these 3 files in the SAME folder:\n"
            "   dicon_app.py\n"
            "   Defence_Industries_Corporation_of_Nigeria__DICON_.xlsx\n"
            "   Defence_Industries_Corporation_of_Nigeria__DICON_.png\n\n"
            "3. Run:  streamlit run dicon_app.py"
        )
        return

    (sel_facility, sel_category, sel_product,
     sel_tier, sel_supervisor, date_start, date_end) = render_sidebar(df)

    fdf = apply_filters(df, sel_facility, sel_category, sel_product,
                        sel_tier, sel_supervisor, date_start, date_end)

    st.markdown(
        f"<div class='dicon-header'>"
        f"<h1>DICON PRODUCTION INTELLIGENCE COMMAND</h1>"
        f"<p>Defence Industries Corporation of Nigeria | "
        f"Showing <strong>{len(fdf):,}</strong> of <strong>{len(df):,}</strong> records | "
        f"{date_start.strftime('%d %b %Y')} to {date_end.strftime('%d %b %Y')} | "
        f"<span class='alert-badge'>CLASSIFIED - INTERNAL USE</span></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if len(fdf) == 0:
        st.warning("No records match the current filters. Please adjust the sidebar.")
        return

    render_kpis(fdf)
    st.markdown("---")

    c1, c2 = st.columns([1, 1.6])
    with c1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Units Produced by Facility", chart_units_by_facility(fdf))
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Monthly Production Volume Trend", chart_monthly_trend(fdf))
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns([1.6, 1])
    with c3:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Production Cost by Product Category", chart_cost_by_category(fdf))
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Quality Tier Distribution", chart_quality_tier_donut(fdf))
        st.markdown("</div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Service Branch Allocation by Product", chart_branch_allocation(fdf))
        st.markdown("</div>", unsafe_allow_html=True)
    with c6:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Top 10 Products by Units Produced", chart_top10_products(fdf))
        st.markdown("</div>", unsafe_allow_html=True)

    c7, c8 = st.columns(2)
    with c7:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Quality Inspection Score Distribution", chart_quality_histogram(fdf))
        st.markdown("</div>", unsafe_allow_html=True)
    with c8:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        section_chart("Remaining Inventory by Facility", chart_inventory_by_facility(fdf))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_chart("Production Supervisor Performance", chart_supervisor_performance(fdf))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_chart("3D Intelligence Scatter - Date x Units x Production Cost",
                  chart_3d_scatter(fdf))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    render_insights(fdf)

    st.markdown(
        "<div style='text-align:center;padding:16px 0 8px;"
        "color:rgb(34,139,34);font-size:0.7rem;"
        "font-family:Rajdhani,sans-serif;letter-spacing:0.1em'>"
        "DICON PRODUCTION INTELLIGENCE SYSTEM | STREAMLIT + PLOTLY | "
        "2025 DEFENCE INDUSTRIES CORPORATION OF NIGERIA | "
        "<span style='color:rgb(255,0,0)'>RESTRICTED</span>"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()