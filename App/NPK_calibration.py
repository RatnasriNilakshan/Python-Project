import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress, skew, kurtosis
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Replace 'your_data.csv' with the path to your dataset
df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\npk_calibration.csv')

# Phosphorus calibration
p_sensor = df['P_sensor'].values
p_aoac = df['P_aoac'].values
slope, intercept, r_value, p_value, std_err = linregress(p_aoac, p_sensor)

# Polynomial Regression
degree = 4  # Change the degree as needed
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(p_aoac.reshape(-1, 1))

model = LinearRegression()
model.fit(X_poly, p_sensor)

# Plotting
plt.scatter(p_aoac, p_sensor, label='Data')

# # Linear Regression line
# plt.plot(humidity_probe, intercept + slope * humidity_probe, color='blue', label='Linear Regression Fit')

# # Polynomial Regression line
# plt.plot(humidity_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')

# Plot the polynomial regression line through midpoints
high_res_humidity = np.linspace(min(p_aoac), max(p_aoac), 1000).reshape(-1, 1)
high_res_X_poly = poly.transform(high_res_humidity)
high_res_poly_fit = model.predict(high_res_X_poly)
plt.plot(high_res_humidity, high_res_poly_fit, color='blue', label=f'Polynomial Regression Fit (degree={degree})')


# Calculate errors for the linear regression
linear_errors = std_err * np.ones_like(p_aoac)

# # Calculate errors for the polynomial regression
poly_errors = np.std(p_aoac - model.predict(X_poly))

# Plot error bars
# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
# plt.errorbar(humidity_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', label='Polynomial Regression Error')

# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='lightblue', capsize=3, label='Linear Regression Error')
plt.errorbar(p_aoac, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', capsize=3, label='Polynomial Regression Error')

plt.xlabel('Phosphorus AOAC (mg/Kg)')
plt.ylabel('Phosphorus Sensor (mg/Kg)')
plt.title('Phosphorus Calibration')
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
print("  R-squared:", model.score(X_poly, p_sensor))
print("  Standard Error:", poly_errors)

# Calculate skewness and kurtosis
skewness = skew(p_sensor)
kurt = kurtosis(p_sensor)

# Output results
print("Skewness:", skewness)
print("Kurtosis:", kurt)

# Potassium Calibration
k_sensor = df['K_sensor'].values
k_aoac = df['K_aoac'].values
slope, intercept, r_value, p_value, std_err = linregress(k_aoac, k_sensor)

# Polynomial Regression
degree = 4  # Change the degree as needed
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(k_aoac.reshape(-1, 1))

model = LinearRegression()
model.fit(X_poly, k_sensor)

# Plotting
plt.scatter(k_aoac, k_sensor, label='Data')

# # Linear Regression line
# plt.plot(humidity_probe, intercept + slope * humidity_probe, color='blue', label='Linear Regression Fit')

# # Polynomial Regression line
# plt.plot(humidity_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')

# Plot the polynomial regression line through midpoints
high_res_humidity = np.linspace(min(k_aoac), max(k_aoac), 1000).reshape(-1, 1)
high_res_X_poly = poly.transform(high_res_humidity)
high_res_poly_fit = model.predict(high_res_X_poly)
plt.plot(high_res_humidity, high_res_poly_fit, color='blue', label=f'Polynomial Regression Fit (degree={degree})')


# Calculate errors for the linear regression
linear_errors = std_err * np.ones_like(k_aoac)

# # Calculate errors for the polynomial regression
poly_errors = np.std(k_aoac - model.predict(X_poly))

# Plot error bars
# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
# plt.errorbar(humidity_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', label='Polynomial Regression Error')

# plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='lightblue', capsize=3, label='Linear Regression Error')
plt.errorbar(k_aoac, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', capsize=3, label='Polynomial Regression Error')

plt.xlabel('Potassium AOAC (mg/Kg)')
plt.ylabel('Potassium Sensor (mg/Kg)')
plt.title('Potassium Calibration')
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
print("  R-squared:", model.score(X_poly, k_sensor))
print("  Standard Error:", poly_errors)

# Calculate skewness and kurtosis
skewness = skew(k_sensor)
kurt = kurtosis(k_sensor)

# Output results
print("Skewness:", skewness)
print("Kurtosis:", kurt)

# # Nitrogen Calibration
# n_sensor = df['N_sensor'].values[-2:]
# n_aoac = df['N_aoac'].values[-2:]
# slope, intercept, r_value, p_value, std_err = linregress(n_aoac, n_sensor)
#
# # Polynomial Regression
# degree = 4  # Change the degree as needed
# poly = PolynomialFeatures(degree=degree)
# X_poly = poly.fit_transform(n_aoac.reshape(-1, 1))
#
# model = LinearRegression()
# model.fit(X_poly, n_sensor)
#
# # Plotting
# plt.scatter(n_aoac, n_sensor, label='Data')
#
# # # Linear Regression line
# # plt.plot(humidity_probe, intercept + slope * humidity_probe, color='blue', label='Linear Regression Fit')
#
# # # Polynomial Regression line
# # plt.plot(humidity_probe, model.predict(X_poly), color='red', label=f'Polynomial Regression Fit (degree={degree})')
#
# # Plot the polynomial regression line through midpoints
# high_res_humidity = np.linspace(min(n_aoac), max(n_aoac), 1000).reshape(-1, 1)
# high_res_X_poly = poly.transform(high_res_humidity)
# high_res_poly_fit = model.predict(high_res_X_poly)
# plt.plot(high_res_humidity, high_res_poly_fit, color='blue', label=f'Polynomial Regression Fit (degree={degree})')
#
#
# # Calculate errors for the linear regression
# linear_errors = std_err * np.ones_like(n_aoac)
#
# # # Calculate errors for the polynomial regression
# poly_errors = np.std(n_aoac - model.predict(X_poly))
#
# # Plot error bars
# # plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='red', label='Linear Regression Error')
# # plt.errorbar(humidity_probe, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', label='Polynomial Regression Error')
#
# # plt.errorbar(humidity_probe, humidity_sensor, yerr=linear_errors, fmt='none', color='blue', ecolor='lightblue', capsize=3, label='Linear Regression Error')
# plt.errorbar(n_aoac, model.predict(X_poly), yerr=poly_errors, fmt='none', color='red', ecolor='mistyrose', capsize=3, label='Polynomial Regression Error')
#
# plt.xlabel('Nitrogen AOAC (mg/Kg)')
# plt.ylabel('Nitrogen Sensor (mg/Kg)')
# plt.title('Nitrogen Calibration')
# plt.legend()
# plt.show()
#
# # Output results
# print("Linear Regression:")
# print("  Slope:", slope)
# print("  Intercept:", intercept)
# print("  R-squared:", r_value**2)
# print("  Standard Error:", std_err)
#
# print("\nPolynomial Regression (degree={}):".format(degree))
# print("  Coefficients:", model.coef_)
# print("  Intercept:", model.intercept_)
# print("  R-squared:", model.score(X_poly, n_sensor))
# print("  Standard Error:", poly_errors)