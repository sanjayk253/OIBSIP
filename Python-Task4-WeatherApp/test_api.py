
import requests
from config import API_KEY, BASE_URL

print("API key length:", len(API_KEY) if API_KEY else 0)

# Test city
city = "London"

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

try:
    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()

        print("API connection successful!")
        print("City:", data["name"])
        print("Temperature:", data["main"]["temp"], "°C")
        print("Humidity:", data["main"]["humidity"], "%")
        print("Weather:", data["weather"][0]["description"])

    elif response.status_code == 401:
        print("Invalid API key or API key not activated yet.")

    elif response.status_code == 404:
        print("City not found.")

    else:
        print("API Error:", response.status_code)
        print(response.text)

except requests.exceptions.Timeout:
    print("Connection timed out.")

except requests.exceptions.RequestException as error:
    print("Network error:", error)