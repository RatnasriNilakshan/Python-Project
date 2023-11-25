from influxdb_client import InfluxDBClient
import numpy as np
import calibrated_values as cv
from datetime import datetime
import pytz
from numpy import average
import pandas as pd


def time_conversion(time_in_utc):
    # Input UTC timestamp
    utc_timestamp = time_in_utc

    # Convert to a datetime object
    utc_time = datetime.fromisoformat(utc_timestamp)
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # Convert to Sri Lanka Standard Time (Asia/Colombo time zone)
    sri_lanka_time = utc_time.astimezone(pytz.timezone('Asia/Colombo'))
    formatted_date_time = sri_lanka_time.strftime('%Y-%m-%d %H:%M')
    # # Extract the date and time components
    # year = sri_lanka_time.year
    # month = sri_lanka_time.month
    # day = sri_lanka_time.day
    # hour = sri_lanka_time.hour
    # minute = sri_lanka_time.minute
    # second = sri_lanka_time.second

    return formatted_date_time


def real_time_weather(rec_time, tag_key):
    print(rec_time)
    print(tag_key)
    try:
        # bucket = "farm_data"
        org = "farm_project"
        token = "7g5omMxTeVgK0ND-cknWiJACb-Y5bJ8TFJiyhQlzbX3cWyPbR0azuO7lLgoHY8eEnQkERoj6pymmG42l3OgybQ=="
        url = "https://us-east-1-1.aws.cloud2.influxdata.com"
        # Query script
        # query = (f'from(bucket: "farm_data") |> range(start: {rec_time}) |> filter(fn: (r) => r._measurement == '
        #          f'"sensors")')
        query = f'''
              from(bucket: "farm_data")
                |> range(start: {rec_time})
                |> filter(fn: (r) => r._measurement == "sensors")
                |> filter(fn:(r) => r.UUID == "{tag_key}")
        '''

        with InfluxDBClient(url=url, token=token, org=org) as client:
            query_api = client.query_api()
            tables = query_api.query(query)
            # print("Query", tables)

            temp = []
            humi = []
            light = []
            # soil = []
            pressure = []
            time = []
            wind = []

            for table in tables:
                for record in table.records:
                    field_name = record.get_field()
                    field_value = record.get_value()

                    if field_name == "light_intensity":
                        light.append(field_value)
                    elif field_name == "humidity":
                        humi.append(field_value)
                    # elif field_name == "soil_moisture":
                    #     soil.append(field_value)
                    elif field_name == "wind_speed":
                        wind.append(field_value)
                    elif field_name == "pressure":
                        pressure.append(field_value)
                    elif field_name == "temperature":
                        temp.append(field_value)
                        # get tne timestamp of record
                        sl_time = time_conversion(str(record.get_time()))
                        time.append(sl_time)

            light = np.pad(light, (0, len(temp) - len(light)), 'constant')
            time = pd.to_datetime(time, format='%Y-%m-%d %H:%M')
            # Example list
            data = list(zip(
                light,
                humi,
                wind,
                pressure,
                temp,
                time
            ))

            # Define column names
            columns = ["light",
                       "humi",
                       "wind",
                       "pressure",
                       "temp",
                       "time"]

            # Create a Pandas DataFrame
            df = pd.DataFrame(data, columns=columns)
            # df.to_csv("original;.csv", index=False)
            # Set 'time' as the index
            df.set_index('time', inplace=True)

            # Create a new DataFrame with a complete time range
            full_time_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='5T')
            full_df = pd.DataFrame(index=full_time_range)
            # Merge the two DataFrames
            merged_df = pd.merge(full_df, df, left_index=True, right_index=True, how='outer')
            # Interpolate missing values
            interpolated_df = merged_df.interpolate()
            # Reset the index
            interpolated_df.reset_index(inplace=True)

            wind = interpolated_df["wind"].tolist()
            humi = interpolated_df["humi"].tolist()
            light = interpolated_df["light"].tolist()
            temp = interpolated_df["temp"].tolist()
            pressure = interpolated_df["pressure"].tolist()

            print("Temp :", max(temp), min(temp))
            print("Humi : ", max(humi), min(humi))
            # print("Soil Moisture :", max(soil), min(soil))
            print("Light :", max(light), min(light))
            print("Pressure :", max(pressure), min(pressure))
            # print("Soil moisture : ", soil)
            print("Wind speed : ", round(average(wind), 3))
            # print("time:", time)
            print("length of light : ", len(light))
            print("length of temp :", len(temp))
            temp = temp_outlier(temp)
            humi = humi_outlier(humi)
            light = light_outlier(light)
            # soil = soil_outlier(soil).interpolate(method="linear", inplace=True)
            pressure = pressure_outlier(pressure)
            # temperature calibrated value
            temperature = sum(temp) / len(temp)
            print("Temperature before calibration: ", temperature)
            temperature = round((temperature - 1.184817421919231) / 0.9915188746604908, 2)
            print("Temperature after calibration: ", temperature)
            # humidity calibrated value
            humidity = sum(humi) / len(humi)
            print("Humidity before calibration: ", humidity)
            humidity = round((humidity - 2.4511113020988304) / 0.7777099342975464, 2)
            if humidity > 100:
                humidity = humidity = sum(humi) / len(humi)
                humidity = round(humidity, 2)
            print("Humidity after calibration: ", humidity)
            # soil_moisture = round(soil[-1], 3)
            # Light intensity calibrated value
            light_intensity = sum(light) / len(light)
            print("Light before calibration: ", light_intensity)
            light_intensity = round(1.4978395975992413 * light_intensity - 293.23609409636083, 3)
            print("Light after calibration: ", light_intensity)
            # pressure calibrated value
            pressure = round(sum(pressure) / len(pressure), 3)
            print("Pressure before calibration: ", pressure)
            pressure = round((pressure + 348.95271755180147) / 1.006443696772644 / 1000, 3)
            print("pressure after calibration: ", pressure)
            # wind speed adjustments
            coefficients = [6.815215, -28.85605239, 17.79369809, 182.68658296758696]
            y_value = average(wind)
            wind_speed = round(cv.third_order_real_roots(coefficients, y_value), 3)
            print("sensor data :",temperature, humidity, light_intensity, temp, humi, time, pressure, wind_speed)

            return temperature, humidity, light_intensity, temp, humi, time, pressure, wind_speed

    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
        return None


def temp_outlier(temp):
    # Calculate quartiles for temperature
    q1 = np.percentile(temp, 25)
    q2 = np.percentile(temp, 50)
    q3 = np.percentile(temp, 75)

    # Calculate Inter quartile Range (IQR)
    iqr = q3 - q1

    # Calculate Lower Bound and Upper Bound for potential outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    print("Upper bound temp: ", upper_bound)
    print("Lower bound temp: ", lower_bound)

    # Replace potential outliers with lower bound and upper bound
    for i in range(len(temp)):
        if temp[i] < lower_bound:
            temp[i] = lower_bound
        elif temp[i] > upper_bound:
            temp[i] = upper_bound

    return temp


def pressure_outlier(pressure):
    # Calculate quartiles for temperature
    q1 = np.percentile(pressure, 25)
    q2 = np.percentile(pressure, 50)
    q3 = np.percentile(pressure, 75)

    # Calculate Inter quartile Range (IQR)
    iqr = q3 - q1

    # Calculate Lower Bound and Upper Bound for potential outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    print("Upper bound pressure: ", upper_bound)
    print("Lower bound pressure: ", lower_bound)

    # Replace potential outliers with lower bound and upper bound
    for i in range(len(pressure)):
        if pressure[i] < lower_bound:
            pressure[i] = lower_bound
        elif pressure[i] > upper_bound:
            pressure[i] = upper_bound

    return pressure


def humi_outlier(humi):
    # Calculate quartiles for temperature
    q1 = np.percentile(humi, 25)
    q2 = np.percentile(humi, 50)
    q3 = np.percentile(humi, 75)

    # Calculate Inter quartile Range (IQR)
    iqr = q3 - q1

    # Calculate Lower Bound and Upper Bound for potential outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    print("Upper bound humi: ", upper_bound)
    print("Lower bound humi: ", lower_bound)

    # Replace potential outliers with lower bound and upper bound
    for i in range(len(humi)):
        if humi[i] < lower_bound:
            humi[i] = lower_bound
        elif humi[i] > upper_bound:
            humi[i] = upper_bound

    return humi


def light_outlier(light):
    light = [x for x in light if x != 0]
    # Calculate quartiles for temperature
    q1 = np.percentile(light, 25)
    q2 = np.percentile(light, 50)
    q3 = np.percentile(light, 75)

    # Calculate Inter quartile Range (IQR)
    iqr = q3 - q1

    # Calculate Lower Bound and Upper Bound for potential outliers
    lower_bound = 0
    upper_bound = q3 + 1.5 * iqr

    print("Upper bound light: ", upper_bound)
    print("Lower bound light: ", lower_bound)

    # Replace potential outliers with lower bound and upper bound
    for i in range(len(light)):
        if light[i] < lower_bound:
            light[i] = lower_bound
        elif light[i] > upper_bound:
            light[i] = upper_bound

    return light


def soil_outlier(soil):
    # Calculate quartiles for temperature
    q1 = np.percentile(soil, 25)
    q2 = np.percentile(soil, 50)
    q3 = np.percentile(soil, 75)

    # Calculate Interquartile Range (IQR)
    iqr = q3 - q1

    # Calculate Lower Bound and Upper Bound for potential outliers
    lower_bound = 0
    upper_bound = q3 + 1.5 * iqr

    print("Upper bound soil: ", upper_bound)
    print("Lower bound soil: ", lower_bound)

    # Replace potential outliers with lower bound and upper bound
    for i in range(len(soil)):
        if soil[i] < lower_bound:
            soil[i] = lower_bound
        elif soil[i] > upper_bound:
            soil[i] = upper_bound

    return soil


real_time_weather("-3d", "FYP0002")
