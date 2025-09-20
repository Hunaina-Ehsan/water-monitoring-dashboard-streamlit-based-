import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------
# Dummy Data
# -----------------------
np.random.seed(42)
dates = pd.date_range(datetime.today() - timedelta(days=30), periods=30, freq="D")
df = pd.DataFrame({
    "date": dates,
    "consumption": np.random.randint(200, 500, size=30),
    "electricity_hours": np.random.uniform(1, 4, size=30)
})
df["electricity_units"] = df["electricity_hours"] * 1.5

# -----------------------
# Tank Data (can be 1, 2, 3+)
# -----------------------
tanks = [
    {"name": "Main Tank", "level": 1.0, "height": 2.5, "width": 1.2, "depth": 1.2},
    {"name": "Linked Tank", "level": 0.22, "height": 2.0, "width": 1.0, "depth": 1.0},
    {"name": "Linked Tank 2", "level": 0.56, "height": 2.2, "width": 1.1, "depth": 1.3},
]

flow_rate = 0.8
flow_threshold = 0.5

# -----------------------
# Streamlit Layout
# -----------------------
st.set_page_config(page_title="Water Monitoring Dashboard", layout="wide")
st.title("💧 Water Monitoring Dashboard")

# -----------------------
# Tank Renderer
# -----------------------
def render_tank(level, tank_name="Tank", size=1.0, specs=None, active=False, show_specs=False):
    percent = int(level * 100)
    width = int(180 * size)
    height = int(200 * size)



    color = "#151e3d"
    if percent < 30:
        color = "#52b2bf"
    elif percent < 60:
        color = "#3944bc"

    opacity = 1.0 if active else 0.4
    border_color = "#111" if active else "#888"

    tank_html = f"""
    <div style="position: relative; width: {width}px; height: {height}px; 
                border: 4px solid {border_color}; border-radius: 10px; 
                overflow: hidden; background: #f9fafb; margin: 10px auto; 
                opacity: {opacity}; transition: all 0.5s ease;">
        <div style="position: absolute; bottom: 0; width: 100%; height: {percent}%;
             background: linear-gradient(to top, {color}, #e0f7ff);">
        </div>
        <div style="position: absolute; top: 40%; width: 100%; 
                    text-align: center; font-size: {int(18*size)}px; 
                    font-weight: bold; color: black;">
            {percent}%
        </div>
        <div style="position: absolute; bottom: -25px; width: 100%; 
                    text-align: center; font-size: {int(14*size)}px; font-weight: bold;">
            {tank_name}
        </div>
    </div>
    """

    # If specs should be shown (for active tank), display them separately
    if show_specs and specs:
        specs_html = f"""
        <div style="margin-top:10px; text-align:center; font-size:14px; color:#444;">
            <b>Height:</b> {specs['height']}m &nbsp; | 
            <b>Width:</b> {specs['width']}m &nbsp; | 
            <b>Depth:</b> {specs['depth']}m
        </div>
        """
        tank_html += specs_html

    return tank_html


# -----------------------
# Tank Carousel (1, 2, or 3+)
# -----------------------
st.subheader("🚰 Tank Levels")

if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = 0

n_tanks = len(tanks)

if n_tanks == 1:
    # Just one tank
    st.components.v1.html(render_tank(
        tanks[0]["level"], tank_name=tanks[0]["name"], size=1.2, specs=tanks[0], active=True, show_specs=True
    ), height=320, scrolling=True)

elif n_tanks == 2:
    # Two tanks side by side
    c1, c2 = st.columns(2)
    with c1:
        st.components.v1.html(render_tank(
            tanks[0]["level"], tank_name=tanks[0]["name"], size=1.0, specs=tanks[0], active=True, show_specs=True
        ), height=280, scrolling=True)
    with c2:
        st.components.v1.html(render_tank(
            tanks[1]["level"], tank_name=tanks[1]["name"], size=1.0, specs=tanks[1], active=True, show_specs=True
        ), height=280, scrolling=True)

else:
    # Normal carousel (≥3 tanks)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Prev"):
            st.session_state.selected_idx = (st.session_state.selected_idx - 1) % n_tanks
    with col3:
        if st.button("Next ➡️"):
            st.session_state.selected_idx = (st.session_state.selected_idx + 1) % n_tanks

    center_idx = st.session_state.selected_idx
    left_idx = (center_idx - 1) % n_tanks
    right_idx = (center_idx + 1) % n_tanks

    c1, c2, c3 = st.columns([1,2,1])
    with c1:
        st.components.v1.html(render_tank(
            tanks[left_idx]["level"], tanks[left_idx]["name"], size=0.7, specs=tanks[left_idx]
        ), height=220)
    with c2:
        st.components.v1.html(render_tank(
            tanks[center_idx]["level"], tanks[center_idx]["name"], size=1.2, specs=tanks[center_idx], active=True, show_specs=True
        ), height=320, scrolling=True)
    with c3:
        st.components.v1.html(render_tank(
            tanks[right_idx]["level"], tanks[right_idx]["name"], size=0.7, specs=tanks[right_idx]
        ), height=220)

# -----------------------
# Water Consumption Trends
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

def metric_card(title, value, color="#006e81"):
    card_html = f"""
    <div style="background:{color}; color:white; padding:20px; 
                border-radius:15px; text-align:center; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin:10px;">
        <h4 style="margin:0; font-size:18px;">{title}</h4>
        <p style="margin:10px 0 0; font-size:22px; font-weight:bold;">{value}</p>
    </div>
    """
    return card_html

today = df.iloc[-1]
cols = st.columns(3)
with cols[0]:
    st.markdown(metric_card("Pump Hours Today", f"{today['electricity_hours']:.2f} hrs"), unsafe_allow_html=True)
with cols[1]:
    st.markdown(metric_card("Electricity Units Today", f"{today['electricity_units']:.2f} kWh"), unsafe_allow_html=True)
#with cols[2]:
#    st.markdown(metric_card("⚙️ Placeholder", "Add param"), unsafe_allow_html=True)

# -----------------------
# Alerts
# -----------------------
st.subheader("🚨 Alerts")

if flow_rate < flow_threshold:
    st.warning("⚠️ Bore Alarm: Flow rate decreased, possible leakage!")

for tank in tanks:
    if tank["level"] < 0.25:
        st.error(f"🚨 Critical Alarm: {tank['name']} is below 25%!")

if df["consumption"].iloc[-1] > df["consumption"].mean() * 1.5:
    st.error("💧 Leak Detection: Abnormal consumption detected!")
