import requests

import converttime as conv_date


def get_weather_data(latitude, longitude, api_key):
    # Make a GET request to the OpenWeatherMap API
    # response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}'
                            f'&lon={longitude}&appid={api_key}')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the weather data from the response
        weather_data = response.json()
        # print(weather_data)

        # Access specific weather information
        longitude = weather_data['coord']['lon']
        latitude = weather_data['coord']['lat']
        dateandtime = conv_date.convert_datetime(weather_data['dt'])
        temperature = weather_data['main']['temp']
        temperature_min = weather_data['main']['temp_min']
        temperature_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
        clouds = weather_data['clouds']['all']
        sunrise = conv_date.convert_datetime(weather_data['sys']['sunrise'])
        sunset = conv_date.convert_datetime(weather_data['sys']['sunset'])
        pressure = weather_data['main']['pressure']
        sea_level = weather_data['main']['sea_level']
        grnd_level = weather_data['main']['grnd_level']

        # Return the weather information
        return longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed, \
            description, clouds, sunrise, sunset, pressure, sea_level, grnd_level
    else:
        print('Failed to retrieve weather data.')
        return None, None, None

# Get current location

# import requests
# api_key = '8d4e7706e24a9f1fc59b0b30b7964887'
# # Replace 'CITY_NAME' with the name of the city for which you want weather data
# city = "Homagama"
# lat = 6.844
# lon = 80.0024
# # Make a GET request to the OpenWeatherMap API
# try:
#     response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}')
#     if response.status_code == 200:
#         # Extract the weather data from the response
#         weather_data = response.json()
#
#         # Print the response content
#         print(weather_data)
#     else:
#         print('Failed to retrieve weather data. Status code:', response.status_code)
# except Exception as e:
#     # Connection failed
#     print("Connection to failed:", str(e))
