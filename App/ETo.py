def calculate_evapotranspiration(temperature, humidity, wind_speed, solar_radiation, elevation, vegetation_height):
    # Constants
    specific_heat_air = 0.001013  # kJ/kg·°C
    psychrometric_constant = 0.067  # kPa/°C

    # Wind related function
    U = wind_speed
    wind_fun = 0.27*(1+U/100)

    # Calculate saturation vapor pressure (ed)
    ed = ea * humidity / 100

    # Calculate actual vapor pressure (ea)
    vapor_pressure = humidity * saturation_vapor_pressure / 100


    # Calculate net radiation (Rn)
    net_radiation = (1 - albedo) * solar_radiation - emissivity * stefan_boltzmann * pow(temperature, 4)

    # Calculate wind speed at 2 meters (u2)
    wind_speed_2m = wind_speed * (4.87 / math.log((67.8 * elevation) - 5.42))

    # Calculate reference evapotranspiration (ET0)
    et0 = c * [W * Rn + (1 - W) * wind_fun * (ea - ed)]

    # Adjust ET0 for vegetation height

    return et0

def feet_to_meters(feet):
    meters = feet * 0.3048
    return meters

P = 952.0
P_0 = 1006.0
# Altitude = (10 ** (math.log(P/P_0)/5.2558797)-1.0/(-6.8755856 * 10.0 ** (-6.0)))
Altitude = 145366*(1-(P/1013.25)**0.190284)
print(Altitude)
print(feet_to_meters(Altitude))