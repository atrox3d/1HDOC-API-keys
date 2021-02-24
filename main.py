from private import privatedata as private
import requests
import json

# api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}
CURRENT_WEATHER_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

# https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
ONE_CALL_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

# parameters key names
KCITY = "q"
KLANGUAGE = "lang"
KUNITS = "units"
KLATITUDE = "lat"
KLONGITUDE = "lon"
KAPI_KEY = "appid"


def call_weather_api(endpoint: str, params: dict):
    response = requests.get(endpoint, params)
    response.raise_for_status()
    return response.status_code, response.json()


def get_current_weather():
    params = {
        KCITY: f"{private.CITY_IT},{private.COUNTRY_CODE}",
        KLANGUAGE: private.LANGUAGE,
        KAPI_KEY: private.API_KEY
    }
    return call_weather_api(CURRENT_WEATHER_ENDPOINT, params)


def get_onecall_forecast():
    params = {
        KLATITUDE: private.LATITUDE,
        KLONGITUDE: private.LONGITUDE,
        KLANGUAGE: private.LANGUAGE,
        KAPI_KEY: private.API_KEY
    }
    return call_weather_api(ONE_CALL_ENDPOINT, params)


statuscode, jsondata = get_onecall_forecast()
print(statuscode)
hourly = jsondata["hourly"]
print(json.dumps(hourly, indent=4))
