import requests

import converttime as conv_date
from datetime import datetime, timezone, timedelta


current_date = datetime.today()

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
from influxdb_client import InfluxDBClient, Point, WriteOptions
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
        point = Point(INFLUXDB_MEASUREMENT).tag("UUID", UUID).tag("location", "Homagama").field(
            "longitude", longitude).field("latitude", latitude).field("dateandtime", dateandtime).field("temperature",
                                                                                                        temperature).field(
            "humidity", humidity).field("wind_speed", wind_speed).field("sunrise", sunrise).field("sunset",
                                                                                                  sunset).field(
            "pressure", pressure)
        write_api = client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=1_000))
        write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
        print("Data written to InfluxDB successfully")
    except Exception as e:
        print(f"Failed to write data to InfluxDB: {str(e)}")

def has_today_data():
    query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "{INFLUXDB_MEASUREMENT}")'
    result = client.query_api().query(query, org=INFLUXDB_ORG)
    return len(result) > 0


def main():
    try:
        while True:
            if not has_today_data():
                # Today's data is not present in InfluxDB, retrieve and save it
                longitude, latitude, dateandtime, temperature, humidity, wind_speed, sunrise, sunset, pressure = (
                    get_weather_data(6.8412384, 80.0034457, '8d4e7706e24a9f1fc59b0b30b7964887', timestamp))
                success = write_to_influxdb(longitude, latitude, dateandtime, temperature, humidity, wind_speed,
                                            sunrise, sunset, pressure)
                if success:
                    print("Data written to InfluxDB successfully")
                else:
                    print(f"Failed to write data to InfluxDB: {client}")

            # time.sleep(1800)  # Delay for 30 minutes (600 seconds)
            return None
    except KeyboardInterrupt:
        print("Program terminated by user.")
        return None
