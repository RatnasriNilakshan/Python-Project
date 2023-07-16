import requests


# Replace 'CITY_NAME' with the name of the city for which you want weather data
# city = "Homagama"

# Make a GET request to the OpenWeatherMap API
def get_avg_weather(lat, lon, api_key):
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}')
        if response.status_code == 200:
            # Extract the weather data from the response
            avg_weather_data = response.json()

            # Print the response content
            return avg_weather_data
        else:
            print('Failed to retrieve weather data. Status code:', response.status_code)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
