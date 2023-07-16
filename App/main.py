import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import metro_weather as metro
import metro_weather as mw
import geocoder
import avg_metro_weather as amw
import requests

st.set_page_config(
    page_title="RG4_AGRO",
    # page_icon="favicon.ico",
    # layout="wide"
)


# Function to find the current longitude and latitude
# def get_current_location(address):
#     g = geocoder.google(address)
#     if g.latlng:
#         latitude_cur, longitude_cur = g.latlng
#         return latitude_cur, longitude_cur
#     else:
#         return None, None

# Find the location longitude and latitude
def find_location(city):
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=8d4e7706e24a9f1fc59b0b30b7964887')
        if response.status_code == 200:
            # Extract the weather data from the response
            location_details = response.json()
            longitude = location_details[0]['lon']
            latitude = location_details[0]['lat']

            # Print the response content
            return longitude, latitude
        else:
            print('Failed to retrieve location data. Status code:', response.status_code)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))


# Find the average values of weather for the selected days
def find_avg_weather(json_data, days):
    if json_data is None or 'list' not in json_data:
        return None, None, None

    temperatures = [item['main']['temp'] for item in json_data['list'][:(days * 8)]]
    humidities = [item['main']['humidity'] for item in json_data['list'][:(days * 8)]]
    rainfalls = [item.get('rain', {}).get('3h', 0) for item in json_data['list'][: (days * 8)]]

    return temperatures, humidities, rainfalls


Plant_varieties = ["Chilli", "Tomato"]
cities = ["Homagama", "Colombo", 'Jaffna', 'Kandy']
days = [1, 2, 3, 4, 5]

st.title("RG_04")
location = st.selectbox("Select your city", cities, index=0)
api_key = '8d4e7706e24a9f1fc59b0b30b7964887'

Longitude, Latitude = find_location(location)
# find the current location
# latitude, longitude = get_current_location(location)
# Call the get_weather_data function to retrieve the weather information
if st.button("Find weather data"):
    longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed, \
        description, clouds, sunrise, sunset, pressure, sea_level, grnd_level = mw.get_weather_data(api_key, location)
    readings = "Longitude : {} <br> Latitude : {} <br> Access Date and Time : {} <br> Temperature : {} K <br> " \
               "Min_Temperature : {} K <br> Max_Temperature : {} K <br> Humidity : {} % <br> Wind Speed : {} m/s <br>" \
               "Description : {} <br> Clouds : {} % <br> Sunrise : {} <br> Sunset : {} <br> Pressure : {} <br> " \
               "Sea Level : {} <br> Ground Level : {} <br>" \
        .format(longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed,
                description, clouds, sunrise, sunset, pressure, sea_level, grnd_level)
    # st.write('Temperature : ', temperature, 'K',
    #          'Min_Temperature : ', temperature_min, 'K',
    #          'Max_Temperature : ', temperature_max, 'K',
    #          'Humidity : ', humidity, '%',
    #          'Wind Speed : ', wind_speed, 'm/s'
    #          'Clouds : ', description)
    st.write(readings, unsafe_allow_html=True)

days_count = st.selectbox("Select number of days", days, index=1)

if st.button("Find Average data"):

    if Latitude is not None and Longitude is not None:
        st.write("Latitude:", Latitude)
        st.write("Longitude:", Longitude)
        avg_weather_data = amw.get_avg_weather(Latitude, Longitude, api_key)
        temperatures, humidities, rainfalls = find_avg_weather(avg_weather_data, days_count)
        st.write("Average Temperatures:", temperatures)
        st.write("Average Humidities:", humidities)
        st.write("Rainfalls:", rainfalls)
    else:
        st.write("Location not found or error occurred.")


plant_type = st.selectbox("Select the plant category", Plant_varieties)
last_irrigation_date = st.date_input("Enter the last irrigated date")
last_irrigation_time = st.time_input("Enter the last irrigated time")
