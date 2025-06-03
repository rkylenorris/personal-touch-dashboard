from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime

from .api_call import make_api_call

load_dotenv()


# TODO: Refactor into 3 functions: make api call, get current weather, get forecast
def get_current_weather(latitude: str, longitude: str, api_key: str) -> dict:
    
    api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
    # api_call = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
    
    data = make_api_call(api_call)
    
    return {
        "description": data["weather"][0]["description"].title(),
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }


def get_forecast(latitude: str, longitude: str, api_key: str) -> list[dict]:
    
    api_call = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
    
    data = make_api_call(api_call)
    
    forecast = []
    for entry in data["list"]:
        dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
        forecast.append({
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M"),
            "temp": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "description": entry["weather"][0]["description"].title(),
            "icon": f"http://openweathermap.org/img/wn/{entry['weather'][0]['icon']}@2x.png"
        })
        
    return forecast
        


if __name__ == "__main__":
    # Load environment variables
    latitude = os.getenv('LATITUDE')
    longitude = os.getenv('LONGITUDE')
    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    
    # Check if all required environment variables are set
    if latitude and longitude and api_key:
        # Fetch and save weather data
        print(f"Fetching forecast data for coordinates: {latitude}, {longitude}")
        try:
            forecast_data = get_forecast(latitude, longitude, api_key)
            current_weather = get_current_weather(latitude, longitude, api_key)
            with open('forecast_data.json', 'w') as f:
                json.dump(forecast_data[0:2], f, indent=4)
            with open('current_weather.json', 'w') as f:
                json.dump(current_weather, f, indent=4)
        except Exception as e:
            print(f"Failed to retrieve weather data: {e}")
    else:
        print("Please set LATITUDE and LONGITUDE in your environment variables.")
