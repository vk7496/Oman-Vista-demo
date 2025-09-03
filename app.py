import streamlit as st
import requests
import feedparser
import folium
from streamlit_folium import st_folium
from openai import OpenAI

# ---- استایل بک‌گراند ----
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #009688 0%, #004D40 100%);
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Oman AI Info Portal")
st.write("تهیه‌شده توسط **Golden Bird**")

# ---- OpenAI Chatbot ----
st.subheader("🤖 Chat with AI")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

user_input = st.text_input("سوالت رو از هوش مصنوعی بپرس:")
if user_input:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    st.write("💬 جواب:", response.choices[0].message.content)

# ---- عکس‌ها از Pexels و Unsplash ----
st.subheader("📸 تصاویر زیبای عمان")

PEXELS_KEY = st.secrets["PEXELS_API_KEY"]
UNSPLASH_KEY = st.secrets["UNSPLASH_API_KEY"]

def get_pexels_images(query="Oman"):
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=3"
    res = requests.get(url, headers=headers).json()
    return [{"url": p["src"]["large"], "loc": query} for p in res.get("photos", [])]

def get_unsplash_images(query="Oman"):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=3&client_id={UNSPLASH_KEY}"
    res = requests.get(url).json()
    return [{"url": u["urls"]["regular"], "loc": query} for u in res.get("results", [])]

images = get_pexels_images() + get_unsplash_images()

for img in images:
    st.image(img["url"], caption=f"📍 {img['loc']}")
    # نقشه
    m = folium.Map(location=[23.6, 58.5], zoom_start=6)
    folium.Marker([23.6, 58.5], tooltip=img['loc']).add_to(m)
    st_folium(m, width=500, height=300)

# ---- Reddit News via RSS ----
st.subheader("📰 Reddit News (Oman)")
rss_url = "https://www.reddit.com/r/oman/.rss"
feed = feedparser.parse(rss_url)

for entry in feed.entries[:5]:
    st.markdown(f"• [{entry.title}]({entry.link})")
