import streamlit as st

# App title
st.set_page_config(page_title="OmanVista: AI Tourism Explorer", page_icon="🌍", layout="wide")

# Header
st.title("🌍 OmanVista: AI Tourism Explorer")
st.markdown("### Discover the hidden gems of Oman with the power of Artificial Intelligence ✨")

# Sidebar
st.sidebar.title("🔎 Explore")
option = st.sidebar.radio("Choose a feature:", ["🏖 Attractions", "🗺 Map View", "📊 Insights"])

# Main content
if option == "🏖 Attractions":
    st.subheader("Top Recommended Attractions in Oman 🇴🇲")
    attractions = [
        {"name": "Wadi Shab", "desc": "A beautiful valley with turquoise pools and waterfalls."},
        {"name": "Jebel Akhdar", "desc": "The Green Mountain, famous for terraced farms and cool weather."},
        {"name": "Muttrah Corniche", "desc": "A scenic seaside promenade in Muscat."},
        {"name": "Wahiba Sands", "desc": "Golden desert dunes perfect for adventure and stargazing."}
    ]
    for place in attractions:
        st.markdown(f"#### 🌟 {place['name']}")
        st.write(place['desc'])
        st.image("https://source.unsplash.com/800x400/?oman," + place['name'].replace(" ", ""), use_column_width=True)

elif option == "🗺 Map View":
    st.subheader("Interactive Map 🗺")
    st.map({"lat": [23.5880, 22.9600, 20.5600], "lon": [58.3829, 57.5300, 58.9000]})

elif option == "📊 Insights":
    st.subheader("Tourism Insights 📊")
    st.write("AI-based insights about tourism trends will appear here.")
    st.progress(70)
    st.success("Oman is becoming a rising hub for eco-tourism 🌱")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by **OmanVista Team**")
