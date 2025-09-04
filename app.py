import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="OmanVista Demo", layout="wide")

# -------------------
# Header with background
# -------------------
st.markdown(
    """
    <div style="background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5d/Muscat_Oman_sunset.jpg');
                background-size: cover; padding: 60px; border-radius: 15px;">
        <h1 style="color: white; text-align: center;">🌍 OmanVista - AI Tourism Explorer</h1>
        <h3 style="color: white; text-align: center;">Discover hidden gems of Oman</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------
# Simple test image
# -------------------
st.subheader("Test Image from Wikipedia (No API)")
st.image("https://upload.wikimedia.org/wikipedia/commons/f/f4/Muscat_City.jpg", caption="Muscat - Capital of Oman")

# -------------------
# Map with markers
# -------------------
st.subheader("📍 Map of Attractions")
m = folium.Map(location=[20.0, 57.0], zoom_start=6)
folium.Marker([23.5880, 58.3829], popup="Muscat").add_to(m)
folium.Marker([17.0194, 54.0897], popup="Salalah").add_to(m)
st_folium(m, width=700, height=450)
