import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from io import BytesIO
import feedparser

# -------------------
# تنظیم زبان
# -------------------
lang = st.sidebar.radio("🌐 Language | اللغة", ["English", "العربية"])

# ترجمه متن‌ها
if lang == "English":
    title = "🌍 OmanVista - AI Tourism Explorer"
    subtitle = "Discover hidden attractions and cultural sites across Oman"
    search_placeholder = "Enter a city (e.g. Muscat, Salalah)"
    search_button = "Search"
    chatbot_title = "💬 AI Travel Assistant"
    map_title = "📍 Map of Attractions"
    reddit_title = "🌐 Reddit Travel Posts"
    welcome_msg = "✨ Welcome to OmanVista! Your smart AI guide to explore Oman."
elif lang == "العربية":
    title = "🌍 عمان فيستا - مستكشف السياحة بالذكاء الاصطناعي"
    subtitle = "اكتشف المعالم المخفية والمواقع الثقافية في جميع أنحاء عمان"
    search_placeholder = "أدخل مدينة (مثال: مسقط، صلالة)"
    search_button = "بحث"
    chatbot_title = "💬 مساعد السفر الذكي"
    map_title = "📍 خريطة المواقع السياحية"
    reddit_title = "🌐 منشورات السفر في ريديت"
    welcome_msg = "✨ مرحبًا بكم في عمان فيستا! دليلك الذكي لاكتشاف عمان."

# -------------------
# هدر / کاور
# -------------------
st.markdown(
    f"""
    <div style="background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
                background-size: cover; padding: 80px; border-radius: 15px;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <h3 style="color: white; text-align: center;">{subtitle}</h3>
        <p style="color: white; text-align: center; font-size:20px;">{welcome_msg}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------
# تابع گرفتن تصویر از Unsplash
# -------------------
def fetch_image(query):
    try:
        url = f"https://api.unsplash.com/photos/random?query={query}&client_id={st.secrets['UNSPLASH_ACCESS_KEY']}"
        response = requests.get(url)
        data = response.json()
        img_url = data["urls"]["regular"]
        return img_url
    except Exception as e:
        return "https://upload.wikimedia.org/wikipedia/commons/5/5d/Muscat_Oman_sunset.jpg"  # fallback

# -------------------
# جستجو شهر
# -------------------
city = st.text_input(search_placeholder, "")
if st.button(search_button):
    if city.lower() == "muscat" or city == "مسقط":
        st.image(fetch_image("Muscat Oman"), caption="Muscat - Capital of Oman")
        st.write("Muscat is known for its beautiful coastline, traditional souqs, and the Sultan Qaboos Grand Mosque.")
    elif city.lower() == "salalah" or city == "صلالة":
        st.image(fetch_image("Salalah Oman"), caption="Salalah - Green Jewel of Oman")
        st.write("Salalah is famous for its Khareef (monsoon) season, lush mountains, and frankincense history.")
    else:
        st.warning("City not found. Try Muscat or Salalah.")

# -------------------
# نقشه
# -------------------
st.subheader(map_title)
m = folium.Map(location=[20.0, 57.0], zoom_start=6)

# نمونه مارکرها
folium.Marker([23.5880, 58.3829], popup="Muscat").add_to(m)
folium.Marker([17.0194, 54.0897], popup="Salalah").add_to(m)

st_folium(m, width=700, height=450)

# -------------------
# چت‌بات ساده
# -------------------
st.subheader(chatbot_title)
user_q = st.text_input("Ask about Oman ✨ | اسأل عن عمان")
if user_q:
    if "muscat" in user_q.lower() or "مسقط" in user_q:
        st.success("Muscat is Oman’s vibrant capital, mixing tradition with modern life. 🏙️")
    elif "salalah" in user_q.lower() or "صلالة" in user_q:
        st.success("Salalah is known for its Khareef season and lush green landscapes. 🌴")
    else:
        st.info("I don’t have info about that yet. Try Muscat or Salalah 😉")

# -------------------
# Reddit RSS
# -------------------
st.subheader(reddit_title)
def fetch_reddit_posts(subreddit="Oman"):
    url = f"https://www.reddit.com/r/{subreddit}/.rss"
    feed = feedparser.parse(url)
    posts = []
    for entry in feed.entries[:5]:
        posts.append({"title": entry.title, "link": entry.link})
    return posts

posts = fetch_reddit_posts("Oman")
for p in posts:
    st.markdown(f"- [{p['title']}]({p['link']})")
