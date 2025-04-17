import streamlit as st
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Auto-refresh the app every 3 seconds
st_autorefresh(interval=3000, key="telemetry-refresh")

# Simulate telemetry data
def generate_telemetry():
    return {
        "battery": round(random.uniform(9.0, 12.6), 2),
        "temperature": round(random.uniform(20, 50), 2),
        "altitude": round(random.uniform(10, 500), 2),
        "roll": round(random.uniform(-180, 180), 2),
        "pitch": round(random.uniform(-90, 90), 2),
        "yaw": round(random.uniform(0, 360), 2),
        "gps": {
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6),
        },
        "connection": random.choice(["Excellent", "Good", "Poor", "No Signal"])
    }

# Streamlit page config
st.set_page_config(page_title="Drone Status Monitoring", layout="wide")
st.title("🚁 Drone Status Monitoring Dashboard")

data = generate_telemetry()

# --- Gauges for Battery, Temperature, Altitude ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔋 Battery Voltage (V)")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data["battery"],
        gauge={"axis": {"range": [0, 13]},
               "bar": {"color": "lightblue"},
               "steps": [
                   {"range": [0, 9], "color": "red"},
                   {"range": [9, 11], "color": "orange"},
                   {"range": [11, 13], "color": "green"}
               ]},
        title={"text": "Battery Voltage"}
    ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌡️ Temperature (°C)")
    st.metric(label="Temp", value=data["temperature"])

with col3:
    st.subheader("📶 Altitude (m)")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data["altitude"],
        gauge={"axis": {"range": [0, 600]}, "bar": {"color": "lightgreen"}},
        title={"text": "Altitude"}
    ))
    st.plotly_chart(fig, use_container_width=True)

# --- IMU and GPS ---
st.markdown("---")
col4, col5 = st.columns(2)

with col4:
    st.subheader("🧭 IMU Sensor Data")
    st.metric("Roll", f"{data['roll']}°")
    st.metric("Pitch", f"{data['pitch']}°")
    st.metric("Yaw", f"{data['yaw']}°")

with col5:
    st.subheader("📍 GPS Coordinates")
    st.metric("Latitude", data["gps"]["lat"])
    st.metric("Longitude", data["gps"]["lon"])

# --- Connection Health ---
st.markdown("---")
st.subheader("📡 Connection Health")
if data["connection"] == "Excellent":
    st.success("Excellent")
elif data["connection"] == "Good":
    st.info("Good")
elif data["connection"] == "Poor":
    st.warning("Poor")
else:
    st.error("No Signal")

# --- Footer ---
st.markdown("---")
st.caption("🌐 Live Simulated Drone Data | Streamlit-based Web App")
