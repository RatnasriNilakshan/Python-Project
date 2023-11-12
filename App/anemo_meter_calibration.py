import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import linregress, skew, kurtosis
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

df = pd.read_csv("G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\anemometer_calibration.csv")
# # Sample data (replace with your actual data)
# anemo_reading = np.array(df["Anemo_meter"].tolist())
# volts = np.array(df["SD"].tolist())
#
#
# # Define a linear calibration function (you may need a different model)
# def windspeed_calibration(x, a, b, c):
#     return a * x**2 + b * x + c
#
#
# # Fit the calibration curve to the data
# params, covariance = curve_fit(windspeed_calibration, volts, anemo_reading)
#
# # Extract the calibration parameters
# a, b, c = params
# print (a,b,c)
# # Visualize the calibration
# plt.scatter(volts, anemo_reading, label='Data')
# plt.plot(volts, windspeed_calibration(volts, a, b, c), color='red', label='Calibration Curve')
# plt.xlabel('Volts')
# plt.ylabel('Anemo-meter Reading')
# plt.legend()
# plt.show()
#
# # Use the calibration parameters to convert a new sensor reading to actual pressure
# new_volt_reading = 320.5  # Replace with your sensor reading
# calibrated_speed = windspeed_calibration(new_volt_reading, a, b, c)
# print(f"Calibrated Wind Speed: {calibrated_speed}")


milli_volts = df['Max'].values
Anemo_meter = df['Anemo_meter'].values


slope, intercept, r_value, p_value, std_err = linregress(Anemo_meter, milli_volts)

# Polynomial Regression
degree = 3  # Change the degree as needed
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(Anemo_meter.reshape(-1, 1))

model = LinearRegression()
model.fit(X_poly, milli_volts)

# Plotting
plt.scatter(Anemo_meter, milli_volts, label='Data')

# # Linear Regression line
# plt.plot(humidity_probe, intercept + slope * humidity_probe, color='blue', label='Linear Regression Fit')

# # Polynomial Regression line
# plt.plot(humidity_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')

# Plot the polynomial regression line through midpoints
high_res_humidity = np.linspace(min(Anemo_meter), max(Anemo_meter), 1000).reshape(-1, 1)
high_res_X_poly = poly.transform(high_res_humidity)
high_res_poly_fit = model.predict(high_res_X_poly)
plt.plot(high_res_humidity, high_res_poly_fit, color='blue', label=f'Polynomial Regression Fit (degree={degree})')


# Calculate errors for the linear regression
linear_errors = std_err * np.ones_like(Anemo_meter)

# # Calculate errors for the polynomial regression
poly_errors = np.std(Anemo_meter - model.predict(X_poly))

# Plot error bars
# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
# plt.errorbar(humidity_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', label='Polynomial Regression Error')

# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='lightblue', capsize=3, label='Linear Regression Error')
plt.errorbar(Anemo_meter, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', capsize=3, label='Polynomial Regression Error')

plt.xlabel('Anemometer (m/s)')
plt.ylabel('Generated volt (mV)')
plt.title('Anemometer Calibration')
plt.legend()
plt.show()

# Output results
print("Linear Regression:")
print("  Slope:", slope)
print("  Intercept:", intercept)
print("  R-squared:", r_value**2)
print("  Standard Error:", std_err)

print("\nPolynomial Regression (degree={}):".format(degree))
print("  Coefficients:", model.coef_)
print("  Intercept:", model.intercept_)
print("  R-squared:", model.score(X_poly, milli_volts))
print("  Standard Error:", poly_errors)

# Calculate skewness and kurtosis
skewness = skew(milli_volts)
kurt = kurtosis(milli_volts)

# Output results
print("Skewness:", skewness)
print("Kurtosis:", kurt)

# print(Anemo_meter)
# print(milli_volts)
# X = milli_volts.reshape(-1, 1)
# y = Anemo_meter
#
# degree = 1  # You can change this to the desired degree
# poly = PolynomialFeatures(degree=degree)
# X_poly = poly.fit_transform(X)
#
# model = LinearRegression()
# model.fit(X_poly, y)
#
# # Get the coefficients (slope and intercept) of the linear regression model
# slope = model.coef_[0]  # Slope
# intercept = model.intercept_  # Intercept
#
# print(f"Slope: {slope}")
# print(f"Intercept: {intercept}")
#
# plt.scatter(X, y, label='Data')
# plt.plot(X, model.predict(X_poly), color='red', label='Polynomial Regression')
# plt.xlabel('Volts Reading')
# plt.ylabel('Anemometer Reading')
# plt.title('Anemometer')
# plt.legend()
# plt.show()
#
# new_anemo_reading = 110.83  # Replace with your sensor reading
# new_anemo_poly = poly.transform(np.array([[new_anemo_reading]]))
# calibrated_anemo = model.predict(new_anemo_poly)
# print(new_anemo_poly-calibrated_anemo)
# print(f"Calibrated winds-peed: {calibrated_anemo[0]}")
