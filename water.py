import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------
# Dummy Data Simulation
# -----------------------
np.random.seed(42)
dates = pd.date_range(datetime.today() - timedelta(days=30), periods=30, freq="D")
daily_consumption = np.random.randint(200, 500, size=30)  # liters
electricity_hours = np.random.uniform(1, 4, size=30)  # hours per day
electricity_units = electricity_hours * 1.5  # simple multiplier

df = pd.DataFrame({
    "date": dates,
    "consumption": daily_consumption,
    "electricity_hours": electricity_hours,
    "electricity_units": electricity_units
})

# Current status (simulate)
tank_levels = {"Main Tank": 1, "Linked Tank": 0.22, "Linked Tank 2": 0.56}  # percentage fill
flow_rate = 0.8  # simulate flow
flow_threshold = 0.5

# -----------------------
# Streamlit Layout
# -----------------------
st.set_page_config(page_title="Water Monitoring Dashboard", layout="wide")

st.title("💧 Water Monitoring Dashboard")

# -----------------------
# Tank Visualizations (HTML-based realistic tanks)
# -----------------------
def render_tank(level, tank_height=300, tank_name="Tank"):
    # level = fraction 0.0 → empty, 1.0 → full
    percent = int(level * 100)
    pixel_height = int(tank_height)  # proportional tank height

    color = "#151e3d"  # denim
    if percent < 30:
        color = "#52b2bf"  # sapphire
    elif percent < 60:
        color = "#3944bc"  # blue

    tank_html = f"""
    <div style="position: relative; width: 180px; height: {pixel_height}px; border: 4px solid #333; border-radius: 20px; overflow: hidden; background: #f9fafb; margin: 10px auto;">
        <!-- Water Fill -->
        <div style="position: absolute; bottom: 0; width: 100%; height: {percent}%;
             background: {color};
             background: linear-gradient(to top, {color}, #e0f7ff);
             transition: height 1s ease;">
        </div>
        
        <!-- Percentage Label -->
        <div style="position: absolute; top: 40%; width: 100%; text-align: center; font-size: 22px; font-weight: bold; color: black;">
            {percent}%
        </div>

        <!-- Side Markers -->
        <div style="position: absolute; left: -40px; top: 5%; height: 90%; display: flex; flex-direction: column; justify-content: space-between; font-size: 14px; color: #333;">
            <span>100%</span><span>75%</span><span>50%</span><span>25%</span><span>0%</span>
        </div>

        <!-- Tank Label -->
        <div style="position: absolute; bottom: -30px; width: 100%; text-align: center; font-size: 16px; font-weight: bold;">
            {tank_name}
        </div>
    </div>
    """

    st.components.v1.html(tank_html, height=pixel_height + 60)

st.subheader("🚰 Tank Levels")

cols = st.columns(len(tank_levels))
for i, (tank, level) in enumerate(tank_levels.items()):
    with cols[i]:
        # Example: different heights for tanks
        tank_height = 360 if "Main" in tank else 500
        render_tank(level, tank_height=tank_height, tank_name=tank)

# -----------------------
# Plots of Consumption
# -----------------------
st.subheader("📈 Water Consumption Trends")

time_range = st.radio("Select View:", ["Daily", "Weekly", "Monthly"], horizontal=True)

if time_range == "Daily":
    data = df.set_index("date")["consumption"]
elif time_range == "Weekly":
    data = df.set_index("date")["consumption"].resample("W").sum()
else:  # Monthly
    data = df.set_index("date")["consumption"].resample("M").sum()

st.line_chart(data)

# -----------------------
# Electricity Usage
# -----------------------
st.subheader("⚡ Electricity Usage")
today = df.iloc[-1]
st.metric("Pump Hours Today", f"{today['electricity_hours']:.2f} hrs")
st.metric("Electricity Units Today", f"{today['electricity_units']:.2f} kWh")

# -----------------------
# Alerts
# -----------------------
st.subheader("🚨 Alerts")

if flow_rate < flow_threshold:
    st.warning("⚠️ Bore Alarm: Flow rate decreased, possible leakage!")

for tank, level in tank_levels.items():
    if level < 0.25:
        st.error(f"🚨 Critical Alarm: {tank} is below 20%!")

# Leak detection logic: sudden spike
if df["consumption"].iloc[-1] > df["consumption"].mean() * 1.5:
    st.error("💧 Leak Detection: Abnormal consumption detected!")

# set dynamic critical points acc to tank size too