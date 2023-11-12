import datetime
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pytz
from influxdb_client import InfluxDBClient
# import time
import requests

# call the data from the influxdb
token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
org = "farm_project"
bucket = "farm_project"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "farm_data"


def time_conversion(time_in_utc):
    # Input UTC timestamp
    utc_timestamp = time_in_utc

    # Convert to a datetime object
    utc_time = datetime.fromisoformat(utc_timestamp)
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # Convert to Sri Lanka Standard Time (Asia/Colombo time zone)
    sri_lanka_time = utc_time.astimezone(pytz.timezone('Asia/Colombo'))
    # formatted_date_time = sri_lanka_time.strftime('%Y-%m-%d %H:%M:%S')

    return sri_lanka_time


def last_weather_time(tag_key):
    try:
        # bucket = "farm_data"
        # Query script
        # query = (f'from(bucket: "farm_data") |> range(start: {rec_time}) |> filter(fn: (r) => r._measurement == '
        #          f'"sensors")')
        query = f'''
              from(bucket: "farm_data")
                |> range(start: -2d)
                |> filter(fn: (r) => r._measurement == "open_weather_save")
                |> filter(fn:(r) => r._field == "location")
                |> filter(fn:(r) => r._value == "{tag_key}")
        '''

        with InfluxDBClient(url=url, token=token, org=org) as client:
            query_api = client.query_api()
            tables = query_api.query(query)
            # print("Query", tables)

            last_time = []
            light = []
            humi = []

            for table in tables:
                for record in table.records:
                    field_name = record.get_field()
                    field_value = record.get_value()
                    if field_name == "light_intensity":
                        light.append(field_value)
                    elif field_name == "humidity":
                        humi.append(field_value)
                    last_time.append(record.get_time())
            print("Last time saves :", last_time)
            print("Light :", light)
            print("Humi :", humi)

            return max(last_time)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
        return None


def get_weather_summary(lat, lon, api_key):
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


def save_weather(json_data):
    days = 1
    if json_data is None or 'list' not in json_data:
        return None, None, None

    date_time = [item['dt'] for item in json_data['list'][:(days * 8)]]
    temperatures = [item['main']['temp'] for item in json_data['list'][:(days * 8)]]
    # temperatures_min = [item['main']['temp_min'] for item in json_data['list'][:(days * 8)]]
    # temperatures_max = [item['main']['temp_max'] for item in json_data['list'][:(days * 8)]]
    humidity = [item['main']['humidity'] for item in json_data['list'][:(days * 8)]]
    rainfalls = [item.get('rain', {}).get('3h', 0) for item in json_data['list'][: (days * 8)]]
    pressure = [item['main']['pressure'] for item in json_data['list'][:(days * 8)]]
    # sea_level = [item['main']['sea_level'] for item in json_data['list'][:(days * 8)]]
    # grnd_level = [item['main']['grnd_level'] for item in json_data['list'][:(days * 8)]]
    wind_speed = [item['wind']['speed'] for item in json_data['list'][:(days * 8)]]
    sun_rise = json_data['city']['sunrise']
    sun_set = json_data['city']['sunset']
    city = json_data['city']['name']
    latitude = json_data['city']['coord']['lat']
    # Sun shine time in seconds
    sun_shine_time = sun_set - sun_rise
    # Convert time difference to a timedelta object
    # time_difference_timedelta = datetime.timedelta(seconds=sun_shine_time)
    # Store the time difference as a tuple
    # time_difference_tuple = (time_difference_timedelta.days, time_difference_timedelta.seconds // 3600,
    #                          (time_difference_timedelta.seconds // 60) % 60, time_difference_timedelta.seconds % 60)
    # sun_shine = f"{time_difference_tuple[1]} Hours {time_difference_tuple[2]} min " \
    #             f"{time_difference_tuple[3]} sec "

    m_t = sum(temperatures) / len(temperatures)
    mean_temperature = round(m_t, 3)
    m_h = sum(humidity) / len(humidity)
    mean_humidity = round(m_h, 2)
    m_w_s = sum(wind_speed) / len(wind_speed)
    mean_wind_speed = round(m_w_s, 3)
    total_rainfall = round(sum(rainfalls), 3)
    # sl_t = sum(sea_level) / len(sea_level)
    # mean_sea_level = round(sl_t, 3)
    pre_t = sum(pressure) / len(pressure)
    mean_pre_level = round(pre_t / 10, 3)

    # calculating the wind speed in day time and nighttime
    u_day_avg = []
    u_night_avg = []
    count = 0
    for speed in wind_speed:
        if count < 4:
            u_day_avg.append(speed)
        elif count < 8:
            u_night_avg.append(speed)
        elif count > 7:
            count = 0
        count += 1
    u_day = sum(u_day_avg) / len(u_day_avg)
    u_night = sum(u_night_avg) / len(u_night_avg)
    # temp_mean, hum_mean, sea_level, shine_time, wind_speed, latitude, u_day, u_night
    # Create a single point with multiple fields
    point = (
        Point("open_weather_save")
        .tag("location", city)
        .field("temperature", mean_temperature)
        .field("humidity", mean_humidity)
        .field("pressure", mean_pre_level)
        .field("sunshine", sun_shine_time)
        .field("wind_speed", mean_wind_speed)
        .field("latitude", latitude)
        .field("u_day", u_day)
        .field("u_night", u_night)
        .field("rainfall", total_rainfall)
        .time(time=datetime.fromtimestamp(date_time[0]))
    )

    # Write the point to InfluxDB
    client = InfluxDBClient3(host=url, token=token, org=org)
    client.write(database=database, record=point)

    print("Day summary weather data uploaded")
    # time.sleep(24 * 60 * 60)

    return None
    # (
    # mean_temperature, mean_humidity, total_rainfall, mean_wind_speed, sun_shine, sun_shine_time, \
    # mean_sea_level, u_day, u_night, mean_pre_level, temperatures, humidity, wind_speed, date_time)


# for influx write


# Define your InfluxDB Cloud credentials


print("Complete. Return to the InfluxDB UI.")
