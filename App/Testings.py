# # # import math
# # # def feet_to_meters(feet):
# # #     meters = feet * 0.3048
# # #     return meters
# # #
# # # P = 1011
# # # P_0 = 1006.0
# # # # Altitude = (10 ** (math.log(P/P_0)/5.2558797)-1.0/(-6.8755856 * 10.0 ** (-6.0)))
# # # altitude = 145366 * (1 - (P / 1013.25) ** 0.190284)
# # # print(altitude)
# # # al_m = feet_to_meters(altitude)
# # # print(al_m)
# # # al_m_r = round(al_m, 3)
# # # print(al_m_r)
# # import pandas as pd
# # from influxdb_client import InfluxDBClient
# # from influxdb_client_3 import InfluxDBClient3
# #
# # # Instantiate an InfluxDB client configured for a bucket
# # # client = InfluxDBClient3(
# # #     "https://us-east-1-1.aws.cloud2.influxdata.com",
# # #     database="farm_data",
# # #     token="Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg==")
# # try:
# #     client = InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com",
# #                             token="Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm"
# #                                   "725E2VMxg==", database="farm_data", debug=False)
# #     print(client.ping())
# #
# #     result = client.query_api().query_data_frame(org="farm_project", query=
# #     '''from(bucket: "farm_data")
# #   |> range(start: -2d)
# #   |> filter(fn: (r) => r._measurement == "sensors" and r._field == "temperature" and r.temperature != null)'''
# #
# #     )
# #
# #     print(result.head())
# #     client.__del__()
# #
# #     # Convert the PyArrow Table to a pandas DataFrame.
# #     # dataframe = table.to_pandas()
# #     # print(dataframe)
# #
# #     # Try to ping the server
# #
# #
# # except Exception as e:
# #     print("Connection error:", e)
# # ## aE1wXvbqBM2CA4hd76UydpMn-N4nWKiMOP4tezr85UjgRPpKBJ1I0G1G3wN5ArsocLjGz1rWE6atmiWTJbFV_w==
# # # Execute the query to retrieve all record batches in the stream
# # # formatted as a PyArrow Table.
# #
# #
# # # # Rounding values for the adjustment factor
# # # def get_nearest_rs(number):
# # #     return round(number / 3) * 3
# # # def get_nearest_rh(number):
# # #     return round(number / 30) * 30
# # # def get_nearest_u(number):
# # #     return round(number / 1) * 1
# # # def get_nearest_uday(number):
# # #     return round(number / 3) * 3
# # # # Function to get the adjustment factor
# # # def get_adjustment_factor(csv_file, rs, rh_max, u_day, u_night):
# # #     df = pd.read_csv(csv_file, index_col='Rs mm/day')
# # #     rs = get_nearest_rs(rs)
# # #     rh_mean = get_nearest_rh(rh_max)
# # #     u_ratio = u_day / u_night
# # #     u_ratio = get_nearest_u(u_ratio)
# # #     u_day = get_nearest_uday(u_day)
# # #     return df.at[str(u_day) + ',' + str(u_ratio), str(rs) + ',' + str(rh_mean)]
# # #
# # #
# # # N = get_adjustment_factor('adjustment_factor.csv', 11.2, 85, 3.2, 2.1)
# # # print(N)
# from influxdb_client import InfluxDBClient
# import queries as q
# bucket = "farm_data"
# org = "farm_project"
# token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
# url = "https://us-east-1-1.aws.cloud2.influxdata.com"
#
# sensor_id_1 = 'TLM0100'
# sensor_id_2 = 'TLM0101'
#
# # Attempt to establish a connection
# try:
#     client = InfluxDBClient(url=url, token=token)
#     # Connection successful
#     print("Connection to InfluxDB successful!")
#
#     # Now you can perform operations on the database using the 'client' object
#     query_api = client.query_api()
#
#     # Temperature plot
#     # queryTemp = q.tempWithtime(bucket, 1)
#     result = query_api.query(org=org, query='''SELECT * FROM "sensors" WHERE time >= now() - interval '2 days'
#     AND ("temperature" IS NOT NULL))''')
#     print(result)
#
# except Exception as e:
#     # Connection failed
#     print("Connection to InfluxDB failed:", str(e))


# import influxdb_client
# from influxdb_client.client.write_api import SYNCHRONOUS
#
# bucket = "farm_data"
# org = "farm_project"
# token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
# # Store the URL of your InfluxDB instance
# url="https://us-east-1-1.aws.cloud2.influxdata.com"
#
# client = influxdb_client.InfluxDBClient(
#     url=url,
#     token=token,
#     org=org
# )
#
# # Query script
# query_api = client.query_api()
# query = ('from(bucket: "farm_data")'
#          '|> range(start: -2d)'
#          '|> filter(fn: (r) => r._measurement == "sensors" and r._field == "temperature" and r.temperature != null)')
#
# result = query_api.query(org=org, query=query)
# results = []
# for table in result:
#     for record in table.records:
#         results.append((record.get_field(), record.get_value()))
#
# print(results)

# from influxdb_client import InfluxDBClient
# # import pytz
# # from datetime import datetime
#
#
# # from influxdb_client.client.write_api import SYNCHRONOUS
#
# def real_time_weather(rec_time):
#     bucket = "farm_data"
#     org = "farm_project"
#     token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
#     # Store the URL of your InfluxDB instance
#     url = "https://us-east-1-1.aws.cloud2.influxdata.com"
#
#     # timestamp_obj = datetime.strptime(record_time, "%Y-%m-%d %H:%M:%S.%f%z")
#     # sri_lanka_timezone = pytz.timezone("Asia/Colombo")
#     # timestamp_obj_sri_lanka = timestamp_obj.astimezone(sri_lanka_timezone)
#
#     query = f'from(bucket: "farm_data") |> range(start: {rec_time}) |> filter(fn: (r) => r._measurement == "sensors")'
#     # Query script
#     with InfluxDBClient(url=url, token=token, org=org) as client:
#         query_api = client.query_api()
#
#         tables = query_api.query(query)
#         temp = []
#         humi = []
#         light = []
#         soil = []
#
#         for table in tables:
#             for record in table.records:
#                 field_name = record.get_field()
#                 field_value = record.get_value()
#
#                 if field_name == "light_intensity":
#                     light.append(field_value)
#                 elif field_name == "humidity":
#                     humi.append(field_value)
#                 elif field_name == "soil_moisture":
#                     soil = field_value
#                 elif field_name == "temperature":
#                     temp.append(field_value)
#
#         print("Temp :", sum(temp) / len(temp))
#         print("Humi : ", sum(humi) / len(humi))
#         print("Soil Moisture :", soil)
#         print("Light :", sum(light) / len(light))
#
#         temperature = sum(temp) / len(temp)
#         humidity = sum(humi) / len(humi)
#         soil_moisture = soil
#         light_intensity = sum(light) / len(light)
#
#         return temperature, humidity, soil_moisture, light_intensity
#
#
# real_time_weather("-7d")
# # print(timestamp_obj_sri_lanka)

# print(str(record["_time"]) + " - " + record.get_measurement()
#   + " " + record.get_field() + "=" + str(record.get_value()))

# result = query_api.query(org=org, query=query)
# results = []
# for table in result:
#     for record in table.records:
#         results.append((record.get_field(), record.get_value()))
# import streamlit as st
# import pandas as pd
# import numpy as np
#
# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])
#
# st.line_chart(
#    chart_data, x="col1", y=["col2", "col3"] # Optional
# )

# from datetime import datetime
# import pytz
#
# # Input UTC timestamp
# utc_timestamp = "2023-10-27T05:48:11.435Z"
#
# # Convert to a datetime object
# utc_time = datetime.fromisoformat(utc_timestamp)
# utc_time = utc_time.replace(tzinfo=pytz.UTC)
#
# # Convert to Sri Lanka Standard Time (Asia/Colombo time zone)
# sri_lanka_time = utc_time.astimezone(pytz.timezone('Asia/Colombo'))
#
# # Print the result
# print("UTC Time:", utc_time)
# print("Sri Lanka Standard Time (SLST):", sri_lanka_time)

#
# import requests
#
# import converttime as conv_date

# def get_weather_data(latitude, longitude, api_key):
#     # Make a GET request to the OpenWeatherMap API
#     # response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
#     response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={latitude}&lon={longitude}&date'
#                             f'=2023-10-27&tz=+05:30&appid={api_key}')
#
#
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Extract the weather data from the response
#         weather_data = response.json()
#         # print(weather_data)
#
#         # Access specific weather information
#         # longitude = weather_data['coord']['lon']
#         # latitude = weather_data['coord']['lat']
#         # dateandtime = conv_date.convert_datetime(weather_data['dt'])
#         # temperature = weather_data['main']['temp']
#         # temperature_min = weather_data['main']['temp_min']
#         # temperature_max = weather_data['main']['temp_max']
#         # humidity = weather_data['main']['humidity']
#         # wind_speed = weather_data['wind']['speed']
#         # description = weather_data['weather'][0]['description']
#         # clouds = weather_data['clouds']['all']
#         # sunrise = conv_date.convert_datetime(weather_data['sys']['sunrise'])
#         # sunset = conv_date.convert_datetime(weather_data['sys']['sunset'])
#         # pressure = weather_data['main']['pressure']
#         # sea_level = weather_data['main']['sea_level']
#         # grnd_level = weather_data['main']['grnd_level']
#
#         # Return the weather information
#         return weather_data
#             # longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed, \
#             # description, clouds, sunrise, sunset, pressure, sea_level, grnd_level
#     else:
#         print('Failed to retrieve weather data.')
#         return None, None, None
#
#
# one_call_data = get_weather_data(6.8412384, 80.0034457, '8d4e7706e24a9f1fc59b0b30b7964887')
# print(one_call_data)

# for influx write
# import os, time
# from influxdb_client_3 import InfluxDBClient3, Point
#
# # Define your InfluxDB Cloud credentials
# token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
# org = "farm_project"
# bucket = "farm_project"
# url = "https://us-east-1-1.aws.cloud2.influxdata.com"  # Replace with your InfluxDB Cloud URL
#
# host = "https://us-east-1-1.aws.cloud2.influxdata.com"
#
# client = InfluxDBClient3(host=host, token=token, org=org)
#
# database = "farm_data"
#
#
#
# print("Complete. Return to the InfluxDB UI.")


# import datetime
# import time
# from influxdb_client import InfluxDBClient
# import requests
# from influxdb_client_3 import InfluxDBClient3, Point
# from datetime import datetime
# import pytz
#
# token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
# org = "farm_project"
# bucket = "farm_project"
# host = "https://us-east-1-1.aws.cloud2.influxdata.com"
# client = InfluxDBClient3(host=host, token=token, org=org)
# database = "farm_data"
#
#
# def time_conversion(time_in_utc):
#     # Input UTC timestamp
#     utc_timestamp = time_in_utc
#
#     # Convert to a datetime object
#     utc_time = datetime.fromisoformat(utc_timestamp)
#     utc_time = utc_time.replace(tzinfo=pytz.UTC)
#
#     # Convert to Sri Lanka Standard Time (Asia/Colombo time zone)
#     sri_lanka_time = utc_time.astimezone(pytz.timezone('Asia/Colombo'))
#     #formatted_date_time = sri_lanka_time.strftime('%Y-%m-%d %H:%M:%S')
#
#     return sri_lanka_time
#
#
# def last_weather_time(rec_time, tag_key):
#     try:
#         # bucket = "farm_data"
#         url = "https://us-east-1-1.aws.cloud2.influxdata.com"
#         # Query script
#         # query = (f'from(bucket: "farm_data") |> range(start: {rec_time}) |> filter(fn: (r) => r._measurement == '
#         #          f'"sensors")')
#         query = f'''
#               from(bucket: "farm_data")
#                 |> range(start: {rec_time})
#                 |> filter(fn: (r) => r._measurement == "open_weather")
#                 |> filter(fn:(r) => r.location == "{tag_key}")
#         '''
#
#         with InfluxDBClient(url=url, token=token, org=org) as client:
#             query_api = client.query_api()
#             tables = query_api.query(query)
#             # print("Query", tables)
#             # temp_mean, hum_mean, sea_level, shine_time, wind_speed, latitude, u_day, u_night
#
#             last_time = []
#
#             for table in tables:
#                 for record in table.records:
#                     # get tne timestamp of record
#                     last_time.append(record.get_time())
#
#             return time_conversion(str(max(last_time)))
#     except Exception as e:
#         # Connection failed
#         print("Connection to failed:", str(e))
#         return None
#
#
# print(datetime.now(pytz.timezone('Asia/Colombo')) - last_weather_time(-1, "Homagama"))
import datetime
from influxdb_client import InfluxDBClient
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pytz
import weather_thread as wt
import time
import requests

token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
org = "farm_project"
bucket = "farm_project"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "farm_data"

api_key = '8d4e7706e24a9f1fc59b0b30b7964887'  # API key to openweather
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

        '''

        with InfluxDBClient(url=url, token=token, org=org) as client:
            query_api = client.query_api()
            tables = query_api.query(query)
            print("Query", tables)

            last_time = []

            for table in tables:
                for record in table.records:
                    last_time.append(record.get_time())



            print("Last time saves :", last_time)

            return max(last_time)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
        return None

# today_summary = wt.get_weather_summary(6.844, 80.0024, api_key)
# wt.save_weather(today_summary)
print(last_weather_time("Homagama"))
