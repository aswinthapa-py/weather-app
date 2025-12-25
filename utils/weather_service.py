import requests
API_KEY="f25975004ba9e8d586b5514ba1400b5b"
BASE_URL="https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, units="metric"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": f"{data['name']}, {data['sys']['country']}",
        "temperature": round(data["main"]["temp"]),
        "min_temp": round(data["main"]["temp_min"]),
        "max_temp": round(data["main"]["temp_max"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["main"],
        "icon": data["weather"][0]["icon"],
        "timestamp": data["dt"],
        "timezone": data["timezone"]
    }