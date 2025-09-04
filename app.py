import os
import random
import time
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from openai import OpenAI
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

# =========================
# Page Setup
# =========================
st.set_page_config(page_title="OmanVista – AI Tourism Explorer", page_icon="🌴", layout="wide")
PRIMARY = "#006666"

st.markdown(f"""
<style>
.big-title {{ font-size: 36px; font-weight: 800; color: {PRIMARY}; text-align:center; margin: 8px 0 2px; }}
.sub-title {{ font-size: 15px; color:#333; text-align:center; margin: 0 0 18px; }}
.hero {{ position: relative; width: 100%; min-height: 240px; border-radius: 14px;
         background-size: cover !important; background-position: center !important;
         display:flex; align-items:center; justify-content:center;
         box-shadow: 0 8px 24px rgba(0,0,0,.12); }}
.hero-overlay {{ background: linear-gradient(180deg, rgba(0,0,0,.35), rgba(0,0,0,.35));
                 position:absolute; inset:0; border-radius:14px; }}
.hero-title {{ position:relative; color:#fff; text-align:center; z-index:2; }}
.chat-bubble-user {{ background:#e8f5f3; padding:10px 12px; border-radius:12px; margin:6px 0; border:1px solid #cbe6e1; }}
.chat-bubble-assistant {{ background:#fff; padding:10px 12px; border-radius:12px; margin:6px 0; border:1px solid #eee; }}
.footer {{ text-align:center; color:#777; font-size:12px; margin-top: 16px; }}
</style>
""", unsafe_allow_html=True)

# =========================
# Secrets / Keys
# =========================
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
PEXELS_KEY = st.secrets.get("PEXELS_API_KEY", "")

# =========================
# Language Pack
# =========================
lang = st.sidebar.radio("🌐 Language | اللغة", ["English", "العربية"], index=0)

TXT = {
    "title": {"English": "OmanVista – AI Tourism Explorer", "العربية": "عُمان فيستا – مستكشف السياحة بالذكاء الاصطناعي"},
    "subtitle": {
        "English": "Discover Oman’s hidden gems with bilingual AI content.",
        "العربية": "اكتشف جواهر عُمان المخفية بمحتوى ذكي ثنائي اللغة."
    },
    "photos": {"English": "Photo Highlights", "العربية": "لمحات مصورة"},
    "map": {"English": "Interactive Map", "العربية": "خريطة تفاعلية"},
    "chat": {"English": "AI Travel Assistant", "العربية": "مساعد السفر الذكي"},
    "reddit": {"English": "Community Buzz (Reddit)", "العربية": "منشورات المجتمع (Reddit)"},
    "reddit_query": {"English": "Topic (e.g., Oman travel, Salalah)", "العربية": "الموضوع (مثال: سياحة عُمان، صلالة)"},
    "reddit_btn": {"English": "Fetch Latest Posts", "العربية": "جلب أحدث المنشورات"},
    "empty_feed": {"English": "No recent posts found.", "العربية": "لا توجد منشورات حديثة."},
    "ai_placeholder": {"English": "Ask about Oman ✨", "العربية": "اسأل عن عُمان ✨"},
    "footer": {"English": "Prepared by Golden Bird", "العربية": "إعداد: Golden Bird"},
}

st.markdown(f"<div class='big-title'>🌴 {TXT['title'][lang]} 🌴</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>{TXT['subtitle'][lang]}</div>", unsafe_allow_html=True)

# =========================
# Attractions
# =========================
ATTRACTIONS = [
    {"name_en":"Sultan Qaboos Grand Mosque","name_ar":"جامع السلطان قابوس الأكبر",
     "lat":23.5859,"lon":58.4078},
    {"name_en":"Mutrah Corniche","name_ar":"كورنيش مطرح",
     "lat":23.6155,"lon":58.5638},
    {"name_en":"Nizwa Fort","name_ar":"قلعة نزوى",
     "lat":22.9333,"lon":57.5333},
    {"name_en":"Jebel Shams","name_ar":"جبل شمس",
     "lat":23.2386,"lon":57.2742},
    {"name_en":"Wadi Bani Khalid","name_ar":"وادي بني خالد",
     "lat":22.6000,"lon":59.2000},
    {"name_en":"Wahiba Sands","name_ar":"رمال الشرقية",
     "lat":21.4500,"lon":58.8000},
    {"name_en":"Ras Al Jinz","name_ar":"محمية السلاحف برأس الجنز",
     "lat":22.3500,"lon":59.4500},
    {"name_en":"Al Mughsail Beach","name_ar":"شاطئ المغسيل",
     "lat":16.8820,"lon":53.7290},
]

# =========================
# Pexels + Unsplash
# =========================
def fetch_pexels(query, key, per_page=3):
    if not key: return []
    try:
        r = requests.get("https://api.pexels.com/v1/search",
                         headers={"Authorization": key},
                         params={"query": query, "per_page": per_page}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return [p["src"]["large"] for p in data.get("photos", [])]
    except Exception:
        return []
    return []

def fetch_unsplash(query, per_page=3):
    try:
        r = requests.get("https://source.unsplash.com/1600x900/?" + query, timeout=10)
        if r.status_code == 200:
            return [r.url]
    except Exception:
        return []
    return []

def get_image(query):
    imgs = fetch_pexels(query, PEXELS_KEY)
    if imgs: return imgs
    imgs = fetch_unsplash(query)
    if imgs: return imgs
    return ["https://placehold.co/600x400?text=OmanVista"]

# =========================
# Map
# =========================
st.markdown(f"### 🗺️ {TXT['map'][lang]}")
m = folium.Map(location=[21.0, 57.0], zoom_start=6)
for a in ATTRACTIONS:
    popup = a["name_en"] if lang == "English" else a["name_ar"]
    folium.Marker([a["lat"], a["lon"]], popup=popup).add_to(m)
st_folium(m, width=950, height=420)

# =========================
# Photo Highlights
# =========================
st.markdown(f"### 📸 {TXT['photos'][lang]}")
cols = st.columns(3)
for i, a in enumerate(ATTRACTIONS[:6]):
    q = a["name_en"] + " Oman"
    imgs = get_image(q)
    with cols[i % 3]:
        st.image(imgs[0], use_container_width=True,
                 caption=a["name_en"] if lang=="English" else a["name_ar"])

# =========================
# OpenAI Chatbot
# =========================
st.markdown(f"### 🤖 {TXT['chat'][lang]}")
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"role":"system","content":"You are an Oman tourism assistant."}]
user_q = st.text_input(TXT["ai_placeholder"][lang])
if st.button("Send") and user_q:
    st.session_state.chat_messages.append({"role":"user","content":user_q})
    if OPENAI_KEY:
        try:
            client = OpenAI(api_key=OPENAI_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.chat_messages
            )
            ans = resp.choices[0].message.content
            st.session_state.chat_messages.append({"role":"assistant","content":ans})
        except Exception as e:
            st.error(e)
for m in st.session_state.chat_messages[1:]:
    if m["role"]=="user":
        st.markdown(f"<div class='chat-bubble-user'>🧑 {m['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-assistant'>🤖 {m['content']}</div>", unsafe_allow_html=True)

# =========================
# Reddit RSS
# =========================
st.markdown(f"### 🔊 {TXT['reddit'][lang]}")
topic = st.text_input(TXT["reddit_query"][lang], "Oman travel")
if st.button(TXT["reddit_btn"][lang]):
    posts = []
    headers = {"User-Agent": "OmanVistaDemo/1.0"}
    def parse_rss(url):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            root = ET.fromstring(r.content)
            items = root.findall(".//item")
            return [{"title":i.findtext("title"),"link":i.findtext("link")} for i in items[:6]]
        except: return []
    enc = quote_plus(topic)
    urls = [
        f"https://www.reddit.com/r/oman/search.rss?q={enc}&restrict_sr=on&sort=new",
        f"https://www.reddit.com/r/travel/search.rss?q={enc}+Oman&restrict_sr=on&sort=new",
    ]
    for u in urls: posts.extend(parse_rss(u))
    if not posts:
        st.info(TXT["empty_feed"][lang])
    else:
        for p in posts: st.markdown(f"• [{p['title']}]({p['link']})")

# =========================
# Footer
# =========================
st.markdown(f"<div class='footer'>© {TXT['footer'][lang]}</div>", unsafe_allow_html=True)
