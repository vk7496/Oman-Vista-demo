import streamlit as st
import folium
from streamlit_folium import st_folium
import feedparser

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
    rss_title = "📰 Latest from Reddit"
elif lang == "العربية":
    title = "🌍 عمان فيستا - مستكشف السياحة بالذكاء الاصطناعي"
    subtitle = "اكتشف المعالم المخفية والمواقع الثقافية في جميع أنحاء عمان"
    search_placeholder = "أدخل مدينة (مثال: مسقط، صلالة)"
    search_button = "بحث"
    map_title = "📍 خريطة المواقع السياحية"
    chatbot_title = "💬 مساعد السفر الذكي"
    rss_title = "📰 آخر الأخبار من ريديت"

# -------------------
# بک‌گراند خوش‌آمدگویی
# -------------------
st.markdown(
    f"""
    <div style="background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5d/Muscat_Oman_sunset.jpg');
                background-size: cover; padding: 60px; border-radius: 15px;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <h3 style="color: white; text-align: center;">{subtitle}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------
# معرفی شهرها
# -------------------
city = st.text_input(search_placeholder, "")
if st.button(search_button):
    if city.lower() in ["muscat", "مسقط"]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/f/f4/Muscat_City.jpg",
                 caption="Muscat - Capital of Oman | مسقط - عاصمة عمان")
        st.write("Muscat is known for its coastline, souqs, and Sultan Qaboos Grand Mosque. "
                 "مسقط تشتهر بساحلها الجميل وأسواقها التقليدية ومسجد السلطان قابوس.")
    elif city.lower() in ["salalah", "صلالة"]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/6d/Salalah_beach.jpg",
                 caption="Salalah - Green Jewel of Oman | صلالة - جوهرة عمان الخضراء")
        st.write("Salalah is famous for its Khareef season, mountains, and frankincense history. "
                 "صلالة تشتهر بموسم الخريف وجبالها وتاريخ اللبان.")
    else:
        st.warning("City not found | لم يتم العثور على المدينة")

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
user_q = st.text_input("Ask / اسأل ✨")
if user_q:
    if "muscat" in user_q.lower() or "مسقط" in user_q:
        st.success("Muscat is Oman’s capital, mixing tradition and modern life. 🏙️ | "
                   "مسقط هي عاصمة عمان، تمزج بين الأصالة والحياة العصرية.")
    elif "salalah" in user_q.lower() or "صلالة" in user_q:
        st.success("Salalah is known for Khareef season and green landscapes. 🌴 | "
                   "صلالة مشهورة بموسم الخريف ومناظرها الطبيعية الخضراء.")
    else:
        st.info("I don’t have info about that yet 😉 | لا توجد لدي معلومات بعد 😉")

# -------------------
# Reddit RSS
# -------------------
st.subheader(rss_title)

rss_url = "https://www.reddit.com/r/Oman/.rss"
feed = feedparser.parse(rss_url)

for entry in feed.entries[:5]:
    st.markdown(f"🔗 [{entry.title}]({entry.link})")
