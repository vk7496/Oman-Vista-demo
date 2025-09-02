import os
import time
import random
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium

# ---------- Page Config & Styles ----------
st.set_page_config(page_title="OmanVista – AI Tourism Explorer", page_icon="🌴", layout="wide")
PRIMARY = "#006666"

st.markdown(f"""
<style>
.big-title {{ font-size: 34px; color: {PRIMARY}; text-align: center; font-weight: 800; margin: 6px 0 2px; }}
.sub-title {{ font-size: 15px; color: #333; text-align: center; margin: 0 0 20px; }}
.card-title {{ font-weight: 700; font-size: 18px; margin: 4px 0; color: #111; }}
.muted {{ color:#666; font-size: 12px; }}
.section {{ padding: 6px 0 2px; }}
</style>
""", unsafe_allow_html=True)

# ---------- Secrets / Keys ----------
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
UNSPLASH_KEY = st.secrets.get("UNSPLASH_ACCESS_KEY", "7MjJqxvtlvgkayIdLZM69n4yFIol0J6cjxeRvciMznQ")

# ---------- Language Selector ----------
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
    "reddit": {"English": "Community Buzz (Reddit)", "العربية": "أحدث المنشورات (Reddit)"},
    "view_map": {"English": "View on Map", "العربية": "عرض على الخريطة"},
}

st.markdown(f"<div class='big-title'>🌴 {TXT['title'][lang]} 🌴</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>{TXT['subtitle'][lang]}</div>", unsafe_allow_html=True)

# ---------- Seed Data (stable – no external API needed) ----------
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

# ---------- Unsplash Helper ----------
def fetch_unsplash_image(query: str, key: str, orientation: str = "landscape") -> str | None:
    if not key:
        return None
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {"query": query, "per_page": 5, "orientation": orientation, "client_id": key}
        r = requests.get(url, params=params, timeout=12)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            pick = random.choice(data["results"])
            return pick["urls"]["regular"]
        return None
    except Exception as e:
        st.warning(f"Unsplash error for '{query}': {e}")
        return None

def get_image_for(item) -> str:
    q = f"{item['name_en']} {item['region']} Oman"
    url = fetch_unsplash_image(q, UNSPLASH_KEY)
    if url:
        return url
    # fallback (placeholder always works)
    return f"https://placehold.co/1000x600?text={item['name_en'].replace(' ','%20')}"

# ---------- Filters ----------
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

# ---------- Map ----------
st.markdown(f"### 🗺️ {TXT['map'][lang]}")
if filtered:
    center_lat = sum(a["lat"] for a in filtered) / len(filtered)
    center_lon = sum(a["lon"] for a in filtered) / len(filtered)
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    for a in filtered:
        popup = a["name_en"] if lang == "English" else a["name_ar"]
        folium.Marker([a["lat"], a["lon"]], popup=popup).add_to(fmap)
    st_folium(fmap, width=900, height=420)
else:
    st.info("No items match your filters." if lang == "English" else "لا توجد نتائج مطابقة للمرشحات.")

# ---------- Cards (images + descriptions) ----------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
cols_per_row = 3
for i in range(0, len(filtered), cols_per_row):
    cols = st.columns(cols_per_row)
    for c, item in zip(cols, filtered[i:i+cols_per_row]):
        with c:
            img_url = get_image_for(item)
            st.image(img_url, use_container_width=True)
            title = item["name_en"] if lang == "English" else item["name_ar"]
            meta = f"{item['region']} • {item['category']}"
            if lang == "العربية":
                desc = f"{item['name_ar']} يقع ضمن فئة {item['category']} في {item['region']}. وجهة مناسبة للتجارب الأصيلة والمناظر الخلابة."
            else:
                desc = f"{item['name_en']} is a {item['category'].lower()} in {item['region']}, Oman. Perfect for authentic experiences and scenic views."
            st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{meta}</div>", unsafe_allow_html=True)
            st.write(desc)
            maps_url = f"https://www.google.com/maps?q={item['lat']},{item['lon']}"
            st.link_button(TXT["view_map"][lang], maps_url, use_container_width=True)
            time.sleep(0.05)

st.write("---")

# ---------- OpenAI Chatbot ----------
st.markdown(f"### 🤖 {TXT['chat'][lang]}")
user_q = st.text_input("Ask about Oman ✨ | اسأل عن عُمان")
if user_q:
    if not OPENAI_KEY:
        st.warning("Add OPENAI_API_KEY in Secrets to enable the AI assistant.")
    else:
        try:
            # OpenAI (new SDK)
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_KEY)
            system_prompt = (
                "You are an expert Oman tourism assistant. Answer concisely and helpfully. "
                "Use the user's language (English or Arabic). If user asks for Arabic, answer in Arabic."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_q}
            ]
            # You can switch model to gpt-4o or gpt-4o-mini depending on quota
            resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.4)
            answer = resp.choices[0].message.content
            st.success(answer)
        except Exception as e:
            st.error(f"OpenAI error: {e}")

st.write("---")

# ---------- Reddit (optional) ----------
st.markdown(f"### 🔊 {TXT['reddit'][lang]}")
enable_reddit = st.toggle("Enable Reddit feed (r/oman, r/travel)" if lang=="English" else "تفعيل خلاصة Reddit")
topic = st.text_input("Reddit topic (e.g., Oman travel, Salalah)" if lang=="English" else "موضوع Reddit (مثال: سياحة عُمان)","Oman travel")

def fetch_reddit_posts(q: str, subreddits=("oman","travel"), limit=5):
    posts = []
    headers = {"User-Agent": "OmanVistaDemo/1.0"}
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/search.json"
        params = {"q": q, "restrict_sr": 1, "sort": "new", "limit": limit}
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            for c in data.get("data", {}).get("children", []):
                d = c.get("data", {})
                posts.append({"title": d.get("title","(no title)"), "url": "https://www.reddit.com"+d.get("permalink","")})
        except Exception:
            # fail silently to keep demo smooth
            pass
    return posts[:limit]

if enable_reddit:
    posts = fetch_reddit_posts(topic)
    if not posts:
        st.info("No recent Reddit posts found (or blocked by rate limits).")
    else:
        for p in posts:
            st.markdown(f"• [{p['title']}]({p['url']})")

st.markdown("<br><div style='text-align:center;color:#777;font-size:12px'>© Golden Bird • OmanVista (Demo)</div>", unsafe_allow_html=True)
