import streamlit as st
import requests
import os

# گرفتن API از سکرت‌ها (مطمئن شو که توی Streamlit Secrets ذخیره کردی)
UNSPLASH_KEY = os.getenv("UNSPLASH_API_KEY")

st.title("Unsplash Image Test - Grid View")

query = st.text_input("🔍 Enter a keyword (e.g. Muscat, Oman, beach, desert):", "Oman")

if st.button("Search Images"):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=3"
    headers = {"Authorization": f"Client-ID {UNSPLASH_KEY}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        results = response.json()["results"]

        if len(results) > 0:
            cols = st.columns(3) # سه ستون برای نمایش عکس‌ها

            for i, result in enumerate(results):
                img_url = result["urls"]["regular"]
                img_desc = result["alt_description"] or "No description"

                with cols[i]:
                    st.image(img_url, caption=img_desc, use_column_width=True)
        else:
            st.warning("No images found. Try another keyword!")
    else:
        st.error(f"Error: {response.status_code}. Check your API key.")
