import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="OmanVista: AI Tourism Explorer", page_icon="🌍", layout="wide")

# --- Language Selector ---
lang = st.sidebar.radio("🌐 Language | اللغة", ["English", "العربية"])

# --- Translation Dict ---
texts = {
    "title": {"English": "OmanVista: AI Tourism Explorer", "العربية": "عمان فيستا: مستكشف السياحة بالذكاء الاصطناعي"},
    "subtitle": {
        "English": "Discover the hidden gems of Oman with the power of Artificial Intelligence",
        "العربية": "اكتشف الكنوز الخفية في عمان بقوة الذكاء الاصطناعي"
    },
    "explore": {"English": "Explore", "العربية": "اكتشف"},
    "attractions": {"English": "Top Recommended Attractions in Oman", "العربية": "أفضل المعالم السياحية في عمان"},
}

# --- Sidebar Menu ---
st.sidebar.title(texts["explore"][lang])
menu = st.sidebar.radio("", ["🏞️ Attractions", "🗺️ Map View", "📊 Insights"])

# --- Main Title ---
st.markdown(f"<h1 style='text-align: center;'>{texts['title'][lang]}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size:18px;'>{texts['subtitle'][lang]}</p>", unsafe_allow_html=True)
st.write("---")

# --- Attractions Data ---
places = [
    {
        "name": {"English": "Wadi Shab", "العربية": "وادي شاب"},
        "desc": {"English": "A beautiful valley with turquoise pools and waterfalls.",
                 "العربية": "وادي جميل مع برك زمردية وشلالات."},
        "img": "images/wadishab.jpg"
    },
    {
        "name": {"English": "Jebel Akhdar", "العربية": "الجبل الأخضر"},
        "desc": {"English": "The Green Mountain, famous for terraced farms and cool weather.",
                 "العربية": "الجبل الأخضر، مشهور بالمزارع المدرجة والطقس البارد."},
        "img": "images/jebelakhdar.jpg"
    },
    {
        "name": {"English": "Muttrah Corniche", "العربية": "كورنيش مطرح"},
        "desc": {"English": "A scenic promenade along the sea with souqs and cafes.",
                 "العربية": "كورنيش خلاب على البحر مع أسواق ومقاهي."},
        "img": "images/muttrah.jpg"
    }
]

# --- Attractions Page ---
if menu == "🏞️ Attractions":
    st.subheader(texts["attractions"][lang])
    for place in places:
        st.markdown(f"### 🌟 {place['name'][lang]}")
        st.write(place["desc"][lang])
        st.image(place["img"], caption=place["name"][lang], use_container_width=True)
        st.write("---")
