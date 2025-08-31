import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# --------------------
# Page Config
# --------------------
st.set_page_config(page_title="OmanVista AI", layout="wide")

# --------------------
# Header
# --------------------
st.title("🏝️ OmanVista: AI Tourism Explorer")
st.markdown("Discover Oman’s hidden gems with **AI-powered tourism insights** ✨")

# --------------------
# Image Slider (Carousel Simulation)
# --------------------
st.subheader("📸 Explore Oman's Beauty")

images = [
    "https://upload.wikimedia.org/wikipedia/commons/6/65/Sultan_Qaboos_Grand_Mosque_02.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/58/Wadi_Shab%2C_Oman.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0c/Muttrah_Corniche.jpg"
]

current_img = st.session_state.get("current_img", 0)
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️"):
        current_img = (current_img - 1) % len(images)
with col2:
    st.image(images[current_img], use_container_width=True)
with col3:
    if st.button("➡️"):
        current_img = (current_img + 1) % len(images)

st.session_state["current_img"] = current_img

# --------------------
# Interactive Map
# --------------------
st.subheader("🗺️ Interactive Map of Oman")

m = folium.Map(location=[23.5880, 58.3829], zoom_start=6)

places = {
    "Muscat": [23.5880, 58.3829],
    "Salalah": [17.0197, 54.0897],
    "Nizwa": [22.9333, 57.5333],
}

for place, coords in places.items():
    folium.Marker(location=coords, popup=place, tooltip=f"Explore {place}").add_to(m)

st_data = st_folium(m, width=700, height=450)

# --------------------
# AI Travel Assistant (Demo Chatbot)
# --------------------
st.subheader("🤖 Ask OmanVista AI")

faq = {
    "best time to visit": "The best time to visit Oman is from October to April when the weather is pleasant.",
    "muscat": "Muscat is famous for Sultan Qaboos Grand Mosque, Muttrah Souq, and the Royal Opera House.",
    "salalah": "Salalah is known for its Khareef season, lush green landscapes, and waterfalls.",
}

user_q = st.text_input("Ask something about Oman:")
if user_q:
    response = None
    for key, value in faq.items():
        if key in user_q.lower():
            response = value
            break
    if not response:
        response = "I’m still learning 🤓 but Oman has many hidden gems!"
    st.success(response)

# --------------------
# Tourism Data Dashboard (Mini Demo)
# --------------------
st.subheader("📊 Tourism Snapshot")

visitors = random.randint(50000, 100000)
st.metric("Monthly Visitors (est.)", f"{visitors:,}", "+12% vs last year")

colA, colB = st.columns(2)
with colA:
    st.metric("Top Destination", "Muscat")
with colB:
    st.metric("Avg. Stay Duration", "5.2 days")

st.markdown("---")
st.markdown("Made with ❤️ in Oman | Golden Bird")
