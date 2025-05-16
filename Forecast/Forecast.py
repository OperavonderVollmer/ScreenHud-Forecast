from OperaPowerRelay import opr
import requests
from datetime import datetime



# Expected time format: HHMM
# Will return {GB: 24:00, US: 12:00 AM}
def get_time(time):

    US_Code = "AM"

    if int(time) >= 1200:
        US_Code = "PM"
    
    return {"GB": f"{time[:-2]}:00", "US": f"{time[:-2]}:00 {US_Code}"}



def get_forecast(city = ""):
    
    url = f"https://wttr.in/{city}?format=j1" 
    response = requests.get(url)

    if response.status_code != 200:
        return 

    data = response.json()
    current_time = datetime.now().hour * 100

    if "weather" not in data or not data["weather"]:
        return 
    
    nearest_area = data.get("nearest_area")[0].get("areaName", "")[0].get("value", "")
    country = data.get("nearest_area")[0].get("country", "")[0].get("value", "")

    today_date = data.get("weather", [{}])[0].get("date", "")
    today_forecast = data.get("weather", [{}])[0].get("hourly", [])
    
    tomorrow_date = data.get("weather", [{}])[1].get("date", "")
    tomorrow_forecast = data.get("weather", [{}])[1].get("hourly", [])

    for hour in today_forecast:
        hour["date"] = today_date
        hour["city"] = f"{nearest_area}, {country}"

    for hour in tomorrow_forecast:
        hour["date"] = tomorrow_date
        hour["city"] = f"{nearest_area}, {country}"


    total_forecasts = today_forecast + tomorrow_forecast
    forecasts = [h for h in total_forecasts if int(h["time"]) >= current_time]

    export = []

    for forecast in forecasts:
        t = get_time(forecast["time"])
        export.append({
            "date": forecast["date"],
            "city": forecast["city"],
            "timeUS": t["US"],
            "timeGB": t["GB"],
            "forecast": forecast["weatherDesc"][0]["value"].strip(),
            "tempC": forecast["tempC"],
            "tempF": forecast["tempF"],
            "fog": f'{forecast["chanceoffog"]}',
            "frost": f'{forecast["chanceoffrost"]}',
            "hightemp": f'{forecast["chanceofhightemp"]}',
            "overcast": f'{forecast["chanceofovercast"]}',
            "rain": f'{forecast["chanceofrain"]}',
            "snow": f'{forecast["chanceofsnow"]}',
            "sunshine": f'{forecast["chanceofsunshine"]}',
            "thunder": f'{forecast["chanceofthunder"]}',
            "windy": f'{forecast["chanceofwindy"]}',
        })
    
    return export


