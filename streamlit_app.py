import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static

# Load the dataset
def load_data():
    return pd.read_csv("European_Ski_Resorts.csv")

df = load_data()

# Streamlit App Title
st.title("⛷️ European Ski Resort Finder 🏔️")
st.markdown("Find the best ski resort based on your preferences!")

# Sidebar filters
st.sidebar.header("Filter Ski Resorts 🎯")
country_filter = st.sidebar.multiselect("Select Country:", df["Country"].unique())
max_price = st.sidebar.slider("Max Day Pass Price (€):", int(df["DayPassPriceAdult"].min()), int(df["DayPassPriceAdult"].max()), int(df["DayPassPriceAdult"].max()))
min_slope = st.sidebar.slider("Min Total Slope (km):", 0, int(df["TotalSlope"].max()), 0)

df_filtered = df[(df["DayPassPriceAdult"] <= max_price) & (df["TotalSlope"] >= min_slope)]
if country_filter:
    df_filtered = df_filtered[df_filtered["Country"].isin(country_filter)]

# Display filtered resorts
st.subheader("🏂 Matching Ski Resorts")
st.dataframe(df_filtered[["Resort", "Country", "DayPassPriceAdult", "TotalSlope"]].sort_values("DayPassPriceAdult"))

# Select a resort to get details
selected_resort = st.selectbox("Select a Ski Resort for More Details:", df_filtered["Resort"].unique())
resort_info = df[df["Resort"] == selected_resort].iloc[0]

st.subheader(f"🏔️ Resort Details: {selected_resort}")
st.write(f"📍 **Country:** {resort_info['Country']}")
st.write(f"🚡 **Highest Point:** {resort_info['HighestPoint']} m")
st.write(f"🏔️ **Lowest Point:** {resort_info['LowestPoint']} m")
st.write(f"💰 **Day Pass Price:** {resort_info['DayPassPriceAdult']} €")
st.write(f"🎿 **Total Slope:** {resort_info['TotalSlope']} km")
st.write(f"🌙 **Night Skiing Available:** {'Yes' if resort_info['NightSki'] else 'No'}")

# Show resort location (example coordinates, should be in dataset)
if "Latitude" in df.columns and "Longitude" in df.columns:
    resort_lat, resort_lon = resort_info["Latitude"], resort_info["Longitude"]
    m = folium.Map(location=[resort_lat, resort_lon], zoom_start=10)
    folium.Marker([resort_lat, resort_lon], popup=selected_resort, icon=folium.Icon(color="red")).add_to(m)
    folium_static(m)

# Google Places API for restaurant suggestions
st.subheader("🍽️ Nearby Restaurants")
api_key = "YOUR_GOOGLE_PLACES_API_KEY"  # Replace with your API key
location = f"{resort_lat},{resort_lon}"
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=5000&type=restaurant&key={api_key}"
response = requests.get(url).json()

if "results" in response:
    restaurants = response["results"][:5]
    for r in restaurants:
        st.write(f"🍴 **{r['name']}** - ⭐ {r.get('rating', 'N/A')} stars")
        st.write(f"📍 Address: {r['vicinity']}")
else:
    st.write("No restaurant data available.")

st.markdown("---")
st.write("Built with ❤️ using Streamlit")
