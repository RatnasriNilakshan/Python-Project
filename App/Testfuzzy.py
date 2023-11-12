# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
#
# # Create antecedent and consequent objects
# growth_stage = ctrl.Antecedent(np.arange(1, 87, 1), 'growth_stage')
# nitrogen = ctrl.Antecedent(np.arange(0, 101, 1), 'nitrogen')  # inclusive and exclusive
# phosphorus = ctrl.Antecedent(np.arange(0, 101, 1), 'phosphorus')
# potassium = ctrl.Antecedent(np.arange(0, 101, 1), 'potassium')
# npk = ctrl.Consequent(np.arange(0, 101, 1), 'npk')
#
# # Define fuzzy sets for growth stages
# growth_stage['seedling'] = fuzz.trimf(growth_stage.universe, [1, 16, 16])
# growth_stage['vegetative'] = fuzz.trimf(growth_stage.universe, [17, 46, 46])
# growth_stage['flowering'] = fuzz.trimf(growth_stage.universe, [47, 66, 66])
# growth_stage['fruiting'] = fuzz.trimf(growth_stage.universe, [67, 86, 86])
#
# # Define fuzzy sets for nitrogen levels
# nitrogen['low'] = fuzz.trimf(nitrogen.universe, [0, 25, 50])
# nitrogen['medium'] = fuzz.trimf(nitrogen.universe, [25, 50, 75])
# nitrogen['high'] = fuzz.trimf(nitrogen.universe, [50, 75, 100])
#
# # Define fuzzy sets for NPK levels (simplified)
# npk['low'] = fuzz.trimf(npk.universe, [0, 25, 50])
# npk['medium'] = fuzz.trimf(npk.universe, [25, 50, 75])
# npk['high'] = fuzz.trimf(npk.universe, [50, 75, 100])
#
# # Define rules for NPK based on growth stage and nitrogen level
# rule1 = ctrl.Rule(growth_stage['seedling'] & nitrogen['low'], npk['low'])
# rule2 = ctrl.Rule(growth_stage['seedling'] & nitrogen['medium'], npk['medium'])
# rule3 = ctrl.Rule(growth_stage['seedling'] & nitrogen['high'], npk['medium'])
# # Define more rules for other combinations
#
# # Create a control system and simulate it
# npk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])  # Add more rules
# npk_sim = ctrl.ControlSystemSimulation(npk_ctrl)
#
# # Input sensor values (e.g., growth stage and nitrogen level)
# npk_sim.input['growth_stage'] = 10
# npk_sim.input['nitrogen'] = 40
#
# # Compute the NPK level
# npk_sim.compute()
#
# # Access the result
# npk_level = npk_sim.output['npk']
#
# print(f"The recommended NPK level is {npk_level:.2f}")


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
#
# # Define input variables and their linguistic terms for both tomato and chili
# # Days is common for both crops, while other variables are specific to each crop
# days = ctrl.Antecedent(np.arange(1, 107, 1), 'days')
# n_tomato = ctrl.Antecedent(np.arange(0, 70, 1), 'tomato_nitrogen')
# p_tomato = ctrl.Antecedent(np.arange(0, 50, 1), 'tomato_phosphorus')
# k_tomato = ctrl.Antecedent(np.arange(0, 20, 1), 'tomato_potassium')
# n_chili = ctrl.Antecedent(np.arange(0, 126, 1), 'chili_nitrogen')
# p_chili = ctrl.Antecedent(np.arange(0, 31, 1), 'chili_phosphorus')
# k_chili = ctrl.Antecedent(np.arange(0, 53, 1), 'chili_potassium')
#
# # Define output variables and their linguistic terms for both tomato and chili
# yield_tomato = ctrl.Consequent(np.arange(0, 5001, 1), 'tomato_yield')
# yield_chili = ctrl.Consequent(np.arange(0, 5001, 1), 'chili_yield')
#
# # Define membership functions for input variables (customize these based on your data)
# days['early'] = fuzz.trimf(days.universe, [1, 15, 30])
# days['mid'] = fuzz.trimf(days.universe, [20, 60, 90])
# days['late'] = fuzz.trimf(days.universe, [80, 105, 106])
#
# n_tomato['low'] = fuzz.trimf(n_tomato.universe, [0, 20, 40])
# n_tomato['medium'] = fuzz.trimf(n_tomato.universe, [30, 50, 70])
# n_tomato['high'] = fuzz.trimf(n_tomato.universe, [60, 69, 69])
#
# n_chili['low'] = fuzz.trimf(n_chili.universe, [0, 30, 60])
# n_chili['medium'] = fuzz.trimf(n_chili.universe, [50, 80, 110])
# n_chili['high'] = fuzz.trimf(n_chili.universe, [100, 125, 125])
#
# # Define rules for tomato and chili separately
# rule_tomato = ctrl.Rule(days['early'] & n_tomato['high'], yield_tomato['high'])
# rule_chili = ctrl.Rule(days['late'] & n_chili['low'], yield_chili['low'])
#
# # Create the control system for tomato and chili separately
# tomato_ctrl = ctrl.ControlSystem([rule_tomato])
# chili_ctrl = ctrl.ControlSystem([rule_chili])
#
# # Create control system simulations for tomato and chili
# tomato_sim = ctrl.ControlSystemSimulation(tomato_ctrl)
# chili_sim = ctrl.ControlSystemSimulation(chili_ctrl)
#
# # Input values for both tomato and chili (customize these values based on your data)
# tomato_sim.input['days'] = 25
# tomato_sim.input['tomato_nitrogen'] = 60
#
# chili_sim.input['days'] = 85
# chili_sim.input['chili_nitrogen'] = 30
#
# # Compute the output for tomato and chili separately
# tomato_sim.compute()
# chili_sim.compute()
#
# # Extract the output values
# predicted_tomato_yield = tomato_sim.output['tomato_yield']
# predicted_chili_yield = chili_sim.output['chili_yield']
#
# # Print the predicted yields for both crops
# print(f'Predicted Tomato Yield: {predicted_tomato_yield} Kg/ha')
# print(f'Predicted Chili Yield: {predicted_chili_yield} Kg/ha')
#
# # You can also visualize the membership functions for days, nitrogen, and yields
# days.view()
# n_tomato.view()
# n_chili.view()
# yield_tomato.view()
# yield_chili.view()

#
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from sklearn.impute import SimpleImputer
#
# # Load the tomato dataset
# tomato_data = pd.read_excel('tomato.xlsx', engine='openpyxl')
#
# # Split the data into features (X) and target (y)
# X_tomato = tomato_data.drop(columns='TOMATO(Kg/ha)')
# y_tomato = tomato_data['TOMATO(Kg/ha)']
#
# # Split the data into training and testing sets
# X_train_tomato, X_test_tomato, y_train_tomato, y_test_tomato = train_test_split(X_tomato, y_tomato, test_size=0.2,
#                                                                                 random_state=42)
#
# # Train a linear regression model for tomato yield
# model_tomato = LinearRegression()
# model_tomato.fit(X_train_tomato, y_train_tomato)
#
# # Load the chili dataset
# chili_data = pd.read_excel('chilli.xlsx', engine='openpyxl')
#
# # Split the data into features (X) and target (y)
# X_chili = chili_data.drop(columns='CHILLI(Kg/ha)')
# y_chili = chili_data['CHILLI(Kg/ha)']
#
# # Split the data into training and testing sets
# X_train_chili, X_test_chili, y_train_chili, y_test_chili = train_test_split(X_chili, y_chili, test_size=0.2,
#                                                                             random_state=42)
#
# # Train a linear regression model for chili yield
# model_chili = LinearRegression()
# model_chili.fit(X_train_chili, y_train_chili)
#
#
# # Evaluate the models
# def evaluate_model(model, X_test, y_test):
#     y_pred = model.predict(X_test)
#     mae = mean_absolute_error(y_test, y_pred)
#     mse = mean_squared_error(y_test, y_pred)
#     r2 = r2_score(y_test, y_pred)
#     return mae, mse, r2
#
#
# mae_tomato, mse_tomato, r2_tomato = evaluate_model(model_tomato, X_test_tomato, y_test_tomato)
# mae_chili, mse_chili, r2_chili = evaluate_model(model_chili, X_test_chili, y_test_chili)
#
# # Print the evaluation results
# print("Tomato Model Evaluation:")
# print(f"Mean Absolute Error (MAE): {mae_tomato}")
# print(f"Mean Squared Error (MSE): {mse_tomato}")
# print(f"R-squared (R^2): {r2_tomato}\n")
#
# print("Chili Model Evaluation:")
# print(f"Mean Absolute Error (MAE): {mae_chili}")
# print(f"Mean Squared Error (MSE): {mse_chili}")
# print(f"R-squared (R^2): {r2_chili}")


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
#
# # Create input and output variables
# temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
# fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')
#
# # Create membership functions for the input variable (temperature)
# temperature['cool'] = fuzz.trimf(temperature.universe, [0, 0, 50])
# temperature['warm'] = fuzz.trimf(temperature.universe, [0, 50, 100])
# temperature['hot'] = fuzz.trimf(temperature.universe, [50, 100, 100])
#
# # Create membership functions for the output variable (fan_speed)
# fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
# fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [0, 50, 100])
# fan_speed['high'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])
#
# # Create fuzzy rules
# rule1 = ctrl.Rule(temperature['cool'], fan_speed['low'])
# rule2 = ctrl.Rule(temperature['warm'], fan_speed['medium'])
# rule3 = ctrl.Rule(temperature['hot'], fan_speed['high'])
#
# # Create a control system
# fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
#
# # Create a control system simulation
# fan_speed_sim = ctrl.ControlSystemSimulation(fan_speed_ctrl)
#
# # Input the temperature value
# fan_speed_sim.input['temperature'] = 10
#
# # Compute the output
# fan_speed_sim.compute()
#
# # Print the resulting fan speed
# print("Fan Speed:", fan_speed_sim.output['fan_speed'])
#
# # Visualize the membership functions and control surface (optional)
# temperature.view()
# fan_speed.view()
# fan_speed.view(sim=fan_speed_sim)


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
#
# # Create input variables
# nitrogen = ctrl.Antecedent(np.arange(0, 101, 1), 'nitrogen')
# phosphorus = ctrl.Antecedent(np.arange(0, 101, 1), 'phosphorus')
# potassium = ctrl.Antecedent(np.arange(0, 101, 1), 'potassium')
#
# # Create output variable
# recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'recommendation')
#
# # Define membership functions for N, P, and K
# nitrogen['low'] = fuzz.trimf(nitrogen.universe, [0, 0, 50])
# nitrogen['optimal'] = fuzz.trimf(nitrogen.universe, [0, 50, 100])
# nitrogen['high'] = fuzz.trimf(nitrogen.universe, [50, 100, 100])
#
# phosphorus['low'] = fuzz.trimf(phosphorus.universe, [0, 0, 50])
# phosphorus['optimal'] = fuzz.trimf(phosphorus.universe, [0, 50, 100])
# phosphorus['high'] = fuzz.trimf(phosphorus.universe, [50, 100, 100])
#
# potassium['low'] = fuzz.trimf(potassium.universe, [0, 0, 50])
# potassium['optimal'] = fuzz.trimf(potassium.universe, [0, 50, 100])
# potassium['high'] = fuzz.trimf(potassium.universe, [50, 100, 100])
# # Define membership functions for P and K (similar to N)
#
# # Define membership functions for the recommendation
# recommendation['low'] = fuzz.trimf(recommendation.universe, [0, 0, 50])
# recommendation['medium'] = fuzz.trimf(recommendation.universe, [0, 50, 100])
# recommendation['high'] = fuzz.trimf(recommendation.universe, [50, 100, 100])
#
# # Create fuzzy rules
# rule1 = ctrl.Rule(nitrogen['low'] & phosphorus['low'] & potassium['low'], recommendation['low'])
# rule2 = ctrl.Rule(nitrogen['optimal'] & phosphorus['optimal'] & potassium['optimal'], recommendation['medium'])
# rule3 = ctrl.Rule(nitrogen['high'] & phosphorus['high'] & potassium['high'], recommendation['high'])
#
# # Add more rules as needed
#
# # Create a control system
# recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
#
# # Create a control system simulation
# recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)
#
# # Input sensor readings
# recommendation_sim.input['nitrogen'] = 42
# recommendation_sim.input['phosphorus'] = 52
# recommendation_sim.input['potassium'] = 8
# # Calculate the recommendation
# recommendation_sim.compute()
#
# # Access the fuzzy recommendation
# recommendation_output = recommendation_sim.output['recommendation']
# print("Recommendation:", recommendation_output)


# # Sample NPK values from the sensor for each day (replace with your actual data)
# sensor_data = [
#     {"date": "2023-11-01", "N": 50, "P": 20, "K": 30},
#     {"date": "2023-11-02", "N": 45, "P": 25, "K": 28},
#     # Add more days as needed
# ]
#
# # Sample agricultural recommendations for NPK values (replace with your actual recommendations)
# agricultural_recommendations = {
#     "N": {"min": 40, "max": 60},
#     "P": {"min": 15, "max": 30},
#     "K": {"min": 25, "max": 40},
# }
#
# # Threshold for acceptable deviation (adjust as needed)
# threshold = 10  # 10% deviation allowed
#
# # Function to calculate deviation and provide recommendations
# def analyze_npk_values(data):
#     recommendations = []
#     for day in data:
#         deviation = {}
#         for nutrient in ["N", "P", "K"]:
#             recommended_range = agricultural_recommendations[nutrient]
#             sensor_value = day[nutrient]
#             deviation[nutrient] = (sensor_value - recommended_range["min"]) / recommended_range["min"] * 100
#
#         recommendations.append(
#             {
#                 "date": day["date"],
#                 "deviation": deviation,
#                 "recommendation": "Adjust" if any(val > threshold for val in deviation.values()) else "OK"
#             }
#         )
#     return recommendations
#
# # Analyze NPK values and get recommendations
# recommendations = analyze_npk_values(sensor_data)
#
# # Print recommendations
# for recommendation in recommendations:
#     print(f"Date: {recommendation['date']}")
#     print(f"Deviation (NPK): {recommendation['deviation']}")
#     print(f"Recommendation: {recommendation['recommendation']}\n")






# # Sample sensor data for NPK values by day
# sensor_data = [
#     {"day": 1, "N": 50, "P": 30, "K": 40},
#     {"day": 2, "N": 45, "P": 25, "K": 35},
#     {"day": 3, "N": 55, "P": 35, "K": 45},
#     # Add more days as needed
# ]
#
# # Sample recommended NPK values for the same days
# recommended_values = [
#     {"day": 1, "N": 60, "P": 40, "K": 50},
#     {"day": 2, "N": 55, "P": 35, "K": 45},
#     {"day": 3, "N": 65, "P": 45, "K": 55},
#     # Add more days as needed
# ]
#
#
# # Function to calculate deviation and provide recommendations
# def analyze_npk_data(sensor_data, recommended_values):
#     for day_data, recommended_data in zip(sensor_data, recommended_values):
#         day = day_data["day"]
#         deviation_N = day_data["N"] - recommended_data["N"]
#         deviation_P = day_data["P"] - recommended_data["P"]
#         deviation_K = day_data["K"] - recommended_data["K"]
#
#         print(f"Day {day}:")
#         print(f"Deviation (N): {deviation_N}")
#         print(f"Deviation (P): {deviation_P}")
#         print(f"Deviation (K): {deviation_K}")
#
#         # Provide recommendations based on deviations
#         if deviation_N > 0:
#             print("Recommendation: Reduce nitrogen (N) fertilizer.")
#         elif deviation_N < 0:
#             print("Recommendation: Increase nitrogen (N) fertilizer.")
#         if deviation_P > 0:
#             print("Recommendation: Reduce phosphorus (P) fertilizer.")
#         elif deviation_P < 0:
#             print("Recommendation: Increase phosphorus (P) fertilizer.")
#         if deviation_K > 0:
#             print("Recommendation: Reduce potassium (K) fertilizer.")
#         elif deviation_K < 0:
#             print("Recommendation: Increase potassium (K) fertilizer.")
#         print("")
#
#
# # Call the function to analyze the data
# analyze_npk_data(sensor_data, recommended_values)
#
#
#
# import pandas as pd
# from fuzzywuzzy import fuzz
# import os
#
# plant_type = "Tomato"
# day = 12
#
# sensor_npk = 40, 54, 9
#
# print("Current Working Directory:", os.getcwd())
#
#
# def get_recommended_npk(csv_file, day):
#     try:
#         df = pd.read_csv(csv_file, index_col='Days')
#         nitrogen = df.at[day, str("nitrogen")]
#         phosphorus = df.at[day, str("phosphorus")]
#         potassium = df.at[day, str("potassium")]
#         return nitrogen, phosphorus, potassium
#     except FileNotFoundError:
#         print(f"File {csv_file} not found. Please check the file path.")
#
#
# if plant_type == "Tomato":
#     recommended_npk = get_recommended_npk('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python '
#                                           'Project\\App\\tomato_NPK.csv', day)
#     print("Recommended_NPK : ", recommended_npk)
# else:
#     recommended_npk = get_recommended_npk('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python '
#                                           'Project\\App\\chilli_NPK.csv', day)
#     print("Recommended_NPK : ", recommended_npk)
#
#
# similarity = fuzz.ratio(sensor_npk, recommended_npk)
# print("Similarity", similarity)










import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the fuzzy variables
sensor_n = ctrl.Antecedent(np.arange(0, 101, 1), 'Sensor_N')
sensor_p = ctrl.Antecedent(np.arange(0, 101, 1), 'Sensor_P')
sensor_k = ctrl.Antecedent(np.arange(0, 101, 1), 'Sensor_K')
day = ctrl.Antecedent(np.arange(1, 101, 1), 'Day')


n_recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'N_Recommendation')
p_recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'P_Recommendation')
k_recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'K_Recommendation')

# Define membership functions
sensor_n['Low'] = fuzz.trimf(sensor_n.universe, [0, 0, 15])
sensor_n['Medium'] = fuzz.trimf(sensor_n.universe, [10, 15, 20])
sensor_n['High'] = fuzz.trimf(sensor_n.universe, [15, 30, 30])

# Define membership functions for other input variables (sensor_p, sensor_k, day)
# Define membership functions for Sensor P
sensor_p['Low'] = fuzz.trimf(sensor_p.universe, [0, 0, 7])
sensor_p['Medium'] = fuzz.trimf(sensor_p.universe, [5, 8, 11])
sensor_p['High'] = fuzz.trimf(sensor_p.universe, [9, 15, 15])

# Define membership functions for Sensor K
sensor_k['Low'] = fuzz.trimf(sensor_k.universe, [0, 0, 5])
sensor_k['Medium'] = fuzz.trimf(sensor_k.universe, [4, 6, 8])
sensor_k['High'] = fuzz.trimf(sensor_k.universe, [7, 12, 12])

# Define membership functions for Day
day['Early Growth'] = fuzz.trimf(day.universe, [1, 1, 30])
day['Mid-Growth'] = fuzz.trimf(day.universe, [25, 50, 75])
day['Late Growth'] = fuzz.trimf(day.universe, [70, 100, 100])

# Define membership functions for the output variables (n_recommendation, p_recommendation, k_recommendation)
# Define membership functions for N_Recommendation
n_recommendation['Low'] = fuzz.trimf(n_recommendation.universe, [0, 0, 30])
n_recommendation['Medium'] = fuzz.trimf(n_recommendation.universe, [20, 50, 80])
n_recommendation['High'] = fuzz.trimf(n_recommendation.universe, [70, 100, 100])

# Define membership functions for P_Recommendation
p_recommendation['Low'] = fuzz.trimf(p_recommendation.universe, [0, 0, 30])
p_recommendation['Medium'] = fuzz.trimf(p_recommendation.universe, [20, 50, 80])
p_recommendation['High'] = fuzz.trimf(p_recommendation.universe, [70, 100, 100])

# Define membership functions for K_Recommendation
k_recommendation['Low'] = fuzz.trimf(k_recommendation.universe, [0, 0, 30])
k_recommendation['Medium'] = fuzz.trimf(k_recommendation.universe, [20, 50, 80])
k_recommendation['High'] = fuzz.trimf(k_recommendation.universe, [70, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule2 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule3 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule4 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule5 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule6 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule7 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule8 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule9 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule10 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule11 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule12 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule13 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule14 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule15 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule16 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule17 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule18 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule19 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule20 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule21 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule22 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule23 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule24 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule25 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Low'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule26 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Medium'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
rule27 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['High'] & day['Early Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Low'], k_recommendation['Low'])
)
# Rule 28
rule28 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 29
rule29 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 30
rule30 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 31
rule31 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 32
rule32 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 33
rule33 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 34
rule34 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 35
rule35 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 36
rule36 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 37
rule37 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 38
rule38 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 39
rule39 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 40
rule40 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 41
rule41 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 42
rule42 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 43
rule43 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 44
rule44 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 45
rule45 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 46
rule46 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 47
rule47 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 48
rule48 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 49
rule49 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 50
rule50 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 51
rule51 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 52
rule52 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['High'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 53
rule53 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Low'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 54
rule54 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Medium'] & day['Mid-Growth']),
    consequent=(n_recommendation['High'], p_recommendation['Medium'], k_recommendation['Medium'])
)
# Rule 55
rule55 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 56
rule56 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 57
rule57 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Low'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 58
rule58 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 59
rule59 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 60
rule60 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['Medium'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 61
rule61 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 62
rule62 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 63
rule63 = ctrl.Rule(
    antecedent=(sensor_n['Low'] & sensor_p['High'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 64
rule64 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 65
rule65 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 66
rule66 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Low'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 67
rule67 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 68
rule68 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 69
rule69 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['Medium'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 70
rule70 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 71
rule71 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 72
rule72 = ctrl.Rule(
    antecedent=(sensor_n['Medium'] & sensor_p['High'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 73
rule73 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 74
rule74 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 75
rule75 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Low'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 76
rule76 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 77
rule77 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 78
rule78 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['Medium'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 79
rule79 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Low'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 80
rule80 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['Medium'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)

# Rule 81
rule81 = ctrl.Rule(
    antecedent=(sensor_n['High'] & sensor_p['High'] & sensor_k['High'] & day['Late Growth']),
    consequent=(n_recommendation['Medium'], p_recommendation['Medium'], k_recommendation['Medium'])
)


# Define more rules based on your specific requirements

# Create a control system
recommendation_ctrl = ctrl.ControlSystem([rule1])

# Create a simulation
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

# Set input values
recommendation_sim.input['Sensor_N'] = 10
recommendation_sim.input['Sensor_P'] = 8
recommendation_sim.input['Sensor_K'] = 5
recommendation_sim.input['Day'] = 30

# Compute the recommendations
recommendation_sim.compute()

# Get the recommended N, P, and K values
n_recommendation_value = recommendation_sim.output['N_Recommendation']
p_recommendation_value = recommendation_sim.output['P_Recommendation']
k_recommendation_value = recommendation_sim.output['K_Recommendation']

# Print the recommendations
print(f'N Recommendation: {n_recommendation_value:.2f}')
print(f'P Recommendation: {p_recommendation_value:.2f}')
print(f'K Recommendation: {k_recommendation_value:.2f}')




