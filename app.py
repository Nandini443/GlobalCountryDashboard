"""
🌍 Global Country Dashboard
A beautiful, data-rich Streamlit application to explore world country statistics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 Global Country Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:   #0b1120;
    --ink:    #111827;
    --slate:  #1e293b;
    --card:   #162032;
    --gold:   #f59e0b;
    --teal:   #06b6d4;
    --rose:   #f43f5e;
    --green:  #10b981;
    --purple: #8b5cf6;
    --text:   #e2e8f0;
    --muted:  #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp { background: var(--navy); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--slate) !important;
    border-right: 1px solid #1e3a5f;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* Hide default header */
header[data-testid="stHeader"] { background: transparent; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f2044 0%, #0b1120 50%, #0e1a33 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-title span { color: var(--gold); }
.hero-sub {
    color: var(--muted);
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 300;
}

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    background: var(--card);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: var(--teal); }
.kpi-accent { position: absolute; top: 0; left: 0; width: 4px; height: 100%; border-radius: 12px 0 0 12px; }
.kpi-label { font-size: 0.72rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700; color: white; line-height: 1.1; margin: 0.2rem 0; }
.kpi-sub { font-size: 0.75rem; color: var(--muted); }

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    margin: 0.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e3a5f;
}
.section-header span { color: var(--gold); }

/* Country card */
.country-profile {
    background: var(--card);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 1.8rem;
}
.country-name {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    color: white;
    margin-bottom: 0.2rem;
}
.country-meta { color: var(--muted); font-size: 0.9rem; margin-bottom: 1rem; }

/* Stat pills */
.stat-row { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-bottom: 0.5rem; }
.stat-pill {
    background: #0b1e38;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.5rem 0.9rem;
    font-size: 0.82rem;
}
.stat-pill-label { color: var(--muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-pill-value { color: white; font-weight: 600; font-size: 0.95rem; }

/* Rank badge */
.rank-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #d97706);
    color: var(--navy);
    font-weight: 700;
    font-size: 0.75rem;
    padding: 0.15rem 0.6rem;
    border-radius: 99px;
    margin-left: 0.5rem;
}

/* Table styling */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: var(--slate); border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); border-radius: 8px; font-weight: 500; }
.stTabs [aria-selected="true"] { background: var(--card) !important; color: white !important; }

/* Plotly chart background */
.js-plotly-plot .plotly { border-radius: 12px; }

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #0f2044, #0e1a2e);
    border: 1px solid #1e3a5f;
    border-left: 4px solid var(--gold);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: var(--muted);
}
.insight-box strong { color: white; }

/* Footer */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    margin-top: 3rem;
    padding: 1.5rem;
    border-top: 1px solid #1e3a5f;
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "world_countries.csv")
    if not os.path.exists(csv_path):
        import subprocess
        subprocess.run(["python", os.path.join(os.path.dirname(__file__), "generate_data.py")], cwd=os.path.dirname(__file__))
    df = pd.read_csv(csv_path)
    return df

df = load_data()

CONTINENT_COLORS = {
    "Africa": "#f59e0b",
    "Asia": "#06b6d4",
    "Europe": "#8b5cf6",
    "North America": "#f43f5e",
    "South America": "#10b981",
    "Oceania": "#fb923c",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(11,17,32,0.6)",
    font=dict(family="DM Sans", color="#94a3b8"),
    title_font=dict(family="Playfair Display", color="white", size=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e3a5f", borderwidth=1),
    margin=dict(l=10, r=10, t=40, b=10),
)

def styled_chart(fig, height=420):
    fig.update_layout(**CHART_LAYOUT, height=height)
    fig.update_xaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    fig.update_yaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    return fig

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Global Dashboard")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🌐 World Overview", "🔍 Country Explorer", "📊 Compare Countries", "📈 Rankings & Trends", "🗺️ Data Table"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🎛️ Filters")

    continents = ["All"] + sorted(df["Continent"].unique().tolist())
    sel_continent = st.selectbox("Continent", continents)

    pop_range = st.slider(
        "Population (Millions)",
        float(df["Population_M"].min()),
        float(df["Population_M"].max()),
        (float(df["Population_M"].min()), float(df["Population_M"].max()))
    )

    gdp_range = st.slider(
        "GDP (Billion USD)",
        float(df["GDP_Billion_USD"].min()),
        float(df["GDP_Billion_USD"].max()),
        (float(df["GDP_Billion_USD"].min()), float(df["GDP_Billion_USD"].max()))
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#475569;'>Data sources: World Bank, UN, IMF · 2023 estimates</div>",
        unsafe_allow_html=True
    )

# ─── FILTER DATA ────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_continent != "All":
    fdf = fdf[fdf["Continent"] == sel_continent]
fdf = fdf[(fdf["Population_M"] >= pop_range[0]) & (fdf["Population_M"] <= pop_range[1])]
fdf = fdf[(fdf["GDP_Billion_USD"] >= gdp_range[0]) & (fdf["GDP_Billion_USD"] <= gdp_range[1])]

# ─── HELPER ─────────────────────────────────────────────────────────────────
def rank_of(country, col, ascending=False):
    ranked = df.sort_values(col, ascending=ascending).reset_index(drop=True)
    idx = ranked[ranked["Country"] == country].index
    return int(idx[0]) + 1 if len(idx) > 0 else "—"

def kpi(label, value, sub="", color="var(--teal)"):
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent" style="background:{color};"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

# ════════════════════════════════════════════════════════════════════════════
#  PAGE 1 · WORLD OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🌐 World Overview":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">🌍 Global Country <span>Dashboard</span></div>
        <div class="hero-sub">Explore economic, demographic & social indicators for 80 nations worldwide</div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    total_pop = fdf["Population_M"].sum()
    total_gdp = fdf["GDP_Billion_USD"].sum()
    avg_hdi   = fdf["HDI"].mean()
    avg_life  = fdf["Life_Expectancy"].mean()

    st.markdown(f"""
    <div class="kpi-grid">
        {kpi("Countries", f"{len(fdf)}", f"of 80 total", "var(--teal)")}
        {kpi("Total Population", f"{total_pop/1000:.2f}B", f"billion people", "var(--gold)")}
        {kpi("Combined GDP", f"${total_gdp/1000:.1f}T", f"trillion USD", "var(--green)")}
        {kpi("Avg Life Expectancy", f"{avg_life:.1f} yrs", f"Avg HDI: {avg_hdi:.3f}", "var(--purple)")}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="section-header">GDP vs <span>HDI</span> — Bubble Chart</div>', unsafe_allow_html=True)
        fig = px.scatter(
            fdf, x="GDP_Per_Capita_USD", y="HDI",
            size="Population_M", color="Continent",
            hover_name="Country",
            hover_data={"Population_M": ":.1f", "Life_Expectancy": ":.1f", "GDP_Per_Capita_USD": ":,.0f"},
            color_discrete_map=CONTINENT_COLORS,
            size_max=55, log_x=True,
            labels={"GDP_Per_Capita_USD": "GDP per Capita (USD, log scale)", "HDI": "Human Development Index"},
        )
        fig.update_traces(marker=dict(opacity=0.82, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        st.plotly_chart(styled_chart(fig, 430), use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">GDP Share by <span>Continent</span></div>', unsafe_allow_html=True)
        cont_gdp = fdf.groupby("Continent")["GDP_Billion_USD"].sum().reset_index()
        fig2 = px.pie(
            cont_gdp, values="GDP_Billion_USD", names="Continent",
            color="Continent", color_discrete_map=CONTINENT_COLORS,
            hole=0.55,
        )
        fig2.update_traces(textposition="outside", textinfo="label+percent",
                           marker=dict(line=dict(color="#0b1120", width=2)))
        fig2.update_layout(**CHART_LAYOUT, height=430,
                           annotations=[dict(text="GDP", x=0.5, y=0.5,
                                             font=dict(size=18, color="white",
                                                       family="Playfair Display"), showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Life Expectancy by <span>Continent</span></div>', unsafe_allow_html=True)
        fig3 = px.box(
            fdf, x="Continent", y="Life_Expectancy", color="Continent",
            color_discrete_map=CONTINENT_COLORS,
            points="all",
            labels={"Life_Expectancy": "Life Expectancy (years)"},
        )
        fig3.update_traces(marker=dict(size=5, opacity=0.6))
        st.plotly_chart(styled_chart(fig3, 380), use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Internet Penetration <span>Distribution</span></div>', unsafe_allow_html=True)
        fig4 = px.histogram(
            fdf, x="Internet_Penetration_Pct", color="Continent",
            nbins=20, barmode="stack",
            color_discrete_map=CONTINENT_COLORS,
            labels={"Internet_Penetration_Pct": "Internet Penetration (%)"},
        )
        st.plotly_chart(styled_chart(fig4, 380), use_container_width=True)

    # Choropleth
    st.markdown('<div class="section-header">🗺️ World <span>GDP per Capita</span> Map</div>', unsafe_allow_html=True)
    fig_map = px.choropleth(
        fdf, locations="Country", locationmode="country names",
        color="GDP_Per_Capita_USD",
        color_continuous_scale=[[0,"#0b1120"],[0.2,"#0f2044"],[0.5,"#06b6d4"],[1,"#f59e0b"]],
        hover_name="Country",
        hover_data={"GDP_Per_Capita_USD": ":,.0f", "HDI": ":.3f", "Life_Expectancy": ":.1f"},
        labels={"GDP_Per_Capita_USD": "GDP/Capita (USD)"},
    )
    fig_map.update_layout(
        **CHART_LAYOUT, height=460,
        geo=dict(
            showframe=False, showcoastlines=True,
            coastlinecolor="#1e3a5f", showland=True, landcolor="#162032",
            showocean=True, oceancolor="#0b1120",
            showcountries=True, countrycolor="#1e3a5f",
            bgcolor="rgba(0,0,0,0)"
        ),
        coloraxis_colorbar=dict(title="USD", tickfont=dict(color="#94a3b8"), title_font=dict(color="#94a3b8")),
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  PAGE 2 · COUNTRY EXPLORER
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Country Explorer":
    st.markdown('<div class="hero"><div class="hero-title">Country <span>Explorer</span></div><div class="hero-sub">Deep dive into any country\'s statistics and global ranking</div></div>', unsafe_allow_html=True)

    country = st.selectbox("Select a Country", sorted(df["Country"].tolist()), index=0)
    row = df[df["Country"] == country].iloc[0]

    col_a, col_b = st.columns([1, 1.4])

    with col_a:
        continent_color = CONTINENT_COLORS.get(row["Continent"], "#06b6d4")
        r_gdp = rank_of(country, "GDP_Billion_USD")
        r_hdi = rank_of(country, "HDI")
        r_pop = rank_of(country, "Population_M")

        st.markdown(f"""
        <div class="country-profile">
            <div class="country-name">{country}</div>
            <div class="country-meta">
                🌍 {row['Continent']} &nbsp;|&nbsp; 🏛️ {row['Capital_City']} &nbsp;|&nbsp; 💱 {row['Currency']}
            </div>

            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">Population</div>
                    <div class="stat-pill-value">{row['Population_M']:.1f}M
                        <span class="rank-badge">#{r_pop}</span>
                    </div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Area</div>
                    <div class="stat-pill-value">{row['Area_Km2']:,.0f} km²</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Pop. Density</div>
                    <div class="stat-pill-value">{row['Population_Density']:.1f}/km²</div>
                </div>
            </div>

            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">GDP</div>
                    <div class="stat-pill-value">${row['GDP_Billion_USD']:,.1f}B
                        <span class="rank-badge">#{r_gdp}</span>
                    </div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">GDP/Capita</div>
                    <div class="stat-pill-value">${row['GDP_Per_Capita_USD']:,.0f}</div>
                </div>
            </div>

            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">HDI</div>
                    <div class="stat-pill-value">{row['HDI']:.3f}
                        <span class="rank-badge">#{r_hdi}</span>
                    </div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Life Expectancy</div>
                    <div class="stat-pill-value">{row['Life_Expectancy']:.1f} yrs</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Education Index</div>
                    <div class="stat-pill-value">{row['Education_Index']:.3f}</div>
                </div>
            </div>

            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">Internet</div>
                    <div class="stat-pill-value">{row['Internet_Penetration_Pct']:.1f}%</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">CO₂/Capita</div>
                    <div class="stat-pill-value">{row['CO2_Tons_Per_Capita']:.2f}t</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Unemployment</div>
                    <div class="stat-pill-value">{row['Unemployment_Rate_Pct']:.1f}%</div>
                </div>
            </div>

            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">Military Spend</div>
                    <div class="stat-pill-value">${row['Military_Spend_Billion_USD']:.1f}B</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        # Radar chart — country vs world avg
        categories = ["HDI", "Life Exp.", "Internet", "Education", "GDP/Cap (norm)"]
        world_max = {
            "HDI": df["HDI"].max(),
            "Life_Expectancy": df["Life_Expectancy"].max(),
            "Internet_Penetration_Pct": 100,
            "Education_Index": df["Education_Index"].max(),
            "GDP_Per_Capita_USD": df["GDP_Per_Capita_USD"].max(),
        }
        def norm(col): return row[col] / world_max[col]
        def norm_avg(col): return df[col].mean() / world_max[col]

        vals_c = [norm("HDI"), norm("Life_Expectancy"), norm("Internet_Penetration_Pct"),
                  norm("Education_Index"), norm("GDP_Per_Capita_USD")]
        vals_w = [norm_avg("HDI"), norm_avg("Life_Expectancy"), norm_avg("Internet_Penetration_Pct"),
                  norm_avg("Education_Index"), norm_avg("GDP_Per_Capita_USD")]

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=vals_c + [vals_c[0]], theta=categories + [categories[0]],
                                        fill="toself", name=country,
                                        line=dict(color="#06b6d4", width=2),
                                        fillcolor="rgba(6,182,212,0.15)"))
        fig_r.add_trace(go.Scatterpolar(r=vals_w + [vals_w[0]], theta=categories + [categories[0]],
                                        fill="toself", name="World Avg",
                                        line=dict(color="#f59e0b", width=2, dash="dot"),
                                        fillcolor="rgba(245,158,11,0.08)"))
        fig_r.update_layout(
            **CHART_LAYOUT, height=340,
            polar=dict(
                bgcolor="rgba(11,17,32,0.5)",
                radialaxis=dict(visible=True, range=[0,1], gridcolor="#1e3a5f", linecolor="#1e3a5f",
                                tickfont=dict(color="#475569", size=10)),
                angularaxis=dict(gridcolor="#1e3a5f", linecolor="#1e3a5f",
                                 tickfont=dict(color="#94a3b8", size=11)),
            ),
            title=dict(text=f"{country} vs World Average", x=0.5),
        )
        st.plotly_chart(fig_r, use_container_width=True)

        # Rank bars
        metrics_rank = {
            "GDP": ("GDP_Billion_USD", False),
            "HDI": ("HDI", False),
            "Life Exp": ("Life_Expectancy", False),
            "Internet": ("Internet_Penetration_Pct", False),
            "CO₂/cap": ("CO2_Tons_Per_Capita", True),
            "Unemployment": ("Unemployment_Rate_Pct", True),
        }
        ranks = {m: rank_of(country, col, asc) for m, (col, asc) in metrics_rank.items()}
        total = len(df)

        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            x=list(ranks.keys()),
            y=[total - v + 1 for v in ranks.values()],
            marker_color=["#06b6d4" if v <= total/3 else "#f59e0b" if v <= 2*total/3 else "#f43f5e"
                          for v in ranks.values()],
            text=[f"#{v}" for v in ranks.values()],
            textposition="auto",
        ))
        fig_rank.update_layout(**CHART_LAYOUT, height=260,
                               title=dict(text="Global Rankings (higher bar = better rank)", x=0.5),
                               yaxis=dict(title="Score (relative)", showticklabels=False))
        st.plotly_chart(fig_rank, use_container_width=True)

    # Continental comparison
    st.markdown(f'<div class="section-header">{country} vs <span>{row["Continent"]}</span> Peers</div>', unsafe_allow_html=True)
    peers = df[df["Continent"] == row["Continent"]].sort_values("GDP_Per_Capita_USD", ascending=False)
    fig_peers = px.bar(
        peers, x="Country", y="GDP_Per_Capita_USD",
        color=peers["Country"].apply(lambda c: "Selected" if c == country else row["Continent"]),
        color_discrete_map={"Selected": "#f59e0b", row["Continent"]: "#1e3a5f"},
        labels={"GDP_Per_Capita_USD": "GDP per Capita (USD)"},
    )
    fig_peers.update_layout(**CHART_LAYOUT, height=340, showlegend=False)
    st.plotly_chart(fig_peers, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  PAGE 3 · COMPARE COUNTRIES
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊 Compare Countries":
    st.markdown('<div class="hero"><div class="hero-title">Country <span>Comparison</span></div><div class="hero-sub">Side-by-side analysis of any two nations</div></div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        c1 = st.selectbox("Country A", sorted(df["Country"].tolist()), index=0)
    with col_r:
        c2 = st.selectbox("Country B", sorted(df["Country"].tolist()), index=4)

    r1, r2 = df[df["Country"] == c1].iloc[0], df[df["Country"] == c2].iloc[0]

    COMPARE_METRICS = [
        ("Population (M)", "Population_M", ""),
        ("GDP (B USD)", "GDP_Billion_USD", "$"),
        ("GDP/Capita", "GDP_Per_Capita_USD", "$"),
        ("HDI", "HDI", ""),
        ("Life Expectancy", "Life_Expectancy", ""),
        ("Internet (%)", "Internet_Penetration_Pct", ""),
        ("Education Index", "Education_Index", ""),
        ("CO₂/Capita", "CO2_Tons_Per_Capita", ""),
        ("Unemployment (%)", "Unemployment_Rate_Pct", ""),
        ("Military ($B)", "Military_Spend_Billion_USD", "$"),
        ("Area (km²)", "Area_Km2", ""),
    ]

    # Side by side bars
    fig_cmp = make_subplots(rows=1, cols=len(COMPARE_METRICS),
                             subplot_titles=[m[0] for m in COMPARE_METRICS])

    for i, (label, col, prefix) in enumerate(COMPARE_METRICS, 1):
        v1, v2 = r1[col], r2[col]
        mx = max(v1, v2, 1)
        fig_cmp.add_trace(go.Bar(x=[c1], y=[v1], marker_color="#06b6d4", name=c1, showlegend=(i==1)), row=1, col=i)
        fig_cmp.add_trace(go.Bar(x=[c2], y=[v2], marker_color="#f59e0b", name=c2, showlegend=(i==1)), row=1, col=i)

    fig_cmp.update_layout(**CHART_LAYOUT, height=400, barmode="group",
                           title=dict(text=f"{c1} vs {c2} — Key Metrics", x=0.5))
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Detailed table
    st.markdown('<div class="section-header">Detailed <span>Comparison</span></div>', unsafe_allow_html=True)

    rows = []
    for label, col, prefix in COMPARE_METRICS:
        v1, v2 = r1[col], r2[col]
        if col in ["HDI","Education_Index"]:
            sv1, sv2 = f"{v1:.3f}", f"{v2:.3f}"
        elif col in ["GDP_Billion_USD","GDP_Per_Capita_USD","Military_Spend_Billion_USD","Area_Km2"]:
            sv1, sv2 = f"{prefix}{v1:,.1f}", f"{prefix}{v2:,.1f}"
        else:
            sv1, sv2 = f"{prefix}{v1:.1f}", f"{prefix}{v2:.1f}"
        winner = "🟦" if v1 > v2 else ("🟨" if v2 > v1 else "—")
        if col in ["CO2_Tons_Per_Capita","Unemployment_Rate_Pct"]:
            winner = "🟦" if v1 < v2 else ("🟨" if v2 < v1 else "—")
        rows.append({"Metric": label, c1: sv1, c2: sv2, "Better": winner})

    cmp_df = pd.DataFrame(rows)
    st.dataframe(cmp_df, use_container_width=True, hide_index=True)

    # Radar compare
    col_ra, col_rb = st.columns(2)
    with col_ra:
        st.markdown(f'<div class="section-header"><span>{c1}</span> Profile</div>', unsafe_allow_html=True)
    with col_rb:
        st.markdown(f'<div class="section-header"><span>{c2}</span> Profile</div>', unsafe_allow_html=True)

    radar_cols = ["HDI","Life_Expectancy","Internet_Penetration_Pct","Education_Index"]
    radar_labels = ["HDI","Life Exp","Internet","Education"]
    maxv = [df[c].max() for c in radar_cols]

    fig_rad = go.Figure()
    for country_n, row_n, color in [(c1, r1, "#06b6d4"), (c2, r2, "#f59e0b")]:
        vals = [row_n[c]/m for c, m in zip(radar_cols, maxv)]
        fig_rad.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=radar_labels+[radar_labels[0]],
            fill="toself", name=country_n,
            line=dict(color=color, width=2),
            fillcolor=color.replace("#","rgba(").replace("06b6d4","6,182,212,0.15)").replace("f59e0b","245,158,11,0.12)")
        ))
    fig_rad.update_layout(**CHART_LAYOUT, height=380,
                           polar=dict(bgcolor="rgba(11,17,32,0.5)",
                                      radialaxis=dict(range=[0,1], gridcolor="#1e3a5f", linecolor="#1e3a5f"),
                                      angularaxis=dict(gridcolor="#1e3a5f", linecolor="#1e3a5f")))
    st.plotly_chart(fig_rad, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  PAGE 4 · RANKINGS & TRENDS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Rankings & Trends":
    st.markdown('<div class="hero"><div class="hero-title">Rankings <span>&amp; Trends</span></div><div class="hero-sub">Top performers and key metric distributions across the globe</div></div>', unsafe_allow_html=True)

    metric_options = {
        "GDP (Billion USD)": "GDP_Billion_USD",
        "GDP per Capita": "GDP_Per_Capita_USD",
        "Human Development Index": "HDI",
        "Life Expectancy": "Life_Expectancy",
        "Internet Penetration (%)": "Internet_Penetration_Pct",
        "CO₂ per Capita": "CO2_Tons_Per_Capita",
        "Education Index": "Education_Index",
        "Military Spend ($B)": "Military_Spend_Billion_USD",
        "Unemployment Rate (%)": "Unemployment_Rate_Pct",
        "Population (Millions)": "Population_M",
    }

    col_m, col_n, col_asc = st.columns([2, 1, 1])
    with col_m:
        sel_metric_label = st.selectbox("Ranking Metric", list(metric_options.keys()))
    with col_n:
        top_n = st.slider("Top N countries", 5, 30, 15)
    with col_asc:
        order = st.radio("Order", ["Highest first", "Lowest first"])

    sel_col = metric_options[sel_metric_label]
    ascending = order == "Lowest first"
    ranked = fdf.sort_values(sel_col, ascending=ascending).head(top_n)

    colors = [CONTINENT_COLORS.get(c, "#94a3b8") for c in ranked["Continent"]]

    fig_bar = go.Figure(go.Bar(
        x=ranked[sel_col], y=ranked["Country"],
        orientation="h", marker_color=colors,
        text=ranked[sel_col].round(2),
        textposition="outside",
    ))
    fig_bar.update_layout(**CHART_LAYOUT, height=max(400, top_n * 26),
                           title=dict(text=f"Top {top_n} — {sel_metric_label}", x=0.5),
                           yaxis=dict(categoryorder="total ascending" if not ascending else "total descending"),
                           xaxis=dict(title=sel_metric_label))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Correlation heatmap
    st.markdown('<div class="section-header">Metric <span>Correlation</span> Heatmap</div>', unsafe_allow_html=True)
    corr_cols = ["GDP_Per_Capita_USD","HDI","Life_Expectancy","Internet_Penetration_Pct",
                 "Education_Index","CO2_Tons_Per_Capita","Unemployment_Rate_Pct"]
    corr_labels = ["GDP/Cap","HDI","Life Exp","Internet","Education","CO₂","Unemployment"]
    corr_matrix = fdf[corr_cols].corr().values

    fig_heat = go.Figure(go.Heatmap(
        z=corr_matrix, x=corr_labels, y=corr_labels,
        colorscale=[[0,"#f43f5e"],[0.5,"#0b1120"],[1,"#06b6d4"]],
        zmid=0, text=[[f"{v:.2f}" for v in row] for row in corr_matrix],
        texttemplate="%{text}", showscale=True,
        colorbar=dict(tickfont=dict(color="#94a3b8")),
    ))
    fig_heat.update_layout(**CHART_LAYOUT, height=420,
                            title=dict(text="Pearson Correlation Matrix", x=0.5))
    st.plotly_chart(fig_heat, use_container_width=True)

    # Scatter: any two metrics
    st.markdown('<div class="section-header">Custom <span>Scatter</span> Explorer</div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1: x_metric = st.selectbox("X axis", list(metric_options.keys()), key="sx")
    with s2: y_metric = st.selectbox("Y axis", list(metric_options.keys()), index=2, key="sy")

    fig_sc = px.scatter(
        fdf, x=metric_options[x_metric], y=metric_options[y_metric],
        color="Continent", hover_name="Country", size="Population_M", size_max=45,
        trendline="ols",
        color_discrete_map=CONTINENT_COLORS,
        labels={metric_options[x_metric]: x_metric, metric_options[y_metric]: y_metric},
    )
    fig_sc.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.15)")))
    st.plotly_chart(styled_chart(fig_sc, 420), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  PAGE 5 · DATA TABLE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Data Table":
    st.markdown('<div class="hero"><div class="hero-title">Full <span>Dataset</span></div><div class="hero-sub">Browse, filter and download the complete country dataset</div></div>', unsafe_allow_html=True)

    # Column selector
    all_cols = list(df.columns)
    default_cols = ["Country","Continent","Population_M","GDP_Billion_USD","GDP_Per_Capita_USD",
                    "HDI","Life_Expectancy","Internet_Penetration_Pct","CO2_Tons_Per_Capita"]
    sel_cols = st.multiselect("Select columns to display", all_cols, default=default_cols)

    search = st.text_input("🔍 Search country", "")
    display_df = fdf.copy()
    if search:
        display_df = display_df[display_df["Country"].str.contains(search, case=False)]

    if sel_cols:
        st.dataframe(
            display_df[sel_cols].reset_index(drop=True),
            use_container_width=True, height=520,
        )

        # Download
        csv_bytes = display_df[sel_cols].to_csv(index=False).encode()
        st.download_button(
            "⬇️ Download filtered CSV",
            data=csv_bytes,
            file_name="global_country_data.csv",
            mime="text/csv",
        )

    # Summary stats
    st.markdown('<div class="section-header">Statistical <span>Summary</span></div>', unsafe_allow_html=True)
    num_cols = fdf.select_dtypes(include="number").columns.tolist()
    summary = fdf[num_cols].describe().round(2)
    st.dataframe(summary, use_container_width=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌍 Global Country Dashboard &nbsp;·&nbsp; Built with Streamlit & Plotly &nbsp;·&nbsp;
    Data: World Bank, UN, IMF (2023 estimates) &nbsp;·&nbsp; 80 countries · 16 indicators
</div>
""", unsafe_allow_html=True)
