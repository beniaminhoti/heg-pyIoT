import os
import pyowm
from dotenv import load_dotenv

load_dotenv('.env')

# OpenWeatherMap API key
# OWM_API = os.environ.get('OWM_API') // Il faut "source .env" avant de lancer le script
OWM_API = os.getenv('OWM_API') 


def getWeather(location):
    """Function to get weather data from OpenWeatherMap API

    :param location: Location to get weather data from
    :return: Temperature in Celcius
    """
    try:
        owm = pyowm.OWM(OWM_API)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location).weather

        weather_dict = observation.to_dict()
        temp = round(weather_dict['temperature']
                     ['temp'] - 273.15, 1)  # in Celcius

        return temp
    except pyowm.exceptions.api_response_error.NotFoundError:
        return None


def main():
    location: str = input("Enter city name: ")
    print(getWeather(location))


if __name__ == "__main__":
    main()
