import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=17.4&longitude=78.4&current=relative_humidity_2m,dew_point_2m"

response = requests.get(url)
data = response.json()

humidity = data["current"]["relative_humidity_2m"]
dew_point = data["current"]["dew_point_2m"]

moisture_index = (humidity * dew_point) / 100

print(f"Humidity: {humidity}%")
print(f"Dew Point: {dew_point}°C")
print(f"Estimated Moisture Index: {moisture_index}")