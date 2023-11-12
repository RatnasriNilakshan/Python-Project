# import numpy as np  # linear algebra
# import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
# import missingno as msno
# from sklearn.datasets import load_iris
# from sklearn import metrics
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.impute import KNNImputer
# import warnings
# data = pd.read_csv("G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\chilli_knn_npk.csv")
# print(data.head())
# print(data.shape)
# print(data.info())
#
# warnings.filterwarnings("ignore")
# p = sns.pairplot(data, hue='N')
# warnings.filterwarnings("default")
# msno.matrix(data)
# print("Summation of NAN values :")
# data.isnull().sum()
# msno.matrix(data)
#
# data_knn = data.copy(deep=True)
# data_knn.head()
#
# knn_imputer = KNNImputer(n_neighbors=4, weights="uniform")
# data_knn[["N", "P", "K"]] = knn_imputer.fit_transform(data_knn[["N", "P", "K"]])
# print(data_knn.info())
# print(data_knn.head(106))

# import numpy as np
# import pandas as pd
# from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt
#
# df = pd.read_csv("G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\anemometer_calibration.csv")
# # Sample data (replace with your actual data)
# anemo_reading = np.array(df["Anemo"].tolist())
# volts = np.array(df["Vpp"].tolist())
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

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
#
# # Replace 'your_data.csv' with the path to your dataset
# df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\anemometer_calibration.csv')
# Anemo_meter = df['Anemo'].values
# volts = df['Vpp'].values
#
# X = volts.reshape(-1, 1)
# y = Anemo_meter
#
# degree = 2  # You can change this to the desired degree
# poly = PolynomialFeatures(degree=degree)
# X_poly = poly.fit_transform(X)
#
# model = LinearRegression()
# model.fit(X_poly, y)
#
# plt.scatter(X, y, label='Data')
# plt.plot(X, model.predict(X_poly), color='red', label='Polynomial Regression')
# plt.xlabel('Volts')
# plt.ylabel('Anemo-meter Reading')
# plt.legend()
# plt.show()
#
# new_volt_reading = 320.5  # Replace with your sensor reading
# new_volt_poly = poly.transform(np.array([[new_volt_reading]]))
# calibrated_speed = model.predict(new_volt_poly)
# print(f"Calibrated Wind Speed: {calibrated_speed[0]}")


from itertools import product

# Define the membership levels for each sensor
membership_levels = {
    'sensor_n': ['Low', 'Medium', 'High'],
    'sensor_p': ['Low', 'Medium', 'High'],
    'sensor_k': ['Low', 'Medium', 'High'],
}

# Create a list of all possible combinations
combinations = list(product(*membership_levels.values()))

# Print the combinations
for combination in combinations:
    print(combination)
