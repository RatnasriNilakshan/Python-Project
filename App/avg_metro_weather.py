import datetime

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


# Find the average values of weather for the selected days
def find_avg_weather(json_data, days):
    if json_data is None or 'list' not in json_data:
        return None, None, None

    date_time = [item['dt'] for item in json_data['list'][:(days * 8)]]
    temperatures = [item['main']['temp'] for item in json_data['list'][:(days * 8)]]
    # temperatures_min = [item['main']['temp_min'] for item in json_data['list'][:(days * 8)]]
    # temperatures_max = [item['main']['temp_max'] for item in json_data['list'][:(days * 8)]]
    humidity = [item['main']['humidity'] for item in json_data['list'][:(days * 8)]]
    rainfalls = [item.get('rain', {}).get('3h', 0) for item in json_data['list'][: (days * 8)]]
    pressure = [item['main']['pressure'] for item in json_data['list'][:(days * 8)]]
    sea_level = [item['main']['sea_level'] for item in json_data['list'][:(days * 8)]]
    # grnd_level = [item['main']['grnd_level'] for item in json_data['list'][:(days * 8)]]
    wind_speed = [item['wind']['speed'] for item in json_data['list'][:(days * 8)]]
    sun_rise = json_data['city']['sunrise']
    sun_set = json_data['city']['sunset']
    # Sun shine time in seconds
    sun_shine_time = sun_set - sun_rise
    # Convert time difference to a timedelta object
    time_difference_timedelta = datetime.timedelta(seconds=sun_shine_time)
    # Store the time difference as a tuple
    time_difference_tuple = (time_difference_timedelta.days, time_difference_timedelta.seconds // 3600,
                             (time_difference_timedelta.seconds // 60) % 60, time_difference_timedelta.seconds % 60)
    sun_shine = f"{time_difference_tuple[1]} Hours {time_difference_tuple[2]} min " \
                f"{time_difference_tuple[3]} sec "

    m_t = sum(temperatures) / len(temperatures)
    mean_temperature = round(m_t, 3)
    m_h = sum(humidity) / len(humidity)
    mean_humidity = round(m_h, 2)
    m_w_s = sum(wind_speed) / len(wind_speed)
    mean_wind_speed = round(m_w_s, 3)
    total_rainfall = round(sum(rainfalls), 3)
    sl_t = sum(sea_level) / len(sea_level)
    mean_sea_level = round(sl_t, 3)
    pre_t = sum(pressure) / len(pressure)
    mean_pre_level = round(pre_t, 3)

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

    return mean_temperature, mean_humidity, total_rainfall, mean_wind_speed, sun_shine, sun_shine_time, \
        mean_sea_level, u_day, u_night, mean_pre_level, temperatures, humidity, wind_speed, date_time
