#!/usr/bin/env python3

import pyowm
from os import getenv

api_key = getenv('OPENWEATHER_API_KEY',
                 'REPLACE_THIS_WITH_THE_ACTUAL_API_KEY')
city_name = getenv('CITY_NAME', 'Zagreb')

# Make sure that the variables aren't empty
if getenv('CITY_NAME') == "":
    city_name = 'Zagreb'

if getenv('OPENWEATHER_API_KEY') == "":
    api_key = 'REPLACE_THIS_WITH_THE_ACTUAL_API_KEY'

if api_key != 'REPLACE_THIS_WITH_THE_ACTUAL_API_KEY':
    owm = pyowm.OWM(api_key)
    owm_city = owm.weather_at_place(city_name)
    weather = owm_city.get_weather()

    temperature = weather.get_temperature('celsius')['temp']
    humidity = weather.get_humidity()
    status = weather.get_detailed_status()

    output = ('source=openweathermap, city="{}", description="{}", '
              'temp={}, humidity={}').format(city_name, status,
                                             temperature, humidity)

    print(output)

else:
    print("API key variable not set, skipping weather check.")
