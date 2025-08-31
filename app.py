import requests
import streamlit as st

UNSPLASH_ACCESS_KEY = "7MjJqxvtlvgkayIdLZM69n4yFIol0J6cjxeRvciMznQ"  # اینو جایگزین کن

def fetch_images(query, count=5):
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": count,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [img["urls"]["regular"] for img in data["results"]]
    else:
        st.error("خطا در گرفتن تصاویر از Unsplash")
        return []

st.title("🌍 OmanVista - AI Tourism Explorer")

place = st.text_input("یک مکان یا موضوع گردشگری وارد کنید:", "Oman nature")

if st.button("جستجو"):
    images = fetch_images(place, count=6)
    if images:
        for img in images:
            st.image(img, use_container_width=True)

