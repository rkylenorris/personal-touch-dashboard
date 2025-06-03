import streamlit as st
from home_tab import get_current_weather, get_forecast
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
    
    weather_col, calendar_col = st.columns(2)
    
    weather = get_current_weather(LATITUDE, LONGITUDE, WEATHER_API_KEY)
    
    with weather_col:
    
        if weather:
            st.subheader("Current Weather")
            st.image(weather["icon"], width=100)
            st.metric("Temp", f"{weather['temp']}°F", f"Feels like {weather['feels_like']}°F")
            st.caption(weather["description"])
        else:
            st.error("Weather data not available.")
        
        st.subheader("Next Forecasts")

        forecast = get_forecast(LATITUDE, LONGITUDE, WEATHER_API_KEY)

        if forecast:
            col1, col2 = st.columns(2)
            for col, entry in zip([col1, col2], forecast):
                with col:
                    st.markdown(f"**{entry['time']}**")
                    st.image(entry["icon"], width=60)
                    st.metric("Temp", f"{entry['temp']}°F", f"Feels like {entry['feels_like']}°F")
        else:
            st.info("No forecast data available.")
    
    with calendar_col:
        st.subheader("Calendar")
        st.write("This is where the calendar will be displayed.")
        # Placeholder for calendar functionality
        st.info("Calendar functionality is not implemented yet.")


if __name__ == "__main__":
    main()
