from influxdb_client import InfluxDBClient

from datetime import datetime, timedelta
import pytz
from numpy import average

import m_ETo


def time_conversion(time_in_utc):
    # Input UTC timestamp
    utc_timestamp = time_in_utc

    # Convert to a datetime object
    utc_time = datetime.fromisoformat(utc_timestamp)
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # Convert to Sri Lanka Standard Time (Asia/Colombo time zone)
    sri_lanka_time = utc_time.astimezone(pytz.timezone('Asia/Colombo'))
    formatted_date_time = sri_lanka_time.strftime('%Y-%m-%d %H:%M:%S')
    # # Extract the date and time components
    # year = sri_lanka_time.year
    # month = sri_lanka_time.month
    # day = sri_lanka_time.day
    # hour = sri_lanka_time.hour
    # minute = sri_lanka_time.minute
    # second = sri_lanka_time.second

    return formatted_date_time


def open_weather_past(rec_time):
    print(rec_time)
    # print(tag_key)
    try:
        # bucket = "farm_data"
        org = "farm_project"
        token = "7g5omMxTeVgK0ND-cknWiJACb-Y5bJ8TFJiyhQlzbX3cWyPbR0azuO7lLgoHY8eEnQkERoj6pymmG42l3OgybQ=="
        url = "https://us-east-1-1.aws.cloud2.influxdata.com"
        # Query script
        query = f'''
              from(bucket: "farm_data")
                |> range(start: {rec_time})
                |> filter(fn: (r) => r._measurement == "past_data")
        '''

        with (InfluxDBClient(url=url, token=token, org=org) as client):
            query_api = client.query_api()
            tables = query_api.query(query)
            print("Query", tables)

            temp = []
            humi = []
            pressure = []
            time = []
            wind = []
            dateandtime = []
            sunrise = []
            sunset = []

            for table in tables:
                for record in table.records:
                    field_name = record.get_field()
                    field_value = record.get_value()

                    if field_name == "dateandtime":
                        dateandtime.append(field_value)
                    elif field_name == "humidity":
                        humi.append(field_value)
                    elif field_name == "wind_speed":
                        wind.append(field_value)
                    elif field_name == "sunrise":
                        sunrise.append(field_value)
                    elif field_name == "sunset":
                        sunset.append(field_value)
                    elif field_name == "pressure":
                        pressure.append(field_value)
                    elif field_name == "temperature":
                        temp.append(field_value)
                        # get tne timestamp of record
                        sl_time = time_conversion(str(record.get_time()))
                        time.append(sl_time)

            # Sun shine time in seconds
            sun_shine_time = max(sunset) - max(sunrise)
            # Convert time difference to a timedelta object
            time_difference_timedelta = timedelta(seconds=sun_shine_time)
            # Store the time difference as a tuple
            time_difference_tuple = (time_difference_timedelta.days, time_difference_timedelta.seconds // 3600,
                                     (time_difference_timedelta.seconds // 60) % 60,
                                     time_difference_timedelta.seconds % 60)
            sun_shine = f"{time_difference_tuple[1]} Hours {time_difference_tuple[2]} min " \
                        f"{time_difference_tuple[3]} sec "

            m_t = sum(temp) / len(temp)
            mean_temperature = round(m_t, 3)
            m_h = sum(humi) / len(humi)
            mean_humidity = round(m_h, 2)
            m_w_s = sum(wind) / len(wind)
            mean_wind_speed = round(m_w_s, 3)
            pre_t = sum(pressure) / len(pressure)
            mean_pre_level = round(pre_t, 3)

            # calculating the wind speed in day time and nighttime

            u_day = average(wind)
            u_night = u_day + 0.2

            temperature = round(m_ETo.kelvin_to_celsius(mean_temperature), 2)

            return mean_temperature, mean_humidity, mean_pre_level, sun_shine_time, mean_wind_speed, u_day, u_night, \
                temperature, sun_shine
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
        return None
