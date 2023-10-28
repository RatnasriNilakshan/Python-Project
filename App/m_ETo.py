import pandas as pd
import math
from datetime import datetime


# Unit conversions
# Feet to meter conversion
def feet_to_meters(feet):
    meters = feet * 0.3048
    return meters


# Temperature Unit conversion
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius


# Rounding the altitude values according to the table
def get_nearest_altitude(number):
    if number < 1000:
        return round(number / 500) * 500
    if number >= 1000:
        return round(number / 1000) * 1000


# Rounding the temp values according to the table
def get_nearest_temperature(number, interval):
    return round(number / interval) * interval


# Function to get the weighting factor from the altitude vs temp table
def get_weighting_factor(csv_file, temperature, altitude):
    df = pd.read_csv(csv_file, index_col='Altitude')
    altitude = get_nearest_altitude(altitude)
    temperature = get_nearest_temperature(temperature, 2)
    return df.at[altitude, str(temperature)]


# Rounding the temp values according to the saturation_vapour_pressure table
def get_nearest_temperature_ea(number):
    return round(number)


# get the saturation vapour pressure
def get_saturation_vapour_pressure(csv_file, temperature):
    df = pd.read_csv(csv_file, index_col='Temperature')
    temperature = get_nearest_temperature_ea(temperature)
    return df.at[temperature, str('ea')]


def get_current_month():
    # Get the current date
    current_date = datetime.now()
    # Extract and return the month from the current date
    return current_date.month


# Rounding the latitude values according to the sunshine hours table
def get_nearest_latitude(number):
    if number < 40:
        return round(number / 5) * 5
    if number >= 40:
        return round(number / 2) * 2


# Function to get the weighting factor from the altitude vs temp table
def get_max_sunshine(csv_file, latitude):
    df = pd.read_csv(csv_file, index_col='Latitude')
    latitude = get_nearest_latitude(latitude)
    month = get_current_month()
    return df.at[latitude, str(month)]


# Rounding the latitude values according to the Extra terrestrial radiation table
def get_nearest_latitude_ra(number):
    return round(number / 2) * 2


# Function to get the weighting factor from the altitude vs temp table
def get_extra_terrestrial_radiation(csv_file, latitude):
    df = pd.read_csv(csv_file, index_col='Latitude')
    latitude = get_nearest_latitude_ra(latitude)
    month = get_current_month()
    return df.at[latitude, str(month)]


# Rounding the latitude values according to the effect of temperature on long wave radiation
def get_nearest_temperature_ft(number):
    return round(number / 2) * 2


# Function to get the temperature effect from the  effect of temperature on long wave radiation
def get_effect_of_temp_on_radiation(csv_file, temperature):
    df = pd.read_csv(csv_file, index_col='Temperature')
    temperature = get_nearest_temperature_ft(temperature)
    return df.at[temperature, str('F(T)')]


# Rounding the vapour pressure values according to the effect of vapour pressure on long wave radiation
def get_nearest_ed(number):
    return round(number / 2) * 2


# Function to get the effect of vapour pressure from the effect of vapour pressure on long wave radiation
def get_effect_of_vapour_pressure_on_radiation(csv_file, ed):
    df = pd.read_csv(csv_file, index_col='ed')
    ed = get_nearest_ed(ed)
    return df.at[ed, str('f(ed)')]


# Rounding the n/N ratio values according to the effect of n/N on long wave radiation
def get_nearest_n_n_ratio(number):
    return round(number / 0.05) * 0.05


# Function to get the  n/N ratio value from the effect of n/N on long wave radiation
def get_effect_of_sunshine_ratio_on_radiation(csv_file, n_n):
    df = pd.read_csv(csv_file, index_col='n/N')
    n_n = get_nearest_n_n_ratio(n_n)
    return df.at[n_n, str('f(n/N)')]


# Rounding values for the adjustment factor
def get_nearest_rs(number):
    return round(number / 3) * 3


def get_nearest_rh(number):
    return round(number / 30) * 30


def get_nearest_u(number):
    return round(number / 1) * 1


def get_nearest_uday(number):
    return round(number / 3) * 3


# Function to get the adjustment factor
def get_adjustment_factor(csv_file, rs, rh_max, u_day, u_night):
    df = pd.read_csv(csv_file, index_col='Rs mm/day')
    rs = get_nearest_rs(rs)
    rh_mean = get_nearest_rh(rh_max)
    u_ratio = u_day / u_night
    u_ratio = get_nearest_u(u_ratio)
    u_day = get_nearest_uday(u_day)
    return df.at[str(u_day) + ',' + str(u_ratio), str(rs) + ',' + str(rh_mean)]


def calculate_et0(temp_mean, hum_mean, sea_level, shine_time, wind_speed, latitude, u_day, u_night):
    # eto = eto.calculate_Et0(mean_temperature, mean_humidity, mean_sea_level, sun_shine_time,
    #                         mean_wind_speed, Latitude, u_day, u_night)
    # Unit conversion
    temp_mean = kelvin_to_celsius(temp_mean)
    # Altitude calculation
    altitude_temp = 145366 * (1 - (sea_level / 1013.25) ** 0.190284)
    altitude_temp_meter = feet_to_meters(altitude_temp)
    altitude = round(altitude_temp_meter, 3)

    # saturation vapour pressure
    ea = get_saturation_vapour_pressure('App\\saturation_vapour_pressure.csv', temp_mean)

    # Calculate saturation vapor pressure (ed)
    ed = ea * hum_mean / 100

    #  Weighting Factor for the effect of radiation on ET0
    w = get_weighting_factor('App\\temp_vs_altitude.csv', temp_mean, altitude)

    # sun shine mean
    n = shine_time / 3600
    n_max = get_max_sunshine('App\\sunshine_hours.csv', latitude)
    n_n = n / n_max
    # print(n, n_max, n_n)
    fn_n = get_effect_of_sunshine_ratio_on_radiation('App\\sunshine_ratio_on_longwave_radiation.csv', n_n)
    ra = get_extra_terrestrial_radiation('App\\extra_terrestrial_radiation.csv', latitude)
    rs = (0.25 + (0.50 * n / n_max)) * ra
    rns = (1 - 0.25) * rs

    ft = get_effect_of_temp_on_radiation('App\\temperature_on_longwave_radiation.csv', temp_mean)
    fed = get_effect_of_vapour_pressure_on_radiation('App\\vapour_pressure_on_longwave_radiation.csv', ed)

    rnl = ft * fed * fn_n
    rn = rns - rnl
    # print ("rn : ", rn)

    # Calculate wind speed at 2 meters (u2)
    u2_numerator = 4.87
    u2_denominator = 67.8 * altitude - 5.42

    # Check if the denominator is positive to avoid taking the logarithm of a non-positive value
    if u2_denominator > 0:
        wind_speed_2m = wind_speed * (u2_numerator / math.log(u2_denominator))
    else:
        wind_speed_2m = 0
    # Wind related function
    fun_u = wind_speed_2m * 86.4
    wind_fun = 0.27 * (1 + fun_u / 100)

    c = get_adjustment_factor('App\\adjustment_factor.csv', rs, hum_mean, u_day, u_night)

    # Calculate reference evapotranspiration (ET0)
    et0 = c * (w * rn + (1 - w) * wind_fun * (ea - ed))
    et0 = round(et0, 2)

    # Adjust ET0 for vegetation height

    return et0
