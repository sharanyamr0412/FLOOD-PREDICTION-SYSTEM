import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import base64  
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="FloodSense",
    page_icon="🌊",
    layout="wide"
)
# Application starting page
if "started" not in st.session_state:
    st.session_state.started = False

def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if not st.session_state.started:

    bg = get_base64_image("assets/floodsense_bg.png")
    st.markdown(f"""
    <style>
    .hero {{
        background-image:
        linear-gradient(rgba(5,30,50,0.72), rgba(5,30,50,0.82)),
        url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        padding: 85px 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
    }}

    .hero h1 {{
        font-size: 55px;
        color: white;
    }}

    .hero h2 {{
        color: #42E8E0;
        font-size: 30px;
    }}

    .hero p {{
        font-size: 19px;
        color: white;
    }}
    </style>

    <div class="hero">
        <h1>🌊 FloodSense</h1>
        <h2>Smarter Flood Monitoring. Safer Communities.</h2>
        <p>AI-Powered Urban Flood Analysis and Early Warning System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.info("🌧️ Rainfall Analysis")
    col2.info("🌊 Flood History")
    col3.info("⚠️ Flood Risk")
    col4.info("📊 Impact Assessment")

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns([1, 2, 1])

    with b:
        if st.button("🚀 GET STARTED", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.stop()
# ---------------- FLOODSENSE CUSTOM DESIGN ----------------


# ==========================================
# FLOODSENSE CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

/* ----------------------------------
   MAIN APPLICATION
---------------------------------- */

.stApp {
    background-color: #F3F7FA;
    color: #183247;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ----------------------------------
   MAIN HEADINGS
---------------------------------- */

h1 {
    color: #12304A !important;
    font-weight: 800 !important;
}

h2 {
    color: #164E63 !important;
    font-weight: 700 !important;
}

h3 {
    color: #087E8B !important;
    font-weight: 650 !important;
}

/* Paragraphs */

p {
    color: #40566B;
    line-height: 1.6;
}

/* ----------------------------------
   SIDEBAR DESIGN
---------------------------------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #102A43 0%,
        #164E63 100%
    );
    border-right: 1px solid #24566B;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Sidebar title */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
}

/* Sidebar navigation spacing */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 10px;
}

/* Sidebar radio labels */

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: rgba(255,255,255,0.06);
    padding: 12px;
    border-radius: 10px;
    transition: 0.2s;
}

/* ----------------------------------
   METRIC CARDS
---------------------------------- */

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #DCE8EF;
    box-shadow: 0 4px 12px rgba(16,42,67,0.06);
    transition: 0.2s;
}

div[data-testid="stMetricLabel"] {
    color: #52697D !important;
    font-size: 14px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #087E8B !important;
    font-size: 28px;
    font-weight: 800;
}

/* ----------------------------------
   BUTTON DESIGN
---------------------------------- */

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #087E8B,
        #0D9AA4
    );
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 650;
    transition: 0.2s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #065F69;
    border: none;
    color: white !important;
}

/* ----------------------------------
   INPUT FIELDS
---------------------------------- */

div[data-baseweb="input"] > div {
    background-color: #FFFFFF;
    border: 1px solid #CAD9E2;
    border-radius: 9px;
}

div[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-radius: 9px;
    border-color: #CAD9E2;
}

/* ----------------------------------
   CHART CONTAINERS
---------------------------------- */

div[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE8EF;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 3px 10px rgba(16,42,67,0.04);
}

/* ----------------------------------
   DATA TABLES
---------------------------------- */

div[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #DCE8EF;
    padding: 8px;
}

/* ----------------------------------
   EXPANDER DESIGN
---------------------------------- */

div[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE8EF;
    border-radius: 12px;
}

/* ----------------------------------
   DIVIDERS
---------------------------------- */

hr {
    border: none;
    height: 1px;
    background-color: #D8E4EB;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* ----------------------------------
   ALERT BOXES
---------------------------------- */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ----------------------------------
   FORM DESIGN
---------------------------------- */

div[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #DCE8EF;
}

/* ----------------------------------
   FOOTER
---------------------------------- */

.footer {
    text-align: center;
    padding: 25px;
    color: #64748B;
    font-size: 13px;
    border-top: 1px solid #DCE8EF;
    margin-top: 35px;
}

/* ----------------------------------
   SCROLLBAR
---------------------------------- */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #8AAEBB;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: #EAF1F5;
}

/* ----------------------------------
   RESPONSIVE LAYOUT
---------------------------------- */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# FLOODSENSE BRANDING
# ==========================================

st.markdown("""
<div style="background: linear-gradient(120deg, #102A43, #078A91); padding: 35px; border-radius: 18px; text-align: center; margin-bottom: 30px;">
<h1 style="color: white; font-size: 38px; margin: 0;">🌊 FloodSense</h1>
<p style="color: white; font-size: 17px; margin-top: 10px;">AI-Powered Urban Flood Analysis and Early Warning System</p>
</div>
""", unsafe_allow_html=True)
# ---------------- LOAD DATASETS ----------------

DATA = "cleaned_data"

@st.cache_data
def load_data(file):
    path = os.path.join(DATA, file)
    return pd.read_csv(path)

try:
    rainfall = load_data("daily_rainfall_cleaned.csv")
    dfsi = load_data("DFSI_cleaned.csv")
    impact = load_data("FloodImpact_cleaned.csv")
    flooded = load_data("District_FloodedArea_cleaned.csv")
    flood_history = load_data("FloodInventory_cleaned.csv")
    kerala = load_data("district_wise_details_cleaned.csv")

except FileNotFoundError as e:
    st.error(f"Dataset not found: {e}")
    st.info("Check that all cleaned CSV files are inside cleaned_data.")
    st.stop()

# Convert dates
rainfall["Date"] = pd.to_datetime(
    rainfall["Date"], errors="coerce"
)

flood_history["Start Date"] = pd.to_datetime(
    flood_history["Start Date"], errors="coerce"
)

# Convert numerical columns
rainfall["Daily Actual"] = pd.to_numeric(
    rainfall["Daily Actual"], errors="coerce"
)

dfsi["DFSI"] = pd.to_numeric(
    dfsi["DFSI"], errors="coerce"
)
if not st.session_state.started:

    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #102A43, #078A91);
        padding: 90px 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 40px;
    ">
        <h1 style="color:white; font-size:55px;">
            🌊 FloodSense
        </h1>
        <h2 style="color:#D8F3F0;">
            Smarter Flood Monitoring. Safer Communities.
        </h2>
        <p style="color:white; font-size:18px;">
            AI-Powered Urban Flood Analysis and Early Warning System
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🌧️ Rainfall Analysis")

    with col2:
        st.info("🌊 Flood Risk Monitoring")

    with col3:
        st.info("📊 Historical Flood Analysis")

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.stop()
# ---------------- SIDEBAR ----------------

st.sidebar.markdown("""
<h2 style="color:white;">🌊 FloodSense</h2>
<p style="color:#BDE0E5;">
Your Flood Monitoring Dashboard
</p>
<hr>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Choose a section",
    [
        "Overview",
        "Rainfall Analysis",
        "Flood Risk Analysis",
        "Flood Impact",
        "Emergency Safety Assistant",
        "Citizen Flood Reporting"
    ]
)

# ---------------- OVERVIEW ----------------


    
# ==========================================
# OVERVIEW DASHBOARD
# ==========================================

if page == "Overview":

    # Prepare data
    overview_rain = rainfall.copy()
    overview_flood = flood_history.copy()
    overview_dfsi = dfsi.copy()
    overview_impact = impact.copy()

    overview_rain["Date"] = pd.to_datetime(
        overview_rain["Date"], errors="coerce"
    )

    overview_flood["Start Date"] = pd.to_datetime(
        overview_flood["Start Date"], errors="coerce"
    )

    # ==========================================
    # WELCOME BANNER
    # ==========================================

    # ==========================================
    # KEY STATISTICS
    # ==========================================

    st.subheader("📊 Dashboard Overview")

    total_rainfall = len(overview_rain)
    total_floods = len(overview_flood)
    total_districts = overview_dfsi["District"].nunique()
    total_impact = len(overview_impact)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🌧️ Rainfall Records",
        f"{total_rainfall:,}"
    )

    c2.metric(
        "🌊 Historical Flood Events",
        f"{total_floods:,}"
    )

    c3.metric(
        "📍 District Risk Records",
        f"{total_districts:,}"
    )

    c4.metric(
        "⚠️ District Impact Records",
        f"{total_impact:,}"
    )

    st.divider()

    # ==========================================
    # ABOUT FLOODSENSE
    # ==========================================

    st.subheader("🌍 About FloodSense")

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown("""
        FloodSense is an interactive flood analysis platform
        designed to explore rainfall patterns, historical flood
        events and district-level flood vulnerability.

        **Our objectives:**

        - Analyse rainfall patterns across Indian districts.
        - Explore historical flood events.
        - Identify districts with higher flood susceptibility.
        - Understand the impact of floods on people.
        - Provide location-based weather forecasts.
        """)

    with col2:

        st.markdown("""
        <div style="
            background:#E4F3F4;
            padding:22px;
            border-radius:15px;
            border-left:5px solid #087E8B;
        ">
            <h3 style="color:#164E63;">Our Mission</h3>
            <p style="color:#244B5A;">
                Use data and technology to improve flood
                awareness and support better preparedness.
            </p>
            <h3 style="color:#164E63;">Our Approach</h3>
            <p style="color:#244B5A;">
                Data analysis + Weather forecasting +
                Flood susceptibility assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    

    # ==========================================
    # DATASET SUMMARY
    # ==========================================

    st.subheader("🗂️ Data Sources Used")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("""
        <div style="background:white; padding:18px;
        border-radius:12px; border:1px solid #DCE8EF;">
            <h3>🌧️ Rainfall Data</h3>
            <p>Daily rainfall and normal rainfall
            observations from IMD.</p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div style="background:white; padding:18px;
        border-radius:12px; border:1px solid #DCE8EF;">
            <h3>🌊 Flood Inventory</h3>
            <p>Historical flood events and available
            event information.</p>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div style="background:white; padding:18px;
        border-radius:12px; border:1px solid #DCE8EF;">
            <h3>📍 District Data</h3>
            <p>Flood susceptibility, flooded areas
            and human impact information.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ==========================================
    # QUICK NAVIGATION
    # ==========================================

    st.subheader("🚀 Explore FloodSense")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.markdown("**🌧️ Rainfall Analysis**")
        st.caption("Explore rainfall and location forecasts.")

    with q2:
        st.markdown("**🌊 Flood History**")
        st.caption("Explore historical flood events.")

    with q3:
        st.markdown("**📍 Flood Risk**")
        st.caption("Compare district susceptibility.")

    with q4:
        st.markdown("**⚠️ Flood Impact**")
        st.caption("Analyse fatalities and injuries.")

    
# ---------------- RAINFALL ANALYSIS ----------------

elif page == "Rainfall Analysis":

    st.title("🌧️ Rainfall Analysis")

    st.write(
        "Explore historical rainfall records and live weather forecasts."
    )
    

    # =====================================
    # PART 1: HISTORICAL RAINFALL ANALYSIS
    # =====================================

    st.header("📊 Historical Rainfall Analysis")

    # Use the existing cleaned rainfall dataset
    rain = rainfall.copy()

    # Convert columns to correct data types
    rain["Date"] = pd.to_datetime(
        rain["Date"],
        errors="coerce"
    )

    rain["Daily Actual"] = pd.to_numeric(
        rain["Daily Actual"],
        errors="coerce"
    )

    rain["Daily Normal"] = pd.to_numeric(
        rain["Daily Normal"],
        errors="coerce"
    )

    rain = rain.dropna(
        subset=["Date", "Daily Actual"]
    )

    # State selection
    states = sorted(
        rain["State"].dropna().unique()
    )

    selected_state = st.selectbox(
        "Select State",
        states,
        key="rain_state"
    )

    state_data = rain[
        rain["State"] == selected_state
    ].copy()

    # District selection
    districts = sorted(
        state_data["District"].dropna().unique()
    )

    selected_district = st.selectbox(
        "Select District",
        districts,
        key="rain_district"
    )

    district_data = state_data[
        state_data["District"] == selected_district
    ].copy()

    # Summary metrics
    total_rainfall = district_data["Daily Actual"].sum()

    average_rainfall = district_data["Daily Actual"].mean()

    maximum_rainfall = district_data["Daily Actual"].max()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rainfall",
        f"{total_rainfall:.2f} mm"
    )

    col2.metric(
        "Average Rainfall",
        f"{average_rainfall:.2f} mm"
    )

    col3.metric(
        "Maximum Rainfall",
        f"{maximum_rainfall:.2f} mm"
    )

    # Daily rainfall trend
    st.subheader("📈 Daily Rainfall Trend")

    daily_trend = (
        district_data
        .groupby("Date")["Daily Actual"]
        .sum()
        .sort_index()
    )

    st.line_chart(daily_trend)

    # Actual versus normal rainfall
    st.subheader("🌦️ Actual vs Normal Rainfall")

    comparison = district_data[
        ["Date", "Daily Actual", "Daily Normal"]
    ].dropna()

    comparison = (
        comparison
        .groupby("Date")[
            ["Daily Actual", "Daily Normal"]
        ]
        .mean()
        .sort_index()
    )

    st.line_chart(comparison)

    # Rainfall records
    st.subheader("📋 Rainfall Records")

    st.dataframe(
        district_data.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    

        # ==========================================
        # PLACE-BASED RAINFALL AND FLOOD SCREENING
        # ==========================================

    st.divider()
    st.header("📍 Check Rainfall and Flood Risk for a Place")

    st.write(
            "Enter a city, town or district to view its "
            "weather forecast and rainfall-based flood screening."
        )

    place = st.text_input(
            "Enter your location",
            placeholder="Example: Bengaluru, Mysuru, Kochi"
        )

    if st.button("Check Weather and Flood Risk"):

            if not place.strip():
                st.warning("Please enter a location.")

            else:
                try:
                    with st.spinner("Finding location and fetching forecast..."):

                        # 1. FIND LOCATION
                        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                        geo_params = {
                            "name": place,
                            "count": 5,
                            "language": "en",
                            "format": "json"
                        }

                        geo_response = requests.get(
                            geo_url,
                            params=geo_params,
                            timeout=20
                        )

                        geo_response.raise_for_status()
                        geo_data = geo_response.json()

                        results = geo_data.get("results", [])

                        if not results:
                            st.error("Location not found. Try another place.")

                        else:
                            # Prefer Indian locations
                            india_results = [
                                x for x in results
                                if x.get("country_code") == "IN"
                            ]

                            choices = india_results if india_results else results

                            selected = choices[0]

                            latitude = selected["latitude"]
                            longitude = selected["longitude"]

                            location_name = selected["name"]
                            country = selected.get("country", "")

                            st.success(
                                f"Location found: {location_name}, {country}"
                            )

                            # 2. FETCH WEATHER FORECAST
                            weather_url = (
                                "https://api.open-meteo.com/v1/forecast"
                            )

                            weather_params = {
                                "latitude": latitude,
                                "longitude": longitude,
                                "hourly": (
                                    "precipitation_probability,"
                                    "precipitation,"
                                    "relative_humidity_2m"
                                ),
                                "daily": (
                                    "precipitation_sum,"
                                    "precipitation_probability_max,"
                                    "temperature_2m_max"
                                ),
                                "forecast_days": 7,
                                "timezone": "auto"
                            }

                            weather_response = requests.get(
                                weather_url,
                                params=weather_params,
                                timeout=30
                            )

                            weather_response.raise_for_status()
                            weather = weather_response.json()

                            daily = pd.DataFrame({
                                "Date": weather["daily"]["time"],
                                "Rainfall (mm)": weather["daily"]["precipitation_sum"],
                                "Rain Probability (%)": weather["daily"]["precipitation_probability_max"],
                                "Maximum Temperature (°C)": weather["daily"]["temperature_2m_max"]
                            })

                            daily["Date"] = pd.to_datetime(daily["Date"])

                            daily["Rainfall (mm)"] = pd.to_numeric(
                                daily["Rainfall (mm)"],
                                errors="coerce"
                            ).fillna(0)

                            daily["Rain Probability (%)"] = pd.to_numeric(
                                daily["Rain Probability (%)"],
                                errors="coerce"
                            )

                            # 3. WEATHER SUMMARY
                            total_rain = daily["Rainfall (mm)"].sum()
                            max_rain = daily["Rainfall (mm)"].max()

                            max_probability = daily[
                                "Rain Probability (%)"
                            ].max()

                            st.subheader("🌦️ 7-Day Weather Forecast")

                            c1, c2, c3 = st.columns(3)

                            c1.metric(
                                "Expected 7-Day Rainfall",
                                f"{total_rain:.1f} mm"
                            )

                            c2.metric(
                                "Maximum Daily Rainfall",
                                f"{max_rain:.1f} mm"
                            )

                            c3.metric(
                                "Highest Rain Probability",
                                f"{max_probability:.0f}%"
                                if pd.notna(max_probability)
                                else "Unavailable"
                            )

                            # 4. RAINFALL PREDICTION
                            st.subheader("🌧️ Rainfall Forecast")

                            if total_rain >= 0.1:
                                st.info(
                                    "Rainfall is forecast during the next "
                                    "7 days for this location."
                                )
                            else:
                                st.success(
                                    "No measurable rainfall is forecast "
                                    "in the next 7 days."
                                )

                            # 5. RAINFALL CHART
                            fig = px.bar(
                                daily,
                                x="Date",
                                y="Rainfall (mm)",
                                title="Expected Daily Rainfall – Next 7 Days",
                                color="Rainfall (mm)",
                                color_continuous_scale="Blues"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                            # 6. RAINFALL-BASED FLOOD SCREENING
                            st.subheader("⚠️ Rainfall-Based Flood Screening")

                            if max_rain >= 100:
                                screening = "High rainfall screening level"
                                message = (
                                    "Very heavy forecast rainfall. "
                                    "Check official local flood advisories."
                                )
                            elif max_rain >= 50:
                                screening = "Elevated rainfall screening level"
                                message = (
                                    "Heavy forecast rainfall. "
                                    "Monitor local conditions and advisories."
                                )
                            elif max_rain >= 20:
                                screening = "Rainfall watch level"
                                message = (
                                    "Moderate forecast rainfall. "
                                    "Continue monitoring weather updates."
                                )
                            else:
                                screening = "Lower rainfall screening level"
                                message = (
                                    "The forecast does not show high daily "
                                    "rainfall using these screening thresholds."
                                )

                            st.warning(
                                f"Screening result: {screening}"
                            )

                            st.write(message)

                            st.caption(
                                "This is a rainfall-only screening indicator, "
                                "not a measured flood probability or verified "
                                "flood prediction. Actual flooding also depends "
                                "on drainage, terrain, river levels, soil "
                                "conditions and local rainfall."
                            )

                            # 7. FORECAST TABLE
                            st.subheader("Complete Weather Forecast")

                            st.dataframe(
                                daily,
                                use_container_width=True
                            )

                            # 8. LOCATION DETAILS
                            st.caption(
                                f"Coordinates: {latitude}, {longitude} | "
                                "Weather source: Open-Meteo"
                            )

                except requests.exceptions.RequestException as e:
                    st.error(f"Weather service connection failed: {e}")

                except (KeyError, ValueError, TypeError) as e:
                    st.error(f"Could not process the weather forecast: {e}")


# ---------------- FLOOD IMPACT ----------------


# ---------------- FLOOD IMPACT ----------------

elif page == "Flood Impact":

    st.header("⚠️ Flood Impact Analysis")

    st.write(
        "Analyse the human impact of floods, including fatalities, "
        "injuries, population and flood duration."
    )

    impact_data = impact.copy()
    kerala_data = kerala.copy()

    # Convert numerical columns
    numeric_cols = [
        "Human_fatality",
        "Human_injured",
        "Population",
        "Mean_Flood_Duration"
    ]

    for col in numeric_cols:
        impact_data[col] = pd.to_numeric(
            impact_data[col], errors="coerce"
        )

    # ---------------- KPI CARDS ----------------

    total_fatalities = impact_data["Human_fatality"].sum()
    total_injured = impact_data["Human_injured"].sum()
    total_population = impact_data["Population"].sum()
    avg_duration = impact_data["Mean_Flood_Duration"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Recorded Fatalities", f"{total_fatalities:,.0f}")
    col2.metric("Recorded Injuries", f"{total_injured:,.0f}")
    col3.metric("Population Covered", f"{total_population:,.0f}")
    col4.metric(
        "Average Flood Duration",
        f"{avg_duration:.2f} days" if pd.notna(avg_duration) else "N/A"
    )

    st.divider()

    # ---------------- FATALITIES ----------------

    st.subheader("Top 10 Districts by Human Fatalities")

    top_fatalities = (
        impact_data.nlargest(10, "Human_fatality")
        .sort_values("Human_fatality")
    )

    fig1 = px.bar(
        top_fatalities,
        x="Human_fatality",
        y="Dist_Name",
        orientation="h",
        text="Human_fatality",
        title="District-wise Human Fatalities"
    )

    fig1.update_layout(
        xaxis_title="Number of Fatalities",
        yaxis_title="District"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ---------------- INJURIES ----------------

    st.subheader("Top 10 Districts by Human Injuries")

    top_injuries = (
        impact_data.nlargest(10, "Human_injured")
        .sort_values("Human_injured")
    )

    fig2 = px.bar(
        top_injuries,
        x="Human_injured",
        y="Dist_Name",
        orientation="h",
        text="Human_injured",
        title="District-wise Human Injuries"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------------- FLOOD DURATION ----------------

    st.subheader("Flood Duration Analysis")

    duration_data = impact_data.dropna(
        subset=["Mean_Flood_Duration"]
    )

    fig3 = px.histogram(
        duration_data,
        x="Mean_Flood_Duration",
        nbins=15,
        title="Distribution of Mean Flood Duration",
        labels={
            "Mean_Flood_Duration": "Mean Flood Duration (days)"
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()


    # ---------------- SEARCH ----------------

    st.subheader("Search District Impact")

    search = st.text_input("Enter district name")

    if search:

        result = impact_data[
            impact_data["Dist_Name"].str.contains(
                search, case=False, na=False
            )
        ]

        st.dataframe(result, use_container_width=True)

    with st.expander("View complete district impact data"):
        st.dataframe(impact_data, use_container_width=True)

    st.caption(
        "Impact statistics describe the uploaded datasets. "
        "The Kerala data and national district data are separate sources."
    )
elif page == "AI Flood Risk Prediction":

    st.title("🤖 AI Flood Risk Prediction")
    st.write(
        "Estimate district-level flood severity using "
        "historical flood indicators."
    )

    # Load datasets
    dfsi_data = pd.read_csv(
        "cleaned_data/DFSI_cleaned.csv"
    )

    flooded_data = pd.read_csv(
        "cleaned_data/District_FloodedArea_cleaned.csv"
    )

    impact_data = pd.read_csv(
        "cleaned_data/FloodImpact_cleaned.csv"
    )

    # Standardize district names for matching
    def clean_name(value):
        return str(value).strip().lower()

    dfsi_data["District_Key"] = (
        dfsi_data["District"].apply(clean_name)
    )

    flooded_data["District_Key"] = (
        flooded_data["Dist_Name"].apply(clean_name)
    )

    impact_data["District_Key"] = (
        impact_data["Dist_Name"].apply(clean_name)
    )

    # Merge district datasets
    data = pd.merge(
        dfsi_data,
        flooded_data,
        on="District_Key",
        how="inner"
    )

    data = pd.merge(
        data,
        impact_data,
        on="District_Key",
        how="inner",
        suffixes=("_area", "_impact")
    )

    # Select model features and target
    features = [
        "Percent_Flooded_Area",
        "Parmanent_Water",
        "Corrected_Percent_Flooded_Area",
        "Human_fatality",
        "Human_injured",
        "Population",
        "Mean_Flood_Duration"
    ]

    target = "DFSI"

    # Clean numeric values
    for column in features + [target]:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(subset=features + [target])

    # Train model
    if len(data) < 20:

        st.error(
            "Not enough matched district records to train "
            "a meaningful model. Check district name matching."
        )

    else:

        X = data[features]
        y = data[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = RandomForestRegressor(
            n_estimators=150,
            random_state=42
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        # Model performance
        st.subheader("📊 Model Performance")

        col1, col2, col3 = st.columns(3)

        col1.metric("Matched Districts", len(data))
        col2.metric("Mean Absolute Error", f"{mae:.2f}")
        col3.metric("R² Score", f"{r2:.2f}")

        # District selection
        st.divider()

        st.subheader("🔍 Select a District")

        district = st.selectbox(
            "Choose district",
            sorted(data["District"].dropna().unique())
        )

        selected = data[
            data["District"] == district
        ].iloc[0]

        input_data = pd.DataFrame(
            [selected[features].to_dict()]
        )

        # Prediction
        predicted_dfsi = model.predict(input_data)[0]

        st.subheader("AI Estimated DFSI")

        st.metric(
            "Estimated District Flood Severity Index",
            f"{predicted_dfsi:.2f}"
        )

        # Compare with actual DFSI
        actual_dfsi = selected["DFSI"]

        st.write(f"Historical DFSI: {actual_dfsi:.2f}")

        # Relative classification using training data
        low_limit = y_train.quantile(0.33)
        high_limit = y_train.quantile(0.67)

        if predicted_dfsi >= high_limit:
            st.error("Higher relative historical DFSI range")

        elif predicted_dfsi >= low_limit:
            st.warning("Middle relative historical DFSI range")

        else:
            st.success("Lower relative historical DFSI range")

        # Feature importance
        st.subheader("Factors Influencing the Model")

        importance = pd.DataFrame({
            "Feature": features,
            "Importance": model.feature_importances_
        }).sort_values(
            "Importance",
            ascending=False
        )

        st.bar_chart(
            importance.set_index("Feature")
        )

        st.caption(
            "This experimental model estimates DFSI from historical "
            "district indicators. It is not a live flood forecast, "
            "flood probability, or official warning. Results depend "
            "on district matching, data quality and model validation."
        )
### Early Warning Alerts ###

elif page == "Early Warning Alerts":

    st.title("🚨 Early Warning Alert System")

    st.write(
        "Monitor rainfall forecasts and generate "
        "rainfall-based warning indicators."
    )

    city = st.text_input(
        "Enter city name",
        placeholder="Example: Bengaluru"
    )

    if st.button("Check Warning Status"):

        if city.strip():

            try:
                # Find location
                geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                geo_response = requests.get(
                    geo_url,
                    params={
                        "name": city.strip(),
                        "count": 10,
                        "language": "en",
                        "format": "json"
                    },
                    timeout=15
                )

                geo_response.raise_for_status()

                results = geo_response.json().get("results", [])

                indian_results = [
                    x for x in results
                    if x.get("country") == "India"
                ]

                if indian_results:
                    place = indian_results[0]
                elif results:
                    place = results[0]
                else:
                    st.error("Location not found.")
                    st.stop()
                if results:
                    location = results[0]

                    st.write("Selected location:", location["name"])
                    st.write("Country:", location.get("country"))
                    st.write("Latitude:", location["latitude"])
                    st.write("Longitude:", location["longitude"])

                else:
                    st.error("Location not found.")
                    st.stop()

                # Get weather forecast
                weather_response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": place["latitude"],
                        "longitude": place["longitude"],
                        "daily": [
                            "precipitation_sum",
                            "precipitation_probability_max"
                        ],
                        "forecast_days": 7,
                        "timezone": "auto"
                    },
                    timeout=15
                )

                weather_response.raise_for_status()

                weather = weather_response.json()["daily"]

                forecast = pd.DataFrame({
                    "Date": weather["time"],
                    "Rainfall": weather["precipitation_sum"],
                    "Probability": weather[
                        "precipitation_probability_max"
                    ]
                })

                max_rain = forecast["Rainfall"].max()
                max_probability = forecast["Probability"].max()

                st.subheader(
                    f"📍 {place['name']}, {place.get('country', '')}"
                )

                col1, col2 = st.columns(2)

                col1.metric(
                    "Maximum Forecast Rainfall",
                    f"{max_rain:.1f} mm"
                )

                col2.metric(
                    "Maximum Rain Probability",
                    f"{max_probability:.0f}%"
                )

                st.subheader("Warning Status")

                if max_rain >= 100:
                    st.error("🔴 RED – Very Heavy Rainfall Indicator")
                    st.write(
                        "Follow official weather and local emergency "
                        "authority advisories. Avoid flood-prone areas."
                    )

                elif max_rain >= 50:
                    st.warning("🟠 ORANGE – Heavy Rainfall Indicator")
                    st.write(
                        "Monitor weather updates and check drainage "
                        "and local conditions."
                    )

                elif max_rain >= 20:
                    st.warning("🟡 YELLOW – Moderate Rainfall Indicator")
                    st.write(
                        "Stay informed and monitor rainfall conditions."
                    )

                else:
                    st.success("🟢 GREEN – Low Rainfall Indicator")
                    st.write(
                        "No heavy rainfall signal in this forecast."
                    )

                st.subheader("7-Day Rainfall Forecast")

                st.bar_chart(
                    forecast.set_index("Date")["Rainfall"]
                )

                st.dataframe(
                    forecast,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "These are project-defined rainfall thresholds, "
                    "not official government warning categories or "
                    "verified flood predictions. Check official alerts."
                )

            except requests.exceptions.RequestException as e:
                st.error(f"Weather service error: {e}")

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a city name.")

# ==========================================
# FLOOD RISK ANALYSIS
# ==========================================

elif page == "Flood Risk Analysis":

    st.title("⚠️ District-wise Flood Risk Analysis")

    st.write(
        "Explore district-level flood susceptibility indicators, "
        "flooded area and permanent water coverage."
    )

    # --------------------------------------
    # LOAD AND CLEAN DATASETS
    # --------------------------------------

    dfsi_data = dfsi.copy()
    flooded_data = flooded.copy()

    dfsi_data["DFSI"] = pd.to_numeric(
        dfsi_data["DFSI"],
        errors="coerce"
    )

    area_columns = [
        "Percent_Flooded_Area",
        "Parmanent_Water",
        "Corrected_Percent_Flooded_Area"
    ]

    for col in area_columns:
        flooded_data[col] = pd.to_numeric(
            flooded_data[col],
            errors="coerce"
        )

    dfsi_data = dfsi_data.dropna(
        subset=["District", "DFSI"]
    )

    flooded_data = flooded_data.dropna(
        subset=["Dist_Name"]
    )

    # --------------------------------------
    # SECTION 1: DFSI OVERVIEW
    # --------------------------------------

    st.header("📊 District Flood Severity Index")

    total_districts = dfsi_data["District"].nunique()

    average_dfsi = dfsi_data["DFSI"].mean()

    highest_dfsi = dfsi_data["DFSI"].max()

    highest_district = dfsi_data.loc[
        dfsi_data["DFSI"].idxmax(),
        "District"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Districts Analysed",
        f"{total_districts:,}"
    )

    col2.metric(
        "Average DFSI",
        f"{average_dfsi:.2f}"
    )

    col3.metric(
        "Highest DFSI",
        f"{highest_dfsi:.2f}"
    )

    st.info(
        f"District with the highest recorded DFSI: "
        f"**{highest_district}**."
    )

    st.divider()

    # --------------------------------------
    # SECTION 2: TOP 10 DFSI DISTRICTS
    # --------------------------------------

    st.subheader("🏆 Top 10 Districts by DFSI")

    top_dfsi = dfsi_data.nlargest(
        10,
        "DFSI"
    ).sort_values(
        "DFSI",
        ascending=True
    )

    fig1 = px.bar(
        top_dfsi,
        x="DFSI",
        y="District",
        orientation="h",
        text="DFSI",
        color="DFSI",
        color_continuous_scale="Tealgrn",
        title="Top 10 Districts by Flood Severity Index",
        labels={
            "DFSI": "District Flood Severity Index",
            "District": "District"
        }
    )

    fig1.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig1.update_layout(
        height=500,
        showlegend=False,
        yaxis_title="District",
        xaxis_title="DFSI"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.caption(
        "Higher DFSI values indicate higher values of the "
        "recorded index. Interpret the index using its original "
        "dataset methodology."
    )

    st.divider()

    # --------------------------------------
    # SECTION 3: STATE-WISE DFSI
    # --------------------------------------

    st.subheader("🗺️ State-wise DFSI Analysis")

    if "State_Name" in dfsi_data.columns:

        state_dfsi = (
            dfsi_data
            .groupby("State_Name")["DFSI"]
            .mean()
            .reset_index()
            .sort_values("DFSI", ascending=False)
        )

        fig2 = px.bar(
            state_dfsi,
            x="State_Name",
            y="DFSI",
            color="DFSI",
            color_continuous_scale="Tealgrn",
            title="Average DFSI by State",
            labels={
                "State_Name": "State",
                "DFSI": "Average DFSI"
            }
        )

        fig2.update_layout(
            xaxis_tickangle=-45,
            height=450
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "State information is not available in the DFSI dataset."
        )

    st.divider()

    # --------------------------------------
    # SECTION 4: FLOODED AREA ANALYSIS
    # --------------------------------------

    st.header("🌊 District-wise Flooded Area Analysis")

    valid_area = flooded_data.dropna(
        subset=["Corrected_Percent_Flooded_Area"]
    )

    if not valid_area.empty:

        top_area = valid_area.nlargest(
            10,
            "Corrected_Percent_Flooded_Area"
        ).sort_values(
            "Corrected_Percent_Flooded_Area"
        )

        fig3 = px.bar(
            top_area,
            x="Corrected_Percent_Flooded_Area",
            y="Dist_Name",
            orientation="h",
            text="Corrected_Percent_Flooded_Area",
            color="Corrected_Percent_Flooded_Area",
            color_continuous_scale="Blues",
            title="Top 10 Districts by Corrected Flooded Area",
            labels={
                "Dist_Name": "District",
                "Corrected_Percent_Flooded_Area":
                    "Corrected Flooded Area (%)"
            }
        )

        fig3.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig3.update_layout(
            height=500,
            showlegend=False
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    else:

        st.warning("No valid flooded-area records are available.")

    st.divider()

    # --------------------------------------
    # SECTION 5: PERMANENT WATER ANALYSIS
    # --------------------------------------

    st.subheader("💧 Permanent Water vs Flooded Area")

    scatter_data = flooded_data.dropna(
        subset=[
            "Parmanent_Water",
            "Corrected_Percent_Flooded_Area"
        ]
    )

    if not scatter_data.empty:

        fig4 = px.scatter(
            scatter_data,
            x="Parmanent_Water",
            y="Corrected_Percent_Flooded_Area",
            hover_name="Dist_Name",
            color="Corrected_Percent_Flooded_Area",
            color_continuous_scale="Blues",
            title="Permanent Water Coverage vs Corrected Flooded Area",
            labels={
                "Parmanent_Water": "Permanent Water (%)",
                "Corrected_Percent_Flooded_Area":
                    "Corrected Flooded Area (%)"
            }
        )

        fig4.update_layout(height=450)

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        st.caption(
            "This chart explores the relationship between "
            "permanent water coverage and corrected flooded area. "
            "It does not establish causation."
        )

    else:

        st.info("Not enough data for the comparison chart.")

    st.divider()

    # --------------------------------------
    # SECTION 6: DISTRICT SEARCH
    # --------------------------------------

    st.header("🔍 Search District Information")

    search = st.text_input(
        "Enter district name",
        placeholder="Search for a district..."
    )

    if search.strip():

        # Search DFSI dataset
        dfsi_result = dfsi_data[
            dfsi_data["District"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        ]

        # Search flooded area dataset
        area_result = flooded_data[
            flooded_data["Dist_Name"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.subheader("District Severity Index")

        if not dfsi_result.empty:

            st.dataframe(
                dfsi_result.drop(
                    columns=["District_Key"],
                    errors="ignore"
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No matching DFSI district found.")

        st.subheader("District Flooded Area")

        if not area_result.empty:

            st.dataframe(
                area_result,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No matching flooded-area district found.")

    # --------------------------------------
    # SECTION 7: COMPLETE DATA
    # --------------------------------------

    with st.expander("View Complete DFSI Dataset"):

        st.dataframe(
            dfsi_data,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("View Complete Flooded Area Dataset"):

        st.dataframe(
            flooded_data,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.success(
        "District flood risk analysis completed successfully."
    )

    st.caption(
        "Data sources: District Flood Severity Index and "
        "District Flooded Area datasets. These historical "
        "indicators are not real-time flood warnings."
    )

# ==========================================
# EMERGENCY SAFETY ASSISTANT
# ==========================================

elif page == "Emergency Safety Assistant":

    st.title("🆘 Flood Emergency Safety Assistant")

    st.write(
        "Practical safety guidance to help individuals "
        "and families prepare for, respond to and recover from floods."
    )

    st.info(
        "If you are in immediate danger, contact local emergency "
        "services and follow instructions from authorities."
    )

    # --------------------------------------
    # SECTION 1: SAFETY PHASES
    # --------------------------------------

    st.header("📋 Flood Safety Guide")

    tab1, tab2, tab3 = st.tabs([
        "🟢 Before a Flood",
        "🔴 During a Flood",
        "🔵 After a Flood"
    ])

    with tab1:

        st.subheader("Prepare Before Flooding")

        before_tasks = [
            "Monitor official weather forecasts and alerts.",
            "Identify safe higher ground and evacuation routes.",
            "Keep important documents in waterproof bags.",
            "Store drinking water and non-perishable food.",
            "Charge mobile phones and power banks.",
            "Prepare medicines and first-aid supplies.",
            "Keep emergency contact numbers accessible.",
            "Move important belongings to higher locations."
        ]

        for i, task in enumerate(before_tasks):
            st.checkbox(
                task,
                key=f"before_flood_{i}"
            )

        st.warning(
            "Do not wait until floodwater reaches your home "
            "to prepare for evacuation."
        )

    with tab2:

        st.subheader("Stay Safe During Flooding")

        during_tasks = [
            "Move to higher ground if flooding threatens your area.",
            "Never walk, swim or drive through floodwater.",
            "Stay away from rivers, drains and overflowing streams.",
            "Avoid touching electrical equipment in wet areas.",
            "Follow official evacuation instructions.",
            "Keep children and pets away from floodwater.",
            "Use a torch instead of candles where possible.",
            "Keep your phone available for emergency communication."
        ]

        for i, task in enumerate(during_tasks):
            st.checkbox(
                task,
                key=f"during_flood_{i}"
            )

        st.error(
            "DANGER: Never attempt to cross moving floodwater. "
            "Even shallow moving water can be dangerous."
        )

    with tab3:

        st.subheader("Stay Safe After Flooding")

        after_tasks = [
            "Return home only when authorities say it is safe.",
            "Avoid damaged buildings and unstable structures.",
            "Do not touch wet electrical equipment.",
            "Use safe or boiled water according to local advisories.",
            "Avoid contact with contaminated floodwater.",
            "Wear protective footwear and gloves during cleanup.",
            "Discard food contaminated by floodwater.",
            "Seek medical attention for injuries or illness."
        ]

        for i, task in enumerate(after_tasks):
            st.checkbox(
                task,
                key=f"after_flood_{i}"
            )

        st.info(
            "Floodwater may contain sewage, chemicals and harmful "
            "microorganisms. Avoid direct contact."
        )

    st.divider()

    # --------------------------------------
    # SECTION 2: EMERGENCY KIT
    # --------------------------------------

    st.header("🎒 Emergency Kit Checklist")

    st.write(
        "Select the essential items you have prepared."
    )

    emergency_items = [
        "Drinking water",
        "Dry food and snacks",
        "First-aid kit",
        "Regular medicines",
        "Torch and spare batteries",
        "Power bank",
        "Mobile phone charger",
        "Waterproof document pouch",
        "Extra clothes",
        "Personal hygiene supplies",
        "Whistle",
        "Emergency contact list"
    ]

    kit_col1, kit_col2 = st.columns(2)

    selected_items = []

    for i, item in enumerate(emergency_items):

        with kit_col1 if i % 2 == 0 else kit_col2:

            checked = st.checkbox(
                item,
                key=f"kit_item_{i}"
            )

            if checked:
                selected_items.append(item)

    completed = len(selected_items)
    total = len(emergency_items)

    st.progress(completed / total)

    st.write(
        f"Emergency kit preparation: {completed}/{total} items"
    )

    if completed == total:
        st.success("Your checklist is complete!")

    st.divider()

    # --------------------------------------
    # SECTION 3: EMERGENCY CONTACTS
    # --------------------------------------

    st.header("📞 Emergency Contact Information")

    st.write(
        "Keep these numbers accessible. Verify contact details "
        "with official government sources for your location."
    )

    contacts = pd.DataFrame({
        "Service": [
            "National Emergency Response",
            "Fire and Rescue",
            "Ambulance",
            "Disaster Management"
        ],
        "Contact Number": [
            "112",
            "101",
            "108",
            "1070 / 1077"
        ],
        "Purpose": [
            "Emergency assistance",
            "Fire and rescue assistance",
            "Medical emergency",
            "State / district disaster control rooms"
        ]
    })

    st.dataframe(
        contacts,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Emergency numbers and availability can vary by location. "
        "112 is India's integrated emergency response number. "
        "Verify other numbers with local authorities."
    )

    st.divider()

    # --------------------------------------
    # SECTION 4: PERSONAL EMERGENCY PLAN
    # --------------------------------------

    st.header("📝 Create Your Emergency Plan")

    with st.form("emergency_plan_form"):

        person_name = st.text_input(
            "Name",
            placeholder="Enter your name"
        )

        location = st.text_input(
            "Your city or district",
            placeholder="Example: Bengaluru"
        )

        emergency_person = st.text_input(
            "Emergency contact person"
        )

        emergency_phone = st.text_input(
            "Emergency contact phone number"
        )

        safe_place = st.text_input(
            "Identified safe place",
            placeholder="Example: Nearby designated shelter"
        )

        submitted = st.form_submit_button(
            "Create My Emergency Plan"
        )

        if submitted:

            if (
                person_name.strip()
                and location.strip()
                and emergency_person.strip()
                and emergency_phone.strip()
                and safe_place.strip()
            ):

                st.success("Emergency plan created!")

                st.write("### Your Emergency Plan")

                st.write(f"**Name:** {person_name}")

                st.write(f"**Location:** {location}")

                st.write(
                    f"**Emergency Contact:** {emergency_person}"
                )

                st.write(
                    f"**Phone:** {emergency_phone}"
                )

                st.write(
                    f"**Safe Place:** {safe_place}"
                )

                st.warning(
                    "This information is displayed only in this "
                    "session and is not permanently saved."
                )

            else:

                st.warning(
                    "Please complete all fields."
                )

    st.divider()

    # --------------------------------------
    # SECTION 5: DOWNLOAD CHECKLIST
    # --------------------------------------

    st.header("📥 Download Emergency Checklist")

    checklist_text = """
FLOODSENSE - FLOOD EMERGENCY CHECKLIST

BEFORE A FLOOD
- Monitor official weather alerts.
- Identify higher ground and evacuation routes.
- Store drinking water and food.
- Charge phones and power banks.
- Prepare medicines and documents.

DURING A FLOOD
- Move to higher ground when necessary.
- Never walk or drive through floodwater.
- Stay away from electrical equipment.
- Follow official evacuation instructions.
- Contact emergency services if in danger.

AFTER A FLOOD
- Return only when authorities say it is safe.
- Avoid contaminated water.
- Do not touch wet electrical equipment.
- Wear protective equipment during cleanup.
- Seek medical attention when necessary.

EMERGENCY CONTACTS
- National emergency number: 112
- Fire and rescue: 101
- Ambulance: 108

Verify local emergency contact numbers.
Follow official government instructions.
"""

    st.download_button(
        label="⬇️ Download Safety Checklist",
        data=checklist_text,
        file_name="FloodSense_Emergency_Checklist.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.caption(
        "FloodSense provides general preparedness guidance. "
        "Always follow official disaster-management and emergency "
        "service instructions."
    )

elif page == "Citizen Flood Reporting":

    st.title("📢 Citizen Flood Reporting")
    st.write(
        "Report flooding in your area to help build community awareness "
        "and support faster response."
    )

    # Create folder for storing reports
    os.makedirs("reports", exist_ok=True)

    REPORT_FILE = "reports/citizen_flood_reports.csv"

    # Load existing reports
    if os.path.exists(REPORT_FILE):
        reports_df = pd.read_csv(REPORT_FILE)
    else:
        reports_df = pd.DataFrame(columns=[
            "Report ID",
            "Name",
            "Phone",
            "District",
            "Area",
            "Flood Severity",
            "Water Level",
            "Description",
            "Date and Time"
        ])

    st.subheader("📝 Submit a Flood Report")

    with st.form("flood_report_form"):

        name = st.text_input("Your Name")

        phone = st.text_input("Phone Number")

        district = st.text_input("District")

        area = st.text_input("Area / Locality")

        severity = st.selectbox(
            "Flood Severity",
            ["Select severity", "Low", "Moderate", "High", "Severe"]
        )

        water_level = st.selectbox(
            "Estimated Water Level",
            [
                "Unknown",
                "Below ankle",
                "Ankle to knee",
                "Knee to waist",
                "Above waist"
            ]
        )

        description = st.text_area(
            "Describe the flood situation",
            placeholder="Mention road flooding, water entering houses, blocked drains, etc."
        )

        photo = st.file_uploader(
            "Upload Flood Photo (Optional)",
            type=["jpg", "jpeg", "png"]
        )

        agree = st.checkbox(
            "I confirm that the information provided is accurate to the best of my knowledge."
        )

        submitted = st.form_submit_button("🚨 Submit Report")

    if submitted:

        if not name.strip() or not district.strip() or not area.strip():
            st.error("Please enter your name, district and area.")

        elif severity == "Select severity":
            st.error("Please select the flood severity.")

        elif not description.strip():
            st.error("Please describe the flood situation.")

        elif not agree:
            st.warning("Please confirm the information before submitting.")

        elif phone.strip() and not phone.strip().isdigit():
            st.error("Enter a valid phone number using digits only.")

        elif phone.strip() and len(phone.strip()) != 10:
            st.error("Enter a 10-digit phone number.")

        else:
            from datetime import datetime
            import uuid

            report_id = "FS-" + uuid.uuid4().hex[:8].upper()

            new_report = {
                "Report ID": report_id,
                "Name": name.strip(),
                "Phone": phone.strip(),
                "District": district.strip(),
                "Area": area.strip(),
                "Flood Severity": severity,
                "Water Level": water_level,
                "Description": description.strip(),
                "Date and Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            new_df = pd.DataFrame([new_report])

            new_df.to_csv(
                REPORT_FILE,
                mode="a",
                header=not os.path.exists(REPORT_FILE),
                index=False
            )

            # Save uploaded photo separately
            if photo is not None:
                photo_folder = "reports/photos"
                os.makedirs(photo_folder, exist_ok=True)

                photo_path = os.path.join(
                    photo_folder,
                    report_id + "_" + photo.name
                )

                with open(photo_path, "wb") as file:
                    file.write(photo.getbuffer())

            st.success("Your flood report has been submitted successfully!")

            st.info(f"Your Report ID: {report_id}")

            st.caption(
                "Your report is stored for review. This submission does not "
                "automatically notify emergency services."
            )

            st.rerun()

    st.divider()

    # Display submitted reports
    st.subheader("📋 Community Flood Reports")

    if os.path.exists(REPORT_FILE):

        reports_df = pd.read_csv(REPORT_FILE)

        if not reports_df.empty:

            st.metric("Total Reports Submitted", len(reports_df))

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "High / Severe Reports",
                    reports_df["Flood Severity"].isin(
                        ["High", "Severe"]
                    ).sum()
                )

            with col2:
                st.metric(
                    "Districts Reporting",
                    reports_df["District"].nunique()
                )

            st.dataframe(
                reports_df.drop(columns=["Phone", "Name"]),
                use_container_width=True,
                hide_index=True
            )

            csv = reports_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download All Reports",
                data=csv,
                file_name="citizen_flood_reports.csv",
                mime="text/csv"
            )

        else:
            st.info("No citizen reports submitted yet.")

    else:
        st.info("No citizen reports submitted yet.")

st.markdown("""
<div class="footer">
    🌊 <b>FloodSense</b> 
</div>
""", unsafe_allow_html=True)
