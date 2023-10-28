import pandas as pd
import math
from datetime import datetime


# Function to calculate the saturation_vapour_pressure
def saturation_vapour_pressure(temperature):
    e = 0.6108 * math.exp((17.27 * temperature) / (temperature + 237.3))
    return e


# Temperature Unit conversion
def celsius_to_kelvin(celsius):
    kelvin = celsius + 273.15
    return kelvin


def calculate_s_et0(temperature, humidity, atmospheric_pressure, wind_speed, light_intensity, days):
    # Unit conversion

    # temperature array
    temp_int = temperature[0]
    temp_last = temperature[-1]
    temp_min = min(temperature)
    temp_max = max(temperature)
    temp_mean = sum(temperature) / len(temperature)
    print("temperatures :", temp_int, temp_last, temp_min, temp_max, temp_mean)

    # humidity array
    humidity_min = min(humidity)
    humidity_max = max(humidity)

    # slope of saturation vapour pressure in kPa `C^-1
    delta = (4098 * (0.6108 * math.exp((17.27 * temp_mean) / (temp_mean + 237.3)))
             / (temp_mean + 237.3) ** 2)
    print("delta : ", delta)

    # net radiation at crop surface
    rn_wm = light_intensity * 0.0084  # in watts per meter square
    print("light : ", light_intensity, rn_wm)
    rn = rn_wm * (86400 / 1000000)  # net radiation in MJ m^-2 day^-1
    print("net radiation in MJ: ", rn)

    # Soil heat flux density
    cs = 2.15  # soil heat capacity
    delta_z: float = 0.2  # effective soil depth in meters
    delta_t = days

    # soil heat flux density
    g = cs * ((temp_last + temp_int) / delta_t) * delta_z
    print("soil heat flux density : ", g)

    # Psychometric constant
    lamda = 2.45  # latent heat of vaporization [MJkg^-1]
    cp = 0.001013  # Specific heat at constant pressure [MJkg^-1`C^-1]
    epsilon = 0.622  # ratio molecular weight of water vapour/day air

    gamma = (cp * atmospheric_pressure/10) / (epsilon * lamda)
    print("pressure :", atmospheric_pressure)
    print("gamma : ", gamma)

    # saturation vapour pressure
    e_t_min = saturation_vapour_pressure(temp_min)
    e_t_max = saturation_vapour_pressure(temp_max)
    print("e_t_max : ", e_t_max)
    print("e_t_min : ", e_t_min)

    es = (e_t_max + e_t_min) / 2
    ea = ((e_t_min * (humidity_max / 100)) + (e_t_max * (humidity_min / 100))) / 2
    print("es :", es)
    print("ea :", ea)

    # Calculate reference evapotranspiration (ET0)
    et0 = (0.408 * delta * (rn - g) + gamma * (900 / temp_mean) * wind_speed * (es - ea)) / (
            delta + gamma * (1 + 0.34 * wind_speed))
    et0 = round(et0, 2)

    # Adjust ET0 for vegetation height

    return et0
