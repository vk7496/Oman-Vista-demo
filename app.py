import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import feedparser

# -------------------
# تنظیمات API
# -------------------
PEXELS_API = "YOUR_PEXELS_API_KEY"
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_API_KEY"

# -------------------
# تابع برای گرفتن عکس از Pexels
# -------------------
def fetch_pexels(query):
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data["photos"]:
                return data["photos"][0]["src"]["large"]
    except:
        return None
    return None

# -------------------
# تابع برای گرفتن عکس از Unsplash
# -------------------
def fetch_unsplash(query):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data["results"]:
                return data["results"][0]["urls"]["regular"]
    except:
        return None
    return None

# -------------------
# زبان
# -------------------
lang = st.sidebar.radio("🌐 Language | اللغة", ["English", "العربية"])

if lang == "English":
    title = "🌍 OmanVista - AI Tourism Explorer"
    subtitle = "Discover hidden attractions and cultural sites across Oman"
    search_placeholder = "Enter a city (e.g. Muscat, Salalah)"
    search_button = "Search"
    map_title = "📍 Map of Attractions"
    chatbot_title = "💬 AI Travel Assistant"
    reddit_title = "📰 Latest from Reddit"
elif lang == "العربية":
    title = "🌍 عمان فيستا - مستكشف السياحة بالذكاء الاصطناعي"
    subtitle = "اكتشف المعالم المخفية والمواقع الثقافية في جميع أنحاء عمان"
    search_placeholder = "أدخل مدينة (مثال: مسقط، صلالة)"
    search_button = "بحث"
    map_title = "📍 خريطة المواقع السياحية"
    chatbot_title = "💬 مساعد السفر الذكي"
    reddit_title = "📰 آخر الأخبار من ريديت"

# -------------------
# هدر با بک‌گراند
# -------------------
st.markdown(
    f"""
    <div style="background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5d/Muscat_Oman_sunset.jpg');
                background-size: cover; padding: 70px; border-radius: 15px;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <h3 style="color: white; text-align: center;">{subtitle}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------
# جستجو شهر
# -------------------
city = st.text_input(search_placeholder, "")
if st.button(search_button):
    img_url = fetch_pexels(city) or fetch_unsplash(city)
    if img_url:
        st.image(img_url, caption=city.title(), use_container_width=True)
        if city.lower() == "muscat":
            st.write("Muscat is known for its coastline, souqs, and Sultan Qaboos Grand Mosque.")
        elif city.lower() == "salalah":
            st.write("Salalah is famous for its Khareef season, lush mountains, and frankincense history.")
        else:
            st.write(f"Showing results for {city}")
    else:
        st.warning("⚠️ No image found. Try another city.")

# -------------------
# نقشه
# -------------------
st.subheader(map_title)
m = folium.Map(location=[20.0, 57.0], zoom_start=6)
folium.Marker([23.5880, 58.3829], popup="Muscat").add_to(m)
folium.Marker([17.0194, 54.0897], popup="Salalah").add_to(m)
st_folium(m, width=700, height=450)

# -------------------
# چت‌بات ساده
# -------------------
st.subheader(chatbot_title)
q = st.text_input("Ask about Oman ✨ | اسأل عن عمان")
if q:
    if "muscat" in q.lower() or "مسقط" in q:
        st.success("Muscat is Oman’s vibrant capital 🏙️ blending tradition with modern life.")
    elif "salalah" in q.lower() or "صلالة" in q:
        st.success("Salalah is known for its Khareef 🌴 and lush green landscapes.")
    else:
        st.info("I don’t have info yet. Try Muscat or Salalah 😉")

# -------------------
# Reddit News (RSS)
# -------------------
st.subheader(reddit_title)
feeds = ["https://www.reddit.com/r/oman/.rss", "https://www.reddit.com/r/travel/.rss"]

for f in feeds:
    feed = feedparser.parse(f)
    st.markdown(f"#### {f}")
    for entry in feed.entries[:3]:
        st.markdown(f"- [{entry.title}]({entry.link})")
