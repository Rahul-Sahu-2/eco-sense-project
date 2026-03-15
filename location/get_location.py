# get_location.py

import streamlit as st
from streamlit_js_eval import get_geolocation


def get_user_location():
    """
    Get user's GPS location from browser
    Returns: latitude, longitude
    """

    st.subheader("📍 Capture User Location")

    location = get_geolocation()

    if location is None:
        st.warning("⚠️ Please allow location permission in your browser.")
        return None, None

    try:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]

        st.success("✅ Location captured successfully!")

        st.write("Latitude:", lat)
        st.write("Longitude:", lon)

        return lat, lon

    except Exception as e:
        st.error("❌ Unable to fetch location")
        st.write(e)
        return None, None


# Test block (optional)
if __name__ == "__main__":

    st.title("📍 Location Test Page")

    lat, lon = get_user_location()

    if lat and lon:
        st.success(f"Your Location: {lat}, {lon}")