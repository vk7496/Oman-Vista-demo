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
/* Global */
html, body {{ background-color:#fafafa; }}
.big-title {{ font-size: 36px; font-weight: 800; color: {PRIMARY}; text-align:center; margin: 8px 0 2px; }}
.sub-title {{ font-size: 15px; color:#333; text-align:center; margin: 0 0 18px; }}

/* Hero */
.hero {{
  position: relative;
  width: 100%;
  min-height: 240px;
  border-radius: 14px;
  background-size: cover !important;
  background-position: center !important;
  display:flex; align-items:center; justify-content:center;
  box-shadow: 0 8px 24px rgba(0,0,0,.12);
}}
.hero-overlay {{
  background: linear-gradient(180deg, rgba(0,0,0,.35), rgba(0,0,0,.35));
  position:absolute; inset:0; border-radius:14px;
}}
.hero-title {{
  position:relative; color:#fff; text-align:center; z-index:2;
}}
.card-title {{ font-weight:700; font-size:18px; margin:6px 0 4px; color:#111; }}
.muted {{ color:#666; font-size:12px; }}
.section {{ padding: 6px 0 2px; }}
.chat-bubble-user {{
  background:#e8f5f3; padding:10px 12px; border-radius:12px; margin:6px 0; border:1px solid #cbe6e1;
}}
.chat-bubble-assistant {{
  background:#fff; padding:10px 12px; border-radius:12px; margin:6px 0; border:1px solid #eee;
}}
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
    "filters": {"English": "Filters", "العربية": "المرشحات"},
    "region": {"English": "Region", "العربية": "المنطقة"},
    "category": {"English": "Category", "العربية": "الفئة"},
    "search": {"English": "Search (name/tags)", "العربية": "بحث (اسم/وسوم)"},
    "results": {"English": "results", "العربية": "نتيجة"},
    "map": {"English": "Interactive Map", "العربية": "خريطة تفاعلية"},
    "chat": {"English": "AI Travel Assistant", "العربية": "مساعد السفر الذكي"},
    "reddit": {"English": "Community Buzz (Reddit)", "العربية": "منشورات المجتمع (Reddit)"},
    "view_map": {"English": "View on Map", "العربية": "عرض على الخريطة"},
    "hero_caption": {"English": "Discover Oman - Beauty & Culture", "العربية": "اكتشف عُمان - الجمال والثقافة"},
    "photos": {"English": "Photo Highlights", "العربية": "لمحات مصورة"},
    "reddit_query": {"English": "Topic (e.g., Oman travel, Salalah)", "العربية": "الموضوع (مثال: سياحة عُمان، صلالة)"},
    "reddit_btn": {"English": "Fetch Latest Posts", "العربية": "جلب أحدث المنشورات"},
    "empty_feed": {"English": "No recent posts found.", "العربية": "لا توجد منشورات حديثة."},
    "ai_placeholder": {"English": "Ask about Oman ✨", "العربية": "اسأل عن عُمان ✨"},
    "footer": {"English": "Prepared by Golden Bird", "العربية": "إعداد: Golden Bird"},
}

st.markdown(f"<div class='big-title'>🌴 {TXT['title'][lang]} 🌴</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>{TXT['subtitle'][lang]}</div>", unsafe_allow_html=True)

# =========================
# Data (Attractions)
# =========================
ATTRACTIONS = [
    {"slug":"sultan-qaboos-grand-mosque","name_en":"Sultan Qaboos Grand Mosque","name_ar":"جامع السلطان قابوس الأكبر",
     "region":"Muscat","category":"Culture & Architecture","tags":["mosque","architecture","landmark"],
     "lat":23.5859,"lon":58.4078},
    {"slug":"mutrah-corniche","name_en":"Mutrah Corniche","name_ar":"كورنيش مطرح",
     "region":"Muscat","category":"City & Waterfront","tags":["sea","promenade","market","sunset"],
     "lat":23.6155,"lon":58.5638},
    {"slug":"nizwa-fort","name_en":"Nizwa Fort","name_ar":"قلعة نزوى",
     "region":"Ad Dakhiliyah","category":"Heritage & Fort","tags":["fort","history","culture","market"],
     "lat":22.9333,"lon":57.5333},
    {"slug":"jebel-shams","name_en":"Jebel Shams","name_ar":"جبل شمس",
     "region":"Ad Dakhiliyah","category":"Mountains & Hiking","tags":["mountain","hiking","viewpoints","nature"],
     "lat":23.2386,"lon":57.2742},
    {"slug":"wadi-bani-khalid","name_en":"Wadi Bani Khalid","name_ar":"وادي بني خالد",
     "region":"Ash Sharqiyah","category":"Wadi & Pools","tags":["wadi","swimming","oasis","hike"],
     "lat":22.6000,"lon":59.2000},
    {"slug":"wahiba-sands","name_en":"Wahiba Sands (Sharqiya Sands)","name_ar":"رمال الشرقية",
     "region":"Ash Sharqiyah","category":"Desert & Adventure","tags":["desert","dunes","camp","4x4"],
     "lat":21.4500,"lon":58.8000},
    {"slug":"ras-al-jinz","name_en":"Ras Al Jinz Turtle Reserve","name_ar":"محمية السلاحف برأس الجنز",
     "region":"Ash Sharqiyah","category":"Wildlife & Nature","tags":["turtles","beach","wildlife","night"],
     "lat":22.3500,"lon":59.4500},
    {"slug":"mughsail-beach","name_en":"Al Mughsail Beach","name_ar":"شاطئ المغسيل",
     "region":"Dhofar (Salalah)","category":"Beach & Blowholes","tags":["beach","blowholes","cliffs","khareef"],
     "lat":16.8820,"lon":53.7290},
]

# =========================
# Pexels Helpers
# =========================
def fetch_pexels_image(query: str, key: str, per_page: int = 6) -> list[str]:
    """Return list of image urls or empty list on failure."""
    if not key:
        return []
    try:
        headers = {"Authorization": key}
        url = "https://api.pexels.com/v1/search"
        params = {"query": query, "per_page": per_page}
        r = requests.get(url, headers=headers, params=params, timeout=12)
        r.raise_for_status()
        data = r.json()
        photos = data.get("photos", [])
        return [p["src"]["large"] for p in photos]
    except Exception:
        return []

def get_cover_image() -> str:
    # Try a few Oman-related queries for a nice hero bg
    for q in ["Oman landscape", "Muscat Oman", "Salalah Oman", "Desert Oman", "Wadi Oman"]:
        imgs = fetch_pexels_image(q, PEXELS_KEY, per_page=3)
        if imgs:
            return random.choice(imgs)
    return "https://placehold.co/1600x600?text=OmanVista"

# =========================
# Hero (Background Cover)
# =========================
hero_url = get_cover_image()
st.markdown(
    f"""
    <div class="hero" style="background: url('{hero_url}');">
        <div class="hero-overlay"></div>
        <div class="hero-title">
            <h1 style="margin:0;">{TXT['title'][lang]}</h1>
            <p style="margin:4px 0 0;">{TXT['hero_caption'][lang]}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# =========================
# Sidebar Filters
# =========================
st.sidebar.header(TXT["filters"][lang])
regions = ["All"] + sorted({a["region"] for a in ATTRACTIONS})
cats = ["All"] + sorted({a["category"] for a in ATTRACTIONS})
sel_region = st.sidebar.selectbox(TXT["region"][lang], regions, index=0)
sel_category = st.sidebar.selectbox(TXT["category"][lang], cats, index=0)
q = st.sidebar.text_input(TXT["search"][lang], "")

filtered = ATTRACTIONS
if sel_region != "All":
    filtered = [a for a in filtered if a["region"] == sel_region]
if sel_category != "All":
    filtered = [a for a in filtered if a["category"] == sel_category]
if q.strip():
    qq = q.strip().lower()
    filtered = [
        a for a in filtered
        if qq in a["name_en"].lower()
        or qq in a["name_ar"]
        or qq in a["region"].lower()
        or qq in a["category"].lower()
        or any(qq in t.lower() for t in a["tags"])
    ]

st.caption(f"Showing {len(filtered)} {TXT['results'][lang]}")

# =========================
# Map
# =========================
st.markdown(f"### 🗺️ {TXT['map'][lang]}")
if filtered:
    center_lat = sum(a["lat"] for a in filtered) / len(filtered)
    center_lon = sum(a["lon"] for a in filtered) / len(filtered)
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    for a in filtered:
        popup = a["name_en"] if lang == "English" else a["name_ar"]
        folium.Marker([a["lat"], a["lon"]], popup=popup).add_to(fmap)
    st_folium(fmap, width=950, height=420)
else:
    st.info("No items match your filters." if lang == "English" else "لا توجد نتائج مطابقة للمرشحات.")

# =========================
# Photo Highlights (from Pexels)
# =========================
st.markdown(f"### 📸 {TXT['photos'][lang]}")
grid = st.columns(3)
# Build a combined query from the first few filtered attractions (or fallback)
queries = [a["name_en"] + " Oman" for a in filtered[:3]] or ["Oman landscape", "Muscat Oman", "Salalah Oman"]
images = []
for qx in queries:
    pics = fetch_pexels_image(qx, PEXELS_KEY, per_page=2)
    images.extend(pics)

if not images: # last fallback
    images = fetch_pexels_image("Oman", PEXELS_KEY, per_page=6)

for i, url in enumerate(images[:6]):
    with grid[i % 3]:
        st.image(url, use_container_width=True)
        time.sleep(0.03)

st.write("---")

# =========================
# OpenAI Chatbot (with history)
# =========================
st.markdown(f"### 🤖 {TXT['chat'][lang]}")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "system", "content":
         "You are an expert Oman tourism assistant. Answer concisely and helpfully. "
         "Detect the user's language (English or Arabic) and reply in that language."}
    ]

# Show history (simple bubbles)
def render_history(msgs):
    for m in msgs:
        if m["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'><b>🧑 You:</b><br>{m['content']}</div>", unsafe_allow_html=True)
        elif m["role"] == "assistant":
            st.markdown(f"<div class='chat-bubble-assistant'><b>🤖 AI:</b><br>{m['content']}</div>", unsafe_allow_html=True)

render_history([m for m in st.session_state.chat_messages if m["role"] != "system"])

user_q = st.text_input(TXT["ai_placeholder"][lang] + " | " + TXT["ai_placeholder"]["العربية"])
col_send, col_clear = st.columns([1,1])
send_clicked = col_send.button("Send / إرسال")
clear_clicked = col_clear.button("Clear / مسح")

if clear_clicked:
    st.session_state.chat_messages = [st.session_state.chat_messages[0]]
    st.experimental_rerun()

if send_clicked and user_q:
    st.session_state.chat_messages.append({"role": "user", "content": user_q})
    if not OPENAI_KEY:
        st.warning("Add OPENAI_API_KEY in Secrets to enable the AI assistant.")
    else:
        try:
            client = OpenAI(api_key=OPENAI_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o-mini", # fast & capable
                messages=st.session_state.chat_messages,
                temperature=0.4,
                max_tokens=350,
            )
            answer = resp.choices[0].message.content
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"OpenAI error: {e}")

st.write("---")

# =========================
# Reddit RSS (r/oman & r/travel)
# =========================
st.markdown(f"### 🔊 {TXT['reddit'][lang]}")
topic = st.text_input(TXT["reddit_query"][lang], "Oman travel")
if st.button(TXT["reddit_btn"][lang]):
    posts = []

    headers = {"User-Agent": "OmanVistaDemo/1.0"}
    def parse_rss(url: str):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            root = ET.fromstring(r.content)
            # works for RSS and Atom: check both
            items = root.findall(".//item")
            if not items:
                items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
            parsed = []
            for it in items[:8]:
                title = it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title") or "(no title)"
                link_el = it.find("link")
                link = (link_el.text if link_el is not None else None) or (link_el.get("href") if link_el is not None else None)
                # Atom sometimes stores link in attribute
                if not link:
                    link = it.findtext("{http://www.w3.org/2005/Atom}link")
                parsed.append({"title": title, "link": link or "#"})
            return parsed
        except Exception:
            return []

    # Search within subreddits
    enc = quote_plus(topic)
    urls = [
        f"https://www.reddit.com/r/oman/search.rss?q={enc}&restrict_sr=on&sort=new",
        f"https://www.reddit.com/r/travel/search.rss?q={enc}+Oman&restrict_sr=on&sort=new",
    ]
    for u in urls:
        posts.extend(parse_rss(u))

    if not posts:
        st.info(TXT["empty_feed"][lang])
    else:
        for p in posts[:8]:
            st.markdown(f"• [{p['title']}]({p['link']})")

# =========================
# Footer
# =========================
st.markdown(f"<div class='footer'>© {TXT['footer'][lang]}</div>", unsafe_allow_html=True)
