from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

def get_weather(latitude: str, longitude: str, api_key: str) -> dict:
    
    api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
    
    response = requests.get(api_call)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Load environment variables
    latitude = os.getenv('LATITUDE')
    longitude = os.getenv('LONGITUDE')
    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    
    # Check if all required environment variables are set
    if latitude and longitude and api_key:
        # Fetch and save weather data
        print(f"Fetching weather data for coordinates: {latitude}, {longitude}")
        try:
            weather_data = get_weather(latitude, longitude, api_key)
            with open('weather_data.json', 'w') as f:
                json.dump(weather_data, f, indent=4)
        except Exception as e:
            print(f"Failed to retrieve weather data: {e}")
    else:
        print("Please set LATITUDE and LONGITUDE in your environment variables.")
