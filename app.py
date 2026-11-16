
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Weather Intelligence Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# BEAUTIFUL BACKGROUND + PROFESSIONAL CSS
# ==========================================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, #312E81 0%, transparent 35%),
        radial-gradient(circle at 90% 20%, #164E63 0%, transparent 30%),
        linear-gradient(135deg, #080D1B 0%, #10172A 50%, #111827 100%);
    color: #F8FAFC;
}

/* REMOVE TOP HEADER BACKGROUND */
[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN CONTENT */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080D1B, #111B35, #0B1220);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

/* HEADINGS */
h1, h2, h3 {
    color: #F8FAFC !important;
}

/* NORMAL TEXT */
p, label, span {
    color: #CBD5E1;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30,41,75,0.95),
        rgba(15,23,42,0.95)
    );
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 18px;
    padding: 22px 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

/* KPI LABEL */
[data-testid="stMetricLabel"] {
    color: #A5B4FC !important;
    font-size: 14px;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    color: #67E8F9 !important;
    font-size: 30px;
    font-weight: 700;
}

/* KPI DELTA */
[data-testid="stMetricDelta"] {
    color: #34D399 !important;
}

/* INPUTS */
div[data-baseweb="select"] {
    background-color: #17223B;
    border-radius: 10px;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(30,41,59,0.55);
    border: 1px dashed #64748B;
    border-radius: 15px;
    padding: 12px;
}

/* CHART CONTAINERS */
[data-testid="stPlotlyChart"] {
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 16px;
    padding: 10px;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg, #4F46E5, #0891B2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #6366F1, #06B6D4);
    color: white;
    border: none;
}

/* DIVIDER */
hr {
    border-color: rgba(148,163,184,0.2);
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 12px;
}

/* FOOTER */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div style="
    background: linear-gradient(120deg, #312E81, #1D4ED8, #0891B2);
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 25px;
    box-shadow: 0 15px 40px rgba(37,99,235,0.25);
">
    <h1 style="color:white !important; font-size:36px; margin:0;">
        🌦️ Weather Intelligence
    </h1>
    <p style="color:#DBEAFE !important; font-size:16px; margin-top:10px;">
        Interactive Weather Analytics & Climate Insights Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("""
# 🌤️ Weather Analytics
### Dashboard Controls
""")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Weather CSV",
    type=["csv"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Dashboard Theme")
st.sidebar.markdown("""
**Theme:** Midnight Blue  
**Accent:** Electric Cyan  
**Charts:** Blue / Purple / Teal
""")

# ==========================================
# DATA LOADING
# ==========================================

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Date column
    if "Formatted Date" in df.columns:
        df["Formatted Date"] = pd.to_datetime(
            df["Formatted Date"],
            errors="coerce",
            utc=True
        )

        df["Year"] = df["Formatted Date"].dt.year
        df["Month"] = df["Formatted Date"].dt.month
        df["Month Name"] = df["Formatted Date"].dt.month_name()
        df["Date"] = df["Formatted Date"].dt.date

    # Numeric columns
    numeric_columns = [
        "Temperature (C)",
        "Apparent Temperature (C)",
        "Humidity",
        "Wind Speed (km/h)",
        "Visibility (km)",
        "Pressure (millibars)"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ==========================================
# UPLOAD SCREEN
# ==========================================

if uploaded_file is None:

    st.markdown("""
    <div style="
        background:rgba(30,41,59,0.65);
        padding:35px;
        border-radius:20px;
        border:1px solid rgba(99,102,241,0.3);
        text-align:center;
    ">
        <h2 style="color:#67E8F9 !important;">
            Welcome to Weather Intelligence
        </h2>
        <p style="font-size:17px;">
            Upload your weather dataset from the sidebar to explore
            interactive climate insights and visual analytics.
        </p>
        <h3>📊 Data Analysis | 🌡️ Temperature | 🌧️ Weather</h3>
    </div>
    """, unsafe_allow_html=True)

    st.info("Please upload your weather CSV file from the sidebar.")
    st.stop()


# ==========================================
# LOAD DATA
# ==========================================

try:
    df = load_data(uploaded_file)

except Exception as e:
    st.error(f"Unable to load file: {e}")
    st.stop()


if df.empty:
    st.error("Your CSV file is empty.")
    st.stop()


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Data Filters")

filtered_df = df.copy()

# YEAR FILTER
if "Year" in df.columns and df["Year"].notna().any():

    years = sorted(df["Year"].dropna().unique().astype(int))

    if len(years) > 1:
        selected_years = st.sidebar.slider(
            "Select Year Range",
            min_value=int(min(years)),
            max_value=int(max(years)),
            value=(int(min(years)), int(max(years)))
        )

        filtered_df = filtered_df[
            filtered_df["Year"].between(
                selected_years[0],
                selected_years[1]
            )
        ]

    elif len(years) == 1:
        st.sidebar.info(f"Year: {years[0]}")


# WEATHER SUMMARY FILTER
if "Summary" in filtered_df.columns:

    summaries = sorted(
        filtered_df["Summary"].dropna().unique().tolist()
    )

    selected_summaries = st.sidebar.multiselect(
        "Weather Summary",
        summaries,
        default=summaries
    )

    filtered_df = filtered_df[
        filtered_df["Summary"].isin(selected_summaries)
    ]


# PRECIPITATION FILTER
if "Precip Type" in filtered_df.columns:

    precip_types = sorted(
        filtered_df["Precip Type"].dropna().unique().tolist()
    )

    selected_precip = st.sidebar.multiselect(
        "Precipitation Type",
        precip_types,
        default=precip_types
    )

    filtered_df = filtered_df[
        filtered_df["Precip Type"].isin(selected_precip)
    ]


if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()


# ==========================================
# KPI SECTION
# ==========================================

st.markdown("## 📌 Weather Overview")
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


def get_mean(column):
    if column in filtered_df.columns:
        return filtered_df[column].mean()
    return None


avg_temp = get_mean("Temperature (C)")
avg_feels = get_mean("Apparent Temperature (C)")
avg_humidity = get_mean("Humidity")
avg_wind = get_mean("Wind Speed (km/h)")
avg_visibility = get_mean("Visibility (km)")


with col1:
    st.metric(
        "🌡️ Avg Temperature",
        f"{avg_temp:.2f} °C" if pd.notna(avg_temp) else "N/A"
    )

with col2:
    st.metric(
        "🌤️ Feels Like",
        f"{avg_feels:.2f} °C" if pd.notna(avg_feels) else "N/A"
    )

with col3:
    st.metric(
        "💧 Avg Humidity",
        f"{avg_humidity * 100:.1f}%" if pd.notna(avg_humidity) else "N/A"
    )

with col4:
    st.metric(
        "💨 Wind Speed",
        f"{avg_wind:.2f} km/h" if pd.notna(avg_wind) else "N/A"
    )

with col5:
    st.metric(
        "👁️ Visibility",
        f"{avg_visibility:.2f} km" if pd.notna(avg_visibility) else "N/A"
    )


st.markdown("---")

# ==========================================
# CHART THEME
# ==========================================

COLORS = [
    "#6366F1",
    "#06B6D4",
    "#8B5CF6",
    "#10B981",
    "#F59E0B",
    "#EC4899"
]


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.20)",
        font=dict(
            color="#E2E8F0",
            family="Arial",
            size=12
        ),
        title_font=dict(
            color="#A5B4FC",
            size=18
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1")
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.12)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.12)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    return fig


# ==========================================
# ROW 1: MONTHLY TEMPERATURE + WEATHER TYPES
# ==========================================

st.markdown("## 📈 Weather Trends")

chart1, chart2 = st.columns(2)

with chart1:

    st.markdown("### 🌡️ Monthly Temperature")

    if "Month" in filtered_df.columns:

        monthly_temp = (
            filtered_df.groupby("Month")["Temperature (C)"]
            .mean()
            .reset_index()
        )

        fig1 = px.area(
            monthly_temp,
            x="Month",
            y="Temperature (C)",
            markers=True,
            color_discrete_sequence=["#06B6D4"]
        )

        fig1.update_traces(
            fill="tozeroy",
            line=dict(width=3),
            marker=dict(size=6)
        )

        fig1.update_layout(
            title="Average Temperature by Month",
            xaxis_title="Month",
            yaxis_title="Temperature (°C)"
        )

        st.plotly_chart(
            style_chart(fig1),
            use_container_width=True
        )

    else:
        st.info("Month column not available.")


with chart2:

    st.markdown("### 🌤️ Weather Distribution")

    if "Summary" in filtered_df.columns:

        weather_counts = (
            filtered_df["Summary"]
            .value_counts()
            .reset_index()
        )

        weather_counts.columns = ["Weather", "Count"]

        fig2 = px.pie(
            weather_counts,
            names="Weather",
            values="Count",
            hole=0.55,
            color_discrete_sequence=COLORS
        )

        fig2.update_traces(
            textinfo="percent",
            textfont=dict(color="white")
        )

        fig2.update_layout(
            title="Weather Conditions Distribution"
        )

        st.plotly_chart(
            style_chart(fig2),
            use_container_width=True
        )

    else:
        st.info("Summary column not available.")


# ==========================================
# ROW 2: TEMPERATURE VS HUMIDITY
# ==========================================

chart3, chart4 = st.columns(2)

with chart3:

    st.markdown("### 💧 Temperature vs Humidity")

    if all(
        col in filtered_df.columns
        for col in ["Temperature (C)", "Humidity"]
    ):

        fig3 = px.scatter(
            filtered_df.sample(
                min(3000, len(filtered_df)),
                random_state=42
            ),
            x="Temperature (C)",
            y="Humidity",
            color="Temperature (C)",
            color_continuous_scale="Viridis",
            opacity=0.65
        )

        fig3.update_layout(
            title="Temperature & Humidity Relationship",
            xaxis_title="Temperature (°C)",
            yaxis_title="Humidity"
        )

        st.plotly_chart(
            style_chart(fig3),
            use_container_width=True
        )

    else:
        st.info("Temperature or Humidity column unavailable.")


with chart4:

    st.markdown("### 📅 Yearly Temperature")

    if "Year" in filtered_df.columns:

        yearly_temp = (
            filtered_df.groupby("Year")["Temperature (C)"]
            .mean()
            .reset_index()
        )

        fig4 = px.bar(
            yearly_temp,
            x="Year",
            y="Temperature (C)",
            color="Temperature (C)",
            color_continuous_scale="Blues"
        )

        fig4.update_layout(
            title="Average Temperature by Year",
            xaxis_title="Year",
            yaxis_title="Temperature (°C)"
        )

        st.plotly_chart(
            style_chart(fig4),
            use_container_width=True
        )

    else:
        st.info("Year column unavailable.")


# ==========================================
# ROW 3: WIND SPEED + VISIBILITY
# ==========================================

chart5, chart6 = st.columns(2)

with chart5:

    st.markdown("### 💨 Wind Speed Analysis")

    if "Wind Speed (km/h)" in filtered_df.columns:

        wind_df = filtered_df.copy()

        if "Month" in wind_df.columns:

            monthly_wind = (
                wind_df.groupby("Month")["Wind Speed (km/h)"]
                .mean()
                .reset_index()
            )

            fig5 = px.line(
                monthly_wind,
                x="Month",
                y="Wind Speed (km/h)",
                markers=True,
                color_discrete_sequence=["#A78BFA"]
            )

            fig5.update_traces(line=dict(width=3))

            fig5.update_layout(
                title="Monthly Average Wind Speed",
                xaxis_title="Month",
                yaxis_title="Wind Speed (km/h)"
            )

            st.plotly_chart(
                style_chart(fig5),
                use_container_width=True
            )

        else:
            st.info("Month column unavailable.")

    else:
        st.info("Wind Speed column unavailable.")


with chart6:

    st.markdown("### 👁️ Visibility Analysis")

    if "Visibility (km)" in filtered_df.columns:

        if "Month" in filtered_df.columns:

            visibility_df = (
                filtered_df.groupby("Month")["Visibility (km)"]
                .mean()
                .reset_index()
            )

            fig6 = px.line(
                visibility_df,
                x="Month",
                y="Visibility (km)",
                markers=True,
                color_discrete_sequence=["#34D399"]
            )

            fig6.update_traces(line=dict(width=3))

            fig6.update_layout(
                title="Monthly Average Visibility",
                xaxis_title="Month",
                yaxis_title="Visibility (km)"
            )

            st.plotly_chart(
                style_chart(fig6),
                use_container_width=True
            )

        else:
            st.info("Month column unavailable.")

    else:
        st.info("Visibility column unavailable.")


# ==========================================
# DATA TABLE
# ==========================================

st.markdown("---")
st.markdown("## 📂 Weather Dataset")

with st.expander("View Filtered Data"):

    st.dataframe(
        filtered_df.head(1000),
        use_container_width=True,
        height=400
    )

    st.caption(
        f"Showing first 1000 records out of "
        f"{len(filtered_df):,} filtered records."
    )


# ==========================================
# DOWNLOAD CSV
# ==========================================

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Weather Data",
    data=csv_data,
    file_name="weather_filtered_data.csv",
    mime="text/csv"
)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style="
    text-align:center;
    padding:25px;
    margin-top:30px;
    border-top:1px solid rgba(148,163,184,0.15);
">
    <p style="color:#94A3B8;">
        🌦️ Weather Intelligence Dashboard |
        Built with Python, Streamlit & Plotly
    </p>
    <p style="color:#64748B; font-size:12px;">
        Interactive Climate Analytics & Data Visualization
    </p>
</div>
""", unsafe_allow_html=True)
