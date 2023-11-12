
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, skew, kurtosis
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\pressure_calibration.csv')
actual_pressure = df["Pressure"].values
sensor_reading = df["Sensor"].values

# Linear Regression
slope, intercept, r_value, p_value, std_err = linregress(actual_pressure, sensor_reading)

# Polynomial Regression
degree = 1  # Change the degree as needed
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(actual_pressure.reshape(-1, 1))

model = LinearRegression()
model.fit(X_poly, sensor_reading)

# Plotting
plt.scatter(actual_pressure, sensor_reading, label='Data')

# # Linear Regression line
plt.plot(actual_pressure, intercept + slope * actual_pressure, color='blue', label='Linear Regression Fit')

# # Polynomial Regression line
# plt.plot(humidity_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')

# Plot the polynomial regression line through midpoints
# high_res_humidity = np.linspace(min(actual_pressure), max(actual_pressure), 1000).reshape(-1, 1)
# high_res_X_poly = poly.transform(high_res_humidity)
# high_res_poly_fit = model.predict(high_res_X_poly)
# plt.plot(high_res_humidity, high_res_poly_fit, color='blue', label=f'Polynomial Regression Fit (degree={degree})')


# Calculate errors for the linear regression
linear_errors = std_err * np.ones_like(actual_pressure)

# # Calculate errors for the polynomial regression
poly_errors = np.std(actual_pressure - model.predict(X_poly))

# Plot error bars
# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
# plt.errorbar(humidity_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', label='Polynomial Regression Error')

# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='lightblue', capsize=3, label='Linear Regression Error')
plt.errorbar(actual_pressure, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', capsize=3, label='Polynomial Regression Error')

plt.xlabel('Actual Pressure (Pa)')
plt.ylabel('Sensor Reading (Pa)')
plt.title('Pressure Calibration')
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
print("  R-squared:", model.score(X_poly, sensor_reading))
print("  Standard Error:", poly_errors)


# Calculate skewness and kurtosis
skewness = skew(sensor_reading)
kurt = kurtosis(sensor_reading)

# Output results
print("Skewness:", skewness)
print("Kurtosis:", kurt)
