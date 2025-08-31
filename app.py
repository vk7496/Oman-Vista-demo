import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import qrcode
from io import BytesIO

st.set_page_config(page_title="OmanVista Explorer", layout="wide")

st.title("🏝️ OmanVista: AI Tourism Explorer")

# تابع گرفتن مکان‌ها از اینترنت
def fetch_places():
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": "tourist attractions in Oman",
        "format": "json",
        "limit": 10
    }
    headers = {"User-Agent": "OmanVistaApp/1.0"}
    
    response = requests.get(url, params=params, headers=headers)

    # بررسی اینکه واقعا JSON هست یا نه
    try:
        return response.json()
    except Exception:
        st.error("⚠️ API جواب JSON نداد، احتمالا محدودیت یا خطا وجود داره.")
        st.text(response.text[:500])  # برای دیباگ
        return []

places = fetch_places()

# نمایش مکان‌ها
if places:
    st.subheader("📍 Tourist Attractions in Oman")
    for place in places:
        st.write(f"**{place.get('display_name','Unknown')}**")
    
    # نقشه
    first_lat = float(places[0]["lat"])
    first_lon = float(places[0]["lon"])
    map_osm = folium.Map(location=[first_lat, first_lon], zoom_start=6)
    
    for p in places:
        folium.Marker(
            [float(p["lat"]), float(p["lon"])],
            popup=p.get("display_name", "Unknown")
        ).add_to(map_osm)

    st_folium(map_osm, width=700, height=500)

    # QR Code برای اولین مکان
    st.subheader("📲 QR Code for Location")
    loc_url = f"https://www.openstreetmap.org/?mlat={first_lat}&mlon={first_lon}&zoom=12"
    qr = qrcode.make(loc_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Scan to view on map")

else:
    st.warning("هیچ مکانی پیدا نشد.")
