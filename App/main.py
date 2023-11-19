import streamlit as st
import metro_weather as mw
import avg_metro_weather as amw
import npk as npk
import weather_thread as wt
import requests
import pandas as pd
import pytz
# import time
# import matplotlib.pyplot as plt
# import numpy as np
# import metro_weather as metro
# from _datetime import datetime
# import geocoder
import m_ETo as m_ETo
import s_ETo as s_ETo
import datetime
import sensor_weather as s_w
from datetime import datetime, timedelta

# def get_current_location():
#     # Initialize the geocoder
#     g = geocoder.ip('me')
#
#     if g.ok:
#         # Get latitude and longitude
#         lat, lon = g.latlng
#         return lat, lon
#     else:
#         # Geocoder failed to fetch the location
#         print("Failed to get the current location.")
#         return None


# Get the current location
# Latitude, Longitude = get_current_location()

api_key = '8d4e7706e24a9f1fc59b0b30b7964887'  # API key to openweather
Plant_varieties = ["Chilli", "Tomato"]  # The plant categories
cities = ["Homagama", "Colombo", 'Jaffna', 'Kandy', "Mannar",
          "Anuradhapura"]  # Names of cities that can find from openweather
m_days = [1, 2, 3, 4, 5]  # Number of days need to collect weather data, maximum 5
s_days = ["-1d", "-2d", "-3d", "-4d", "-5d", "-6d", "-7d", "-10d", "-12d", "-15d", "-30d"]

st.set_page_config(
    page_title="RG4_AGRO",
    page_icon="🌱",
    layout="wide"
)


# timestamp to date and time
def convert_datetime(timestamp):
    # Convert the Unix timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(timestamp)

    # Format the datetime object as a string
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    # Print the formatted datetime
    return formatted_datetime


# Find the location longitude and latitude
def find_location(city):
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=8d4e7706e24a9f1fc59b0b30b7964887')
        if response.status_code == 200:
            # Extract the weather data from the response
            location_details = response.json()
            lon = location_details[0]['lon']
            lat = location_details[0]['lat']

            # Print the response content
            return lon, lat
        else:
            print('Failed to retrieve location data. Status code:', response.status_code)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))


st.title("🌿 RG_04 AGRO Data Preview")
# Sidebar Formatting
st.sidebar.write("**Options**")  # Sidebar Title
# User options to filter data
current_weather_check = st.sidebar.checkbox("Current Weather", value=True)
refresh_current_weather = st.sidebar.button("Refresh 🔄")
# sensor node selection
sensors = ["FYP0001", "FYP0002"]
weather_station = "FYP0002"
sensor_node = st.sidebar.selectbox("Selection the sensor node", sensors)
location = st.sidebar.selectbox("Select your area", cities, index=0)  # Define the location
m_days_count = st.sidebar.selectbox("Select number of days (future)", m_days,
                                    index=4)  # Define the days to collect data
# s_days_count = st.sidebar.selectbox("Select number of days (past)", s_days, index=10)
# show_avg_weather = st.sidebar.button("Find Average data")
plant_type = st.sidebar.selectbox("Select the crop type", Plant_varieties)
# minimum area
if plant_type == "Tomato":
    min_value = 0.4
elif plant_type == "Chilli":
    min_value = 0.36
else:
    min_value = 0.0  # Set a default value if the plant type is not recognized
filed_area = st.sidebar.number_input("Enter the field area in meter square", min_value=min_value)
current_date = datetime.now().date()
new_date = current_date - timedelta(days=7)
planted_date = st.sidebar.date_input("Enter the planting date", value=new_date)
plantation_days = (current_date - planted_date).days
# Show the irrigation menu
# if show_irrigation:
st.sidebar.header("Irrigation Details")
col_irr_1, col_irr_2 = st.sidebar.columns(2)
with col_irr_1:
    last_irrigation_date = st.date_input("Enter the last irrigation date", current_date - timedelta(days=2))
with col_irr_2:
    last_irrigation_time = st.time_input("Enter the last irrigation time")
last_irrigated_amount = st.sidebar.number_input("Enter the amount of water irrigation last time in litres",
                                                value=filed_area)

# Show the fertilization menu
# if show_fertilization:
# st.sidebar.header("Fertilization Details")
# col_fer_1, col_fer_2 = st.sidebar.columns(2)
# with col_fer_1:
#     last_fertilization_date = st.date_input("Enter the last fertilization date",
#                                             current_date - timedelta(days=5))
# with col_fer_2:
#     last_fertilization_time = st.time_input("Enter the last fertilization time")

# Date and time difference calculations
combined_date_irr = datetime.combine(last_irrigation_date, last_irrigation_time)
time_diff_irr = round((combined_date_irr - datetime.now()).total_seconds() / (60 * 60 * 24))
print("Irrigation time difference : ", time_diff_irr)
print("Irrigation Combine date : ", combined_date_irr)
# combined_date_fer = datetime.combine(last_fertilization_date, last_fertilization_time)
# time_diff_fer = round((combined_date_fer - datetime.now()).total_seconds() / (60 * 60 * 24))


# show_irrigation = st.sidebar.button("Irrigation")
# show_fertilization = st.sidebar.button("Fertilization")
# Find age of crop
def define_age_of_crop(crop, days):
    if crop == "Tomato":
        if days < 30:
            return "Early"
        if days < 110:
            return "Mid"
        if days >= 110:
            return "End"
    if crop == "Chilli":
        if days < 20:
            return "Early"
        if days < 40:
            return "Mid"
        if days >= 40:
            return "End"


def get_crop_coefficient(csv_file):
    df = pd.read_csv(csv_file, index_col='Crop')
    crop = plant_type
    # print(crop)
    days_diff = plantation_days
    age = define_age_of_crop(crop, days_diff)
    # print("Age", age)
    # print(df.at[crop, age])
    return df.at[crop, age]


# find the current location
Longitude, Latitude = find_location(location)


# Call the get_weather_data function to retrieve the weather information
def get_current_weather():
    longitude, latitude, dateandtime, temperature, temperature_min, temperature_max, humidity, wind_speed, \
        description, clouds, sunrise, sunset, pressure, sea_level, grnd_level = mw.get_weather_data(Latitude, Longitude,
                                                                                                    api_key)
    readings = f"""<title>Current weather data</title><style> div.container {{background-color: #666;}}div.container p
                 {{font-family: Arial;font-size: 14px;font-style: normal;font-weight: normal;text-decoration: none;
                 text-transform: none;background-color: #666;}}</style><div class="container">
                 <table style="height: 76px; width: 100%;">
    <tbody>
    <tr style="height: 22px;">
    <td style="width: 118px; height: 22px;" colspan="2">Access Time: {dateandtime}</td>
    <td style="width: 162.575px; height: 22px;" colspan="2">
    <p>Wind Speed 💨: {wind_speed} m/s</p>
    <p>Humidity 🫧: {humidity} %</p>
    </td>
    </tr>
    <tr style="height: 22px;">
    <td style="width: 118px; height: 22px;">Location 📍 &nbsp;</td>
    <td style="width: 123px; height: 22px;">&nbsp;Temperature 🌡️: {temperature} K</td>
    <td style="width: 162.575px; height: 22px;">&nbsp;Sun 🌞</td>
    <td style="width: 135.425px; height: 22px;">&nbsp;Pressure 🌡: {pressure} hPa</td>
    </tr>
    <tr style="height: 42px;">
    <td style="width: 118px; height: 42px;">Latitude: {latitude}&nbsp;</td>
    <td style="width: 123px; height: 42px;">Max: {temperature_max} K&nbsp;</td>
    <td style="width: 162.575px; height: 42px;">Rise Time: {sunrise}&nbsp;</td>
    <td style="width: 135.425px; height: 42px;">Sea Level: {sea_level} hPa&nbsp;</td>
    </tr>
    <tr style="height: 22.8px;">
    <td style="width: 118px; height: 22.8px;">Longitude: {longitude}&nbsp;</td>
    <td style="width: 123px; height: 22.8px;">Min: {temperature_min} K&nbsp;</td>
    <td style="width: 162.575px; height: 22.8px;">Set Time: {sunset}&nbsp;</td>
    <td style="width: 135.425px; height: 22.8px;">Ground Level: {grnd_level} hPa&nbsp;</td>
    </tr>
    <tr style="height: 22.8px;">
    <td style="width: 241px; height: 22.8px;" colspan="2">Description: {description}</td>
    <td style="width: 162.575px; height: 22.8px;" colspan="2">Clouds ☁️: {clouds} %</td>
    </tr>
    </tbody>
    </table></div>"""
    # st.write('Temperature : ', temperature, 'K',
    #          'Min_Temperature : ', temperature_min, 'K',
    #          'Max_Temperature : ', temperature_max, 'K',
    #          'Humidity : ', humidity, '%',
    #          'Wind Speed : ', wind_speed, 'm/s'
    #          'Clouds : ', description)
    return readings


# Create a boolean flag to control data display
show_current_weather = True

# Display the data by default
current_weather_data = get_current_weather()
if show_current_weather and current_weather_check:
    st.header("Current weather data")
    st.write(current_weather_data, unsafe_allow_html=True)

# Create a button with the label "Refresh Data"
if refresh_current_weather:
    # Set the flag too False to hide the data temporarily
    show_current_weather = False

# When the button is pressed, fetch and display the data
if not show_current_weather:
    updated_data = get_current_weather()
    if updated_data:
        # st.write(current_weather_data, unsafe_allow_html=True)
        # Set the flag back to True to show the data again
        current_weather_data = updated_data
        show_current_weather = True

# Find/Show the days average weather data
# if show_avg_weather:

# NPK values


if Latitude is not None and Longitude is not None:
    # st.write("Latitude:", Latitude)
    # st.write("Longitude:", Longitude)
    # last_weather_time = amw.last_weather_time(time_diff_irr, location)
    # time_diff_data = datetime.now(pytz.timezone('Asia/Colombo')) - last_weather_time
    # call api to collect the data
    avg_weather_data = amw.get_avg_weather(Latitude, Longitude, api_key)
    # avg_weather_data = amw.get_avg_weather(Latitude, Longitude, api_key)
    (mean_temperature, mean_humidity, total_rainfall, mean_wind_speed, sun_shine, sun_shine_time,
     mean_sea_level, u_day, u_night, mean_pre_level, m_temperatures, m_humidity,
     m_wind_speed, m_date_time) = amw.find_avg_weather(avg_weather_data, m_days_count)
    # Show the location log and lat according to the selected city
    st.header("Location 📌")
    st.write("Lat : ", Latitude)
    st.write("Log : ", Longitude)
    # Calculating water requirement
    m_eto = m_ETo.calculate_et0(mean_temperature, mean_humidity, mean_sea_level, sun_shine_time,
                                mean_wind_speed, Latitude, u_day, u_night)
    # Find crop coefficient factor
    kc = get_crop_coefficient('App\\cropcoefficient.csv')
    # Calculate crop water requirement
    m_crw = round(m_eto * kc, 3)
    st.header("Weather data")
    # create three columns to show the irrigation related details with metro data
    m_Col1, m_Col2, m_Col3 = st.columns(3)
    # fill in those three columns with respective metrics or KPIs
    with m_Col1:
        st.header("Temperature 🌡️")
        st.write(round(m_ETo.kelvin_to_celsius(mean_temperature), 2), "℃")

        st.header("Rainfall 🌧️")
        st.write(total_rainfall, "mm")

        st.header("Irrigation water requirement 🚿")
        m_tir = ((m_crw * m_days_count) - total_rainfall) * filed_area
        print("metro total irrigation req: ", m_tir)
        if m_tir < 0:
            water_level = "Excess of "
            m_tir_abs = abs(m_tir)
        else:
            water_level = "Required "
            m_tir_abs = abs(m_tir)
        st.write(water_level, round(m_tir_abs, 3), "Litres")

    with m_Col2:
        st.header("Humidity 🫧")
        st.write(mean_humidity, "%")

        st.header("Wind 💨")
        st.write(mean_wind_speed, "m/s")

    with m_Col3:
        st.header("Sunrise 🌥️")
        st.write(sun_shine)

        st.header("Crop Water Requirement 💦")
        st.write(m_crw, "mm/day")
    # st.write("Average Temperatures:", mean_temperature, "K")
    # st.write("Average Humidity:", mean_humidity, "%")
    # st.write("Rainfalls:", total_rainfall, "mm")

    st.header("Data from Sensors")
    (s_temp, s_humidity, s_light, temp_list, humi_list, s_time, s_pressure, s_wind_speed) = \
        (s_w.real_time_weather(f"{time_diff_irr}d", weather_station))
    # Evapotranspiration from sensor
    s_eto = s_ETo.calculate_s_et0(temp_list, humi_list, s_pressure, mean_wind_speed, s_light, time_diff_irr)
    # Calculate crop water requirement for sensor
    s_crw = round(s_eto * kc, 3)
    print("S_CRW :", s_crw)
    # create three columns to show irrigation related details with sensors data
    s_Col1, s_Col2, s_Col3 = st.columns(3)
    with s_Col1:
        st.header("Temperature 🌡️")
        st.write(s_temp, "℃")

        st.header("Light Intensity ☀")
        st.write(s_light, "lux")

        st.header("Total Evapotranspiration ♨")
        s_tvw = s_crw * filed_area * time_diff_irr
        if s_tvw < 0:
            water_level = "Evapotranspiration of "
            s_tvw_abs = abs(s_tvw)
        else:
            water_level = "Remains of "
            s_tvw_abs = abs(s_tvw)
        st.write(water_level, round(s_tvw_abs, 3), "Litres")

    with s_Col2:
        st.header("Humidity 🫧")
        st.write(s_humidity, "%")

        st.header("Wind 💨")
        st.write(s_wind_speed, "m/s")

    with s_Col3:
        st.header("Sunrise 🌥️")
        st.write(s_light, "lux")

        st.header("Crop Evapotranspiration 🌫")
        st.write(s_crw, "mm/day")

        st.header("Atmospheric pressure 😶‍🌫")
        st.write(s_pressure, "kPa")

else:
    st.write("Location not found or error occurred.")

# Readings from saved metro data
# last_saved_date = wt.last_weather_time(location)  # last saved time of the weather data
# st.write("Last saved date: ", last_saved_date)
# time_diff = datetime.now(pytz.timezone('Asia/Colombo')) - last_saved_date
# if time_diff.hour >= 24:
#     today_summary = wt.get_weather_summary(Latitude, Longitude, api_key)
#     wt.save_weather(today_summary)

# Irrigation Results
st.header("Results")
current_water_level = s_tvw_abs - last_irrigated_amount  # remaining water in litres
print("Current water level: ", current_water_level)


# if m_tir >= 0:
#     water_requirement = m_tir + current_water_level
# else:
#     water_requirement = m_tir - current_water_level
# water_requirement = m_tir + current_water_level  # water requirement for the upcoming days according to the
# # selected days
# print("Required water: ", water_requirement)
# st.header("Total Water Requirement")
# st.write(round(water_requirement, 3), "Litres")

# Convert the remaining time to day hour min
def convert_minutes_to_dhm(minutes):
    if minutes < 0:
        raise ValueError("Input must be a non-negative integer")

    # Calculate days, hours, and minutes
    days = minutes // (24 * 60)
    minutes %= 24 * 60
    hours = minutes // 60
    minutes %= 60

    return days, hours, minutes


if current_water_level <= 0:
    irr_state = '''<span style="color: blue;">You don't need to irrigate</span>'''  # blue text for not to irrigate
    #  estimating the next target irrigation time
    m_crw_list = []
    for i in [1, 2, 3, 4, 5]:
        (mean_temperature, mean_humidity, total_rainfall, mean_wind_speed, sun_shine, sun_shine_time, mean_sea_level,
         u_day,
         u_night, mean_pre_level, m_temperatures, m_humidity, m_wind_speed, m_date_time) \
            = amw.find_avg_weather(avg_weather_data, i)
        # Calculating water requirement
        m_eto = m_ETo.calculate_et0(mean_temperature, mean_humidity, mean_sea_level, sun_shine_time,
                                    mean_wind_speed, Latitude, u_day, u_night)
        # Find crop coefficient factor
        kc = get_crop_coefficient('App\\cropcoefficient.csv')
        # Calculate crop water requirement and append them into list
        # m_crw_list.append(round(m_eto * kc, 3))
        # check day by day
        water_required = (i * filed_area * m_eto * kc) - total_rainfall
        print("water required : ", water_required)
        evaporates_time_in_min = ((60 * 24 * i) / water_required) * current_water_level
        print("time in min:", evaporates_time_in_min)
        if evaporates_time_in_min < 0:
            day, hour, minute = convert_minutes_to_dhm(abs(evaporates_time_in_min))
            st.write("Irrigate after : ", day, "Days", hour, "Hours", round(minute, 0), "Minutes")
            st.write("Require amount of water : ", round(water_required, 3), "Litres")
            break
        # if abs(evaporates_time_in_min) < 1440:
        #     evaporates_time_in_min = abs(evaporates_time_in_min)
        #     break
        # water_to_irr = ((i * a) - total_rainfall)
        # diff = rain_to_irr + water_requirement  # water required amount after the rainfall
        # print("after rainfall :", water_to_irr)
        # if water_to_irr >= 0:
        #     water_state = "Need to irrigate"
        # elif water_to_irr < 0:
        #     water_state = "NO need to irrigate"
        # count the minutes to
        # a = a + 1
elif current_water_level > 0:
    irr_state = '''<span style="color: red;">You need to irrigate</span>'''  # red text for irrigate
    st.write("The shortage amount : ", round(current_water_level, 3), "Litres")
st.markdown(irr_state, unsafe_allow_html=True)
print(s_time)


g_Col1, g_Col2 = st.columns(2)
m_date_and_time = []
for i in m_date_time:
    m_date_and_time.append(convert_datetime(i))

with g_Col2:
    st.header("Metrological")
    # temperature
    chart_data = pd.DataFrame(
        {
            "Temperature in K": m_temperatures,
            "Date": m_date_and_time
        }
    )
    st.line_chart(chart_data, x="Date", y="Temperature in K")
    # humidity
    chart_data = pd.DataFrame(
        {
            "Humidity %": m_humidity,
            "Date": m_date_and_time
        }
    )
    st.line_chart(chart_data, x="Date", y="Humidity %")
with g_Col1:
    st.header("Sensors")
    # temperature
    chart_data = pd.DataFrame(
        {
            "Temperature in C": temp_list,
            "Date": s_time
        }
    )
    st.line_chart(chart_data, x="Date", y="Temperature in C")
    # humidity
    chart_data = pd.DataFrame(
        {
            "Humidity %": humi_list,
            "Date": s_time
        }
    )
    st.line_chart(chart_data, x="Date", y="Humidity %")


# Nutrients readings
# Soil density = 1490 Kg / m3
# average root depth 0.3 m
# Soil weight per m2 = 447 Kg
nitrogen_sensor = 8
phosphorus_sensor = 5
potassium_sensor = 8
nitrogen_recommend, phosphorus_recommend, potassium_recommend = npk.get_crop_npk(plant_type, plantation_days)
nitrogen_decision = npk.nitrogen_decision(nitrogen_recommend, nitrogen_sensor)
phosphorus_decision = npk.nitrogen_decision(phosphorus_recommend, phosphorus_sensor)
potassium_decision = npk.nitrogen_decision(potassium_recommend, potassium_sensor)
st.header("Nutrients")
st.header("NPKs")
st.write("Nitrogen : ", nitrogen_decision)
st.write("Phosphorus : ", phosphorus_decision)
st.write("Potassium : ", potassium_decision)
