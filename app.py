import streamlit as st
from PIL import Image

# ---------- Page Config ----------
st.set_page_config(
    page_title="OmanVista - AI Tourism Explorer",
    page_icon="🌍",
    layout="wide"
)

# ---------- Language Selector ----------
lang = st.sidebar.radio("🌐 Language | اللغة", ["English", "العربية"])

# ---------- Content Dictionary ----------
content = {
    "English": {
        "title": "OmanVista: AI Tourism Explorer",
        "subtitle": "Discover Oman’s hidden gems with the power of Artificial Intelligence",
        "about": """
            OmanVista is an **AI-powered tourism explorer** designed to showcase 
            hidden attractions, cultural sites, and natural wonders of Oman.
            
            🎯 Our mission: To connect travelers with unique experiences using **AI insights**.
        """,
        "button": "🚀 Explore Oman",
        "footer": "Made with ❤️ in Oman | Golden Bird"
    },
    "العربية": {
        "title": "عُمان فيستا: مستكشف السياحة بالذكاء الاصطناعي",
        "subtitle": "اكتشف جواهر عُمان المخفية بقوة الذكاء الاصطناعي",
        "about": """
            عُمان فيستا هو **مستكشف سياحي يعمل بالذكاء الاصطناعي** 
            يهدف إلى عرض المعالم المخفية، المواقع الثقافية، 
            والعجائب الطبيعية في عُمان.
            
            🎯 رسالتنا: ربط المسافرين بتجارب فريدة باستخدام **رؤى الذكاء الاصطناعي**.
        """,
        "button": "🚀 استكشف عُمان",
        "footer": "صُنع بحب ❤️ في عُمان | Golden Bird"
    }
}

# ---------- Layout ----------
col1, col2 = st.columns([1,1])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/81/Oman_Mountains.jpg", use_column_width=True)

with col2:
    st.markdown(f"## {content[lang]['title']}")
    st.markdown(f"### {content[lang]['subtitle']}")
    st.write(content[lang]['about'])
    if st.button(content[lang]['button']):
        st.success("✨ Coming Soon: Interactive AI Tourism Map of Oman")

# ---------- Footer ----------
st.markdown("---")
st.markdown(f"<p style='text-align:center;'>{content[lang]['footer']}</p>", unsafe_allow_html=True)
