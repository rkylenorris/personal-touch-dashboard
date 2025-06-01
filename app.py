import streamlit as st
from home_tab import get_weather
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
    LATITUDE = os.getenv('LATITUDE')
    LONGITUDE = os.getenv('LONGITUDE')
    
    if not WEATHER_API_KEY or not LATITUDE or not LONGITUDE:
        st.error("Please set the environment variables: OPEN_WEATHER_API_KEY, LATITUDE, and LONGITUDE.")
        return
    
    st.set_page_config(layout="wide", page_title="Home Dashboard")
    
    st.title("Home Dashboard")
    
    weather = get_weather(LATITUDE, LONGITUDE, WEATHER_API_KEY)
    
    if weather:
        st.subheader("Current Weather")
        st.image(weather["icon"], width=100)
        st.metric("Temp", f"{weather['temp']}°F", f"Feels like {weather['feels_like']}°F")
        st.caption(weather["description"])
    else:
        st.error("Weather data not available.")


if __name__ == "__main__":
    main()
