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
KEXCLUDE = "exclude"


def call_weather_api(endpoint: str, params: dict) -> (int, dict):
    print(f"calling endpoint: {endpoint}")
    print(f"with params: {params}")
    response = requests.get(endpoint, params)
    response.raise_for_status()
    return response.status_code, response.json()


def get_current_weather() -> (int, dict):
    params = {
        KCITY: f"{private.CITY_IT},{private.COUNTRY_CODE}",
        KLANGUAGE: private.LANGUAGE,
        KAPI_KEY: private.API_KEY
    }
    return call_weather_api(CURRENT_WEATHER_ENDPOINT, params)


def get_onecall_forecast(current=True, minutely=True, hourly=True, daily=True) -> (int, dict):
    # https://www.ventusky.com/merauke
    rainy_latitude = -8.484026790361654
    rainy_longitude = 140.40224668902974
    params = {
        # KLATITUDE: private.LATITUDE,
        # KLONGITUDE: private.LONGITUDE,
        KLATITUDE: rainy_latitude,
        KLONGITUDE: rainy_longitude,
        KLANGUAGE: private.LANGUAGE,
        KAPI_KEY: private.API_KEY
    }

    exclude = []
    if not current:
        exclude.append("current")
    if not minutely:
        exclude.append("minutely")
    if not hourly:
        exclude.append("hourly")
    if not daily:
        exclude.append("daily")

    if len(exclude):
        exclude_param = ",".join(exclude)
        params["exclude"] = exclude_param

    return call_weather_api(ONE_CALL_ENDPOINT, params)


# get only hourly
statuscode, weather_data = get_onecall_forecast(current=False, minutely=False, daily=False)
print(statuscode)
# print(json.dumps(weather_data, indent=4))

weather_slice = weather_data["hourly"][:12]
# condition_codes = [hour["weather"][0]["id"] for hour  in weather_slice]
umbrella = False
for hour in weather_slice:
    condition_code = hour["weather"][0]["id"]
    if int(condition_code) < 700:
        umbrella = True

if umbrella:
    print("bring an umbrella")
