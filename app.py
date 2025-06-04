import streamlit as st
from home_tab import get_current_weather, get_forecast, get_calendar_events, get_quote, get_moon_phase
from dotenv import load_dotenv
import os
from datetime import datetime



def get_date_text():
    date_text = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')
    return date_text

load_dotenv()

def main():
    WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
    LATITUDE = os.getenv('LATITUDE')
    LONGITUDE = os.getenv('LONGITUDE')
    
    date_text = get_date_text()
    
    if not WEATHER_API_KEY or not LATITUDE or not LONGITUDE:
        st.error("Please set the environment variables: OPEN_WEATHER_API_KEY, LATITUDE, and LONGITUDE.")
        return
    
    st.set_page_config(layout="wide", page_title="Home Dashboard")
    
    # st.title("Home Dashboard")
    
    title_container = st.container()
    with title_container:
        # st.markdown(f"<h1 style='text-align: center; color: #4A90E2;'>{date_text}</h1>", unsafe_allow_html=True)
        st.title(date_text)
        quote = get_quote()
        if quote:
            st.subheader(f"\"{quote['quote']}\"")
            st.caption(f"- {quote['author']}")
        else:
            st.error("Quote not available.")
            
        
        
    weather_schedule_container = st.container()
    with weather_schedule_container:
    
        weather_col, calendar_col = st.columns(2)
        
        weather = get_current_weather(LATITUDE, LONGITUDE, WEATHER_API_KEY)
        
        with weather_col:
            current_weather_col, moon_col = st.columns(2)
            with current_weather_col:
                if weather:
                    st.subheader("Current Weather")
                    st.image(weather["icon"], width=100)
                    st.metric("Temp", f"{weather['temp']}°F", f"Feels like {weather['feels_like']}°F")
                    st.caption(weather["description"])
                else:
                    st.error("Weather data not available.")
            with moon_col:
                moon = get_moon_phase()
                st.subheader("Moon Phase")
                st.markdown(
                    f"""
                    <div>
                        <div>{moon['phase']}</div>
                        {moon['icon']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
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
            import datetime

            st.subheader("📅 Upcoming Events")
            
            CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')
            CALENDAR_CREDENTIALS_FILE = os.getenv('CALENDAR_CREDENTIALS_PATH', 'calendar-credentials.json')

            events = get_calendar_events(CALENDAR_CREDENTIALS_FILE, calendar_id=CALENDAR_ID)
            
            if not events:
                st.info("No upcoming events found.")
            else:
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    dt = datetime.datetime.fromisoformat(start)
                    time_str = dt.strftime("%a %b %d, %I:%M %p") if "T" in start else dt.strftime("%a %b %d")
                    title = event.get("summary", "Untitled")
                    st.markdown(f"**{time_str}** — {title}")


if __name__ == "__main__":
    main()
