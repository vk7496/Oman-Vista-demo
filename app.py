import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# -----------------------------
# عنوان و توضیحات
# -----------------------------
st.set_page_config(page_title="OmanVista: AI Tourism Explorer", layout="wide")

st.title("🏝️ OmanVista: AI Tourism Explorer")
st.markdown("با این اپ می‌تونی جاذبه‌های گردشگری عمان رو روی نقشه ببینی و اطلاعات رو مستقیم از اینترنت دریافت کنی 🌍")

# -----------------------------
# گرفتن دیتای گردشگری از اینترنت (نمونه با API ویکی‌پدیا)
# -----------------------------
def fetch_places(query="tourist attractions in Oman"):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=5&namespace=0&format=json"
    response = requests.get(url)
    data = response.json()
    
    places = []
    for i in range(len(data[1])):
        places.append({
            "name": data[1][i],
            "desc": data[2][i],
            "link": data[3][i],
            # جای لوکیشن واقعی میشه بعدا از API دیگه گرفت (الان فقط مسقط به صورت پیش‌فرض)
            "lat": 23.5880,
            "lon": 58.3829
        })
    return places

places = fetch_places()

# -----------------------------
# انتخاب جاذبه
# -----------------------------
place_names = [p["name"] for p in places]
selected_name = st.selectbox("یک مکان گردشگری انتخاب کن:", place_names)

selected = next(p for p in places if p["name"] == selected_name)

# -----------------------------
# نمایش اطلاعات
# -----------------------------
st.subheader(f"ℹ️ معرفی: {selected['name']}")
st.write(selected["desc"])
st.markdown(f"[🔗 اطلاعات بیشتر در ویکی‌پدیا]({selected['link']})")

# -----------------------------
# نقشه تعاملی
# -----------------------------
st.subheader("🗺️ Interactive Map")

m = folium.Map(location=[selected["lat"], selected["lon"]], zoom_start=7)

# مارکر درست‌شده (بدون ارور کوتیشن)
folium.Marker(
    [selected["lat"], selected["lon"]],
    popup=selected["name"]
).add_to(m)

st_data = st_folium(m, width=700, height=500)
