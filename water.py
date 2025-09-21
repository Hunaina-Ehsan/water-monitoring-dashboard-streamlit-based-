import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------
# Make entire background black
# -----------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

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
# Tank Data
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

# Main Title (different style than subheaders)
st.markdown("""
    <div style="
        text-align:center; 
        font-size:38px; 
        font-weight:bold; 
        background: linear-gradient(90deg, #ff00ff, #00f6ff); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0,246,255,0.6);
        margin-bottom: 30px;
    ">
        Smart Water Monitoring System
    </div>
""", unsafe_allow_html=True)

# Function for neon subheaders
def neon_subheader(text):
    st.markdown(f"""
    <h1 style="
        text-align:center; 
        color:#00f6ff; 
        padding:15px; 
        border: 3px solid #00f6ff; 
        border-radius: 12px; 
        box-shadow: 0 0 20px #00f6ff, inset 0 0 10px #00f6ff;
        font-family: 'Trebuchet MS', sans-serif;
        ">
        {text}
    </h1>
""", unsafe_allow_html=True)



# -----------------------
# Tank Renderer
# -----------------------
def render_tank(level, tank_name="Tank", specs=None):
    percent = int(level * 100)
    color = "#151e3d"
    if percent < 30:
        color = "#52b2bf"
    elif percent < 60:
        color = "#3944bc"

    tank_html = f"""
    <div style="position: relative; width: 200px; height: 260px; 
                border: 4px solid #333; border-radius: 10px; 
                overflow: hidden; background: #f9fafb; margin: 20px auto;">
        <div style="position: absolute; bottom: 0; width: 100%; height: {percent}%;
             background: linear-gradient(to top, {color}, #e0f7ff);">
        </div>
        <div style="position: absolute; top: 40%; width: 100%; 
                    text-align: center; font-size: 22px; font-weight: bold; color: black;">
            {percent}%
        </div>
        <div style="position: absolute; bottom: -30px; width: 100%; 
                    text-align: center; font-size: 18px; font-weight: bold;">
            {tank_name}
        </div>
    </div>
    """
    if specs:
        tank_html += f"""
        <div style="margin-top:10px; text-align:center; font-size:14px; color:#444;">
            <b>Height:</b> {specs['height']}m &nbsp; | 
            <b>Width:</b> {specs['width']}m &nbsp; | 
            <b>Depth:</b> {specs['depth']}m
        </div>
        """
    return tank_html


# -----------------------
# Tank Carousel with Swipe
# -----------------------
neon_subheader("Tank Levels")

if len(tanks) == 1:
    st.components.v1.html(render_tank(tanks[0]["level"], tanks[0]["name"], specs=tanks[0]),
                          height=350, scrolling=False)
else:
    slides = "".join([
        f"<div class='swiper-slide'>{render_tank(t['level'], t['name'], specs=t)}</div>"
        for t in tanks
    ])

    carousel_html = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper/swiper-bundle.min.css" />
    <div class="swiper-container" style="width:100%; height:400px;">
      <div class="swiper-wrapper">
        {slides}
      </div>
      <div class="swiper-pagination"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper/swiper-bundle.min.js"></script>
    <script>
      var swiper = new Swiper('.swiper-container', {{
        loop: true,
        pagination: {{
          el: '.swiper-pagination',
          clickable: true,
        }},
        slidesPerView: 1,
        centeredSlides: true,
      }});
    </script>
    """

    st.components.v1.html(carousel_html, height=450, scrolling=False)


# -----------------------
# Water Consumption Trends
# -----------------------
import altair as alt

neon_subheader("Water Consumption Trends")
time_range = st.radio("Select View:", ["Daily", "Weekly", "Monthly"], horizontal=True)

if time_range == "Daily":
    data = df.set_index("date")["consumption"]
elif time_range == "Weekly":
    data = df.set_index("date")["consumption"].resample("W").sum()
else:
    data = df.set_index("date")["consumption"].resample("M").sum()

chart_data = data.reset_index()

chart = (
    alt.Chart(chart_data)
    .mark_line(color="deepskyblue")
    .encode(
        x="date:T",
        y="consumption:Q"
    )
    .properties(
        width="container",
        height=400,
        background="black"   # <-- black background
    )
    .configure_axis(
        grid=False,
        labelColor="white",
        titleColor="white"
    )
    .configure_view(
        strokeWidth=0,
        fill="black"         # inner plot bg
    )
)

st.altair_chart(chart, use_container_width=True)

# -----------------------
# Electricity Usage
# -----------------------
neon_subheader(" Electricity Usage")

def metric_card(title, value, color="#006e81"):
    return f"""
    <div style="
        background:{color};
        color:white;
        padding:16px;
        border-radius:12px;
        text-align:center;
        box-shadow:0 4px 8px rgba(0,0,0,0.2);
        flex:1;
        min-width:140px;      
        max-width:320px;      
    ">
        <h4 style="margin:0; font-size:16px;">{title}</h4>
        <p style="margin:8px 0 0; font-size:20px; font-weight:bold;">{value}</p>
    </div>
    """

today = df.iloc[-1]

cards_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
.container {{
    display: flex;
    flex-wrap: wrap;         /* allows wrapping on small screens */
    gap: 12px;               /* horizontal spacing */
    justify-content: flex-start;
}}
.card {{
    flex: 1;
}}
</style>
</head>
<body>
<div class="container">
    {metric_card("Pump Hours Today", f"{today['electricity_hours']:.2f} hrs")}
    {metric_card("Electricity Units Today", f"{today['electricity_units']:.2f} kWh")}
</div>
</body>
</html>
"""

# ✅ Use components with enough height so visuals render fully
st.components.v1.html(cards_html, height=200)




# -----------------------
# Alerts
# -----------------------
neon_subheader("Alerts")

if flow_rate < flow_threshold:
    st.warning("⚠️ Bore Alarm: Flow rate decreased, possible leakage!")

for tank in tanks:
    if tank["level"] < 0.25:
        st.error(f"🚨 Critical Alarm: {tank['name']} is below 25%!")

if df["consumption"].iloc[-1] > df["consumption"].mean() * 1.5:
    st.error("💧 Leak Detection: Abnormal consumption detected!")
