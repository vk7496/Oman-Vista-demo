import streamlit as st
import folium
from streamlit_folium import st_folium

# صفحه تنظیمات
st.set_page_config(page_title="OmanVista Explorer", layout="wide")

st.title("🏞️ OmanVista: AI Tourism Explorer")
st.markdown("Explore hidden gems of Oman with interactive maps and images 🌍")

# جاذبه‌های گردشگری عمان
places = [
    {
        "name": "Wadi Shab",
        "desc": "A stunning canyon with turquoise pools and hidden waterfalls.",
        "lat": 22.834, "lon": 59.243,
        "img": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Wadi_Shab_Oman.jpg"
    },
    {
        "name": "Jebel Akhdar",
        "desc": "The Green Mountain, famous for its terraces and cool climate.",
        "lat": 23.072, "lon": 57.665,
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Jebel_Akhdar_Oman.jpg"
    },
    {
        "name": "Muttrah Corniche",
        "desc": "A lively waterfront with souks, cafes, and sea views in Muscat.",
        "lat": 23.619, "lon": 58.593,
        "img": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Muttrah_Corniche_Oman.jpg"
    }
]

# انتخاب مکان
place_names = [p["name"] for p in places]
choice = st.selectbox("Choose a destination to explore:", place_names)

# مکان انتخابی
selected = next(p for p in places if p["name"] == choice)

# نمایش توضیحات و تصویر
st.subheader(f"📍 {selected['name']}")
st.write(selected["desc"])
st.image(selected["img"], use_container_width=True)

# نمایش نقشه
st.subheader("🗺️ Interactive Map")
m = folium.Map(location=[selected["lat"], selected["lon"]], zoom_start=10)
folium.Marker([selected["lat"], selected["lon']], popup=selected["name"]).add_to(m)

st_data = st_folium(m, width=700, height=500)

