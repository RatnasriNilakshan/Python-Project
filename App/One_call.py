import requests

import converttime as conv_date
from datetime import datetime, timezone, timedelta

start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 11, 14)

current_date = start_date
# while current_date <= end_date:
#     timestamp = int(current_date.timestamp())
#     print(f"{current_date.strftime('%Y-%m-%d')} - Unix Timestamp: {timestamp}")
#     # Convert Unix timestamp to date and time
#     dt_object = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
#     formatted_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S %Z')
#
#     # Print the result
#     print("Date and Time:", formatted_date_time)
#
#
#     current_date += timedelta(days=1)
timestamp = int(current_date.timestamp())
def get_weather_data(latitude, longitude, api_key, timestamp):
    # Make a GET request to the OpenWeatherMap API
    # response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
    # response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={latitude}&lon={longitude}&date'
    #                         f'=2023-10-27&tz=+05:30&appid={api_key}')
    response = requests.get(
        f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={latitude}&lon={longitude}&dt={timestamp}&appid={api_key}')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the weather data from the response
        weather_data = response.json()
        # print(weather_data)

        # Access specific weather information
        longitude = weather_data['lon']
        latitude = weather_data['lat']
        dateandtime = weather_data['data'][0]['dt']
        temperature = weather_data['data'][0]['temp']
        # temperature_min = weather_data['temperature']['min']
        # temperature_max = weather_data['temperature']['max']
        humidity = weather_data['data'][0]['humidity']
        wind_speed = weather_data['data'][0]['wind_speed']
        # description = weather_data['weather'][0]['description']
        # clouds = weather_data['clouds']['all']
        sunrise = weather_data['data'][0]['sunrise']
        sunset = weather_data['data'][0]['sunset']
        pressure = weather_data['data'][0]['pressure']
        # sea_level = weather_data['main']['sea_level']
        # grnd_level = weather_data['main']['grnd_level']

        # print these parameters
        print("Longitude:", longitude)
        print("Latitude:", latitude)
        print("Date and Time:", dateandtime)
        print("Temperature: ", temperature)
        # print("Min Temperature:", temperature_min)
        # print("Max Temperature:", temperature_max)
        print("Humidity:", humidity)
        print("Wind Speed:", wind_speed)
        # print("Description:", description)
        # print("Clouds:", clouds)
        print("Sunrise:", sunrise)
        print("Sunset:", sunset)
        print("Pressure:", pressure)
        # print("Sea Level:", sea_level)
        # print("Ground Level:", grnd_level)

        # Return the weather information
        return longitude, latitude, dateandtime, temperature, humidity, wind_speed, sunrise, sunset, pressure
        # longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed, \
        # description, clouds, sunrise, sunset, pressure, sea_level, grnd_level
    else:
        print('Failed to retrieve weather data.')
        return None, None, None
from influxdb_client import InfluxDBClient, Point
from datetime import datetime
import time

# Define constants

INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN = "7g5omMxTeVgK0ND-cknWiJACb-Y5bJ8TFJiyhQlzbX3cWyPbR0azuO7lLgoHY8eEnQkERoj6pymmG42l3OgybQ=="
INFLUXDB_ORG = "farm_project"
INFLUXDB_BUCKET = "farm_data"
INFLUXDB_MEASUREMENT = "past_data"
TZ_INFO = "IST-5:30"
UUID = "FYP0003"

# Create InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG, debug=True)


def write_to_influxdb(longitude, latitude, dateandtime,temperature, humidity, wind_speed, sunrise, sunset, pressure):
    try:
        json_body = [
            {
                "measurement": INFLUXDB_MEASUREMENT,
                "tags": {"UUID": UUID, "location": "Homagama"},
                "fields": {
                    "longitude": longitude,
                    "latitude": latitude,
                    "dateandtime": dateandtime,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "sunrise": sunrise,
                    "sunset": sunset,
                    "pressure": pressure,
                },
            }
        ]
        client.write_points(json_body)
        print("Data written to InfluxDB successfully")
    except Exception as e:
        print(f"Failed to write data to InfluxDB: {str(e)}")

def main():
    try:
        while True:
            longitude, latitude, dateandtime, temperature, humidity, wind_speed, sunrise, sunset, pressure = (
                get_weather_data(6.8412384, 80.0034457, '8d4e7706e24a9f1fc59b0b30b7964887', timestamp))
            # print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Light Intensity: {light_intensity} lux, Pressure: {pressure} hPa")

            if temperature > 5:  # Check if the sensor is working
                success = write_to_influxdb(longitude, latitude, dateandtime, temperature, humidity, wind_speed, sunrise, sunset, pressure)
                if success:
                    print("Data written to InfluxDB successfully")
                else:
                    print(f"Failed to write data to InfluxDB: {client}")

            time.sleep(600)  # Delay for 10 minutes (600 seconds)

    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()
