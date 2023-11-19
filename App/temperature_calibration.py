import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, skew, kurtosis
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\temp_humi_calibration.csv')
temp_sensor = df['temperature_sensor'].values
temp_probe = df['temperature_probe'].values

# Linear Regression
slope, intercept, r_value, p_value, std_err = linregress(temp_probe, temp_sensor)

# Polynomial Regression
degree = 1  # Change the degree as needed
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(temp_probe.reshape(-1, 1))

model = LinearRegression()
model.fit(X_poly, temp_sensor)

# Plotting
plt.scatter(temp_probe, temp_sensor, label='Data')

# Linear Regression line
plt.plot(temp_probe, intercept + slope * temp_probe, color='blue', label='Linear Regression Fit')

# Polynomial Regression line
# plt.plot(temp_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')

# Calculate errors for the linear regression
linear_errors = std_err * np.ones_like(temp_probe)

# Calculate errors for the polynomial regression
poly_errors = np.std(temp_sensor - model.predict(X_poly))

# Plot error bars
# plt.errorbar(temp_probe, temp_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
plt.errorbar(temp_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose',capsize=2, label='Polynomial Regression Error')

plt.xlabel('Actual Temperature (°C)')
plt.ylabel('Temperature Reading in Sensor (°C)')
plt.title('Temperature Calibration')
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
print("  R-squared:", model.score(X_poly, temp_sensor))
print("  Standard Error:", poly_errors)


# Calculate skewness and kurtosis
skewness = skew(temp_sensor)
kurt = kurtosis(temp_sensor)

# Output results
print("Skewness:", skewness)
print("Kurtosis:", kurt)