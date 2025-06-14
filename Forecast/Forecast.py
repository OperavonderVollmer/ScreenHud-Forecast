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
         
    """
    Fetches the current and next day's weather forecast for a given city.

    Parameters
    ----------
    city : str, optional
        The city to fetch the forecast for. Defaults to an empty string.

    Returns
    -------
    list
        A list of dictionaries, each containing the forecast for a given hour. If the
        request fails, an empty list is returned.

    Notes
    -----
    The time format used is 24 hour format, and the returned forecast times are in
    the format "HH:MM".
    """
    
    url = f"https://wttr.in/{city}?format=j1" 
    print(url)
        
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    current_time = datetime.now().hour * 100

    if "weather" not in data or not data["weather"]:
        return None
    

    nearest_area = data.get("nearest_area")[0].get("areaName", "")[0].get("value", "")
    country = data.get("nearest_area")[0].get("country", "")[0].get("value", "")

    today_date = data.get("weather", [{}])[0].get("date", "")
    today_forecast = data.get("weather", [{}])[0].get("hourly", [])
    
    tomorrow_date = data.get("weather", [{}])[1].get("date", "")
    tomorrow_forecast = data.get("weather", [{}])[1].get("hourly", [])


    for hour in today_forecast:
        hour["date"] = today_date
        hour["city"] = f"{nearest_area}, {country}"
        hour["time"] = str(int(hour["time"])).zfill(4)


    for hour in tomorrow_forecast:
        hour["date"] = tomorrow_date
        hour["city"] = f"{nearest_area}, {country}"
        hour["time"] = str(int(hour["time"]) + 2400).zfill(4)


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
            "chances":
            {
                "fog": f'{forecast["chanceoffog"]}',
                "frost": f'{forecast["chanceoffrost"]}',
                "hightemp": f'{forecast["chanceofhightemp"]}',
                "overcast": f'{forecast["chanceofovercast"]}',
                "rain": f'{forecast["chanceofrain"]}',
                "snow": f'{forecast["chanceofsnow"]}',
                "sunshine": f'{forecast["chanceofsunshine"]}',
                "thunder": f'{forecast["chanceofthunder"]}',
                "windy": f'{forecast["chanceofwindy"]}',
            }
            
        })
    
    return export


