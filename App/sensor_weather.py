from influxdb_client import InfluxDBClient
import numpy as np

from datetime import datetime
import pytz


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


def real_time_weather(rec_time, tag_key):
    try:
        # bucket = "farm_data"
        org = "farm_project"
        token = "Xl1akcWonZAgMksXlOOizTmNa_jhJ_zWGBwy_KahCAHcH14C9d9iE3ISnDEDBoPnZP9d32oA2KEnm725E2VMxg=="
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
            soil = []
            pressure = []
            time = []

            for table in tables:
                for record in table.records:
                    field_name = record.get_field()
                    field_value = record.get_value()

                    if field_name == "light_intensity":
                        light.append(field_value)
                    elif field_name == "humidity":
                        humi.append(field_value)
                    elif field_name == "soil_moisture":
                        soil.append(field_value)
                    elif field_name == "pressure":
                        pressure.append(field_value)
                    elif field_name == "temperature":
                        temp.append(field_value)
                        # get tne timestamp of record
                        sl_time = time_conversion(str(record.get_time()))
                        time.append(sl_time)

            print("Temp :", max(temp), min(temp))
            print("Humi : ", max(humi), min(humi))
            print("Soil Moisture :", max(soil), min(soil))
            print("Light :", max(light), min(light))
            print("Pressure :", max(pressure), min(pressure))
            print("Soil moisture : ", soil)
            # print("time:", time)

            temp = temp_outlier(temp).interpolate(method="linear", inplace=True)
            humi = humi_outlier(humi).interpolate(method="linear", inplace=True)
            light = light_outlier(light).interpolate(method="linear", inplace=True)
            soil = soil_outlier(soil).interpolate(method="linear", inplace=True)
            pressure = pressure_outlier(pressure).interpolate(method="linear", inplace=True)

            temperature = round(sum(temp) / len(temp), 2)
            humidity = round(sum(humi) / len(humi), 2)
            soil_moisture = round(soil[-1], 3)
            light_intensity = round(sum(light) / len(light), 3)
            pressure = round((sum(pressure) / len(pressure) / 1000), 3)

            return temperature, humidity, soil_moisture, light_intensity, temp, humi, time, pressure, soil
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
