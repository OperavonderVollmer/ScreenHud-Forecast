from Forecast import Forecast
from OperaPowerRelay import opr

if __name__ == '__main__':
    CITY = opr.input_from("Forecast", "Enter City")
    forecast = Forecast.get_forecast(CITY)

    opr.print_from("Forecast", f"Forecast for {forecast[0]['city']}")

    for f in forecast:
        print(f"Date: {f['date']}, Time: {f['timeUS']}, Forecast: {f['forecast']},  Temp: {f['tempC']}°c/{f['tempF']}°f")

