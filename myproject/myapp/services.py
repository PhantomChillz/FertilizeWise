import requests

WEATHER_API_KEY = "56231c4405fb01884adcd1e961ee46d9"
GEO_API_KEY = "0227097bc71b17fbadd5b971c15d9820"

def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def fetch_location():
    url = f"https://ipapi.co/json/?key={GEO_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None