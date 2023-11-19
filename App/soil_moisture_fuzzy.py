# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
# # import matplotlib.pyplot as plt
#
# # Create Antecedent/Consequent objects representing the linguistic variables
# soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
# recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'recommendation')
#
# # Define membership functions for Soil Moisture
# soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 0, 26])
# soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [0, 26, 60])
# soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 100, 100])
#
# # Define membership functions for Recommendation
# recommendation['water_now'] = fuzz.trimf(recommendation.universe, [0, 0, 40])
# recommendation['monitor'] = fuzz.trimf(recommendation.universe, [0, 40, 89])
# recommendation['do_not_water'] = fuzz.trimf(recommendation.universe, [89, 100, 100])
#
# # Define rules
# rule1 = ctrl.Rule(soil_moisture['low'], recommendation['water_now'])
# rule2 = ctrl.Rule(soil_moisture['medium'], recommendation['monitor'])
# rule3 = ctrl.Rule(soil_moisture['high'], recommendation['do_not_water'])
#
# # Create control system
# recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
#
# # Create simulation
# recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)
#
# # Example usage
# soil_moisture_level = 61  # Replace this with your actual soil moisture reading
# recommendation_sim.input['soil_moisture'] = soil_moisture_level
#
# # Compute the recommendation
# recommendation_sim.compute()
#
# # # Visualize the membership functions
# # soil_moisture.view()
# # recommendation.view()
# #
# # # Show the plot
# # plt.show()
# # Print the result
# print("Soil Moisture Level:", soil_moisture_level)
# print("Recommendation:", recommendation_sim.output['recommendation'])
#
# # You can also visualize the result
# recommendation.view(sim=recommendation_sim)






import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# Create Antecedent/Consequent objects representing the linguistic variables
soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'recommendation')

# Define membership functions for Soil Moisture
soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 0, 26])
soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [0, 26, 60])
soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [26, 60, 100])

# Define membership functions for Recommendation
recommendation['water_now'] = fuzz.trimf(recommendation.universe, [0, 0, 40])
recommendation['monitor'] = fuzz.trimf(recommendation.universe, [0, 40, 89])
recommendation['do_not_water'] = fuzz.trimf(recommendation.universe, [40, 89, 100])

# Define rules
rule1 = ctrl.Rule(soil_moisture['low'], recommendation['water_now'])
rule2 = ctrl.Rule(soil_moisture['medium'], recommendation['monitor'])
rule3 = ctrl.Rule(soil_moisture['high'], recommendation['do_not_water'])

# Create control system
recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Create simulation
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

# Example usage
soil_moisture_level = 30  # Replace this with your actual soil moisture reading
recommendation_sim.input['soil_moisture'] = soil_moisture_level

# Print rule activations for debugging
print("\nRule activations:")

# Rule 1 activation
activation_rule1 = fuzz.interp_membership(soil_moisture.universe, soil_moisture['low'].mf, soil_moisture_level)
print("Rule 1:", activation_rule1)

# Rule 2 activation
activation_rule2 = fuzz.interp_membership(soil_moisture.universe, soil_moisture['medium'].mf, soil_moisture_level)
print("Rule 2:", activation_rule2)

# Rule 3 activation
activation_rule3 = fuzz.interp_membership(soil_moisture.universe, soil_moisture['high'].mf, soil_moisture_level)
print("Rule 3:", activation_rule3)

# ... (remaining code)

# Compute the recommendation
try:
    recommendation_sim.compute()
except AssertionError as e:
    print(f"AssertionError: {e}")
    print("Error occurred during defuzzification. Check membership function shapes and input values.")


# Visualize the membership functions
soil_moisture.view()
recommendation.view()

# Show the plot
plt.show()

# Print intermediate results for debugging
print("\nActivated memberships:")
soil_moisture.view(sim=recommendation_sim)
recommendation.view(sim=recommendation_sim)
# Show the plot
plt.show()
# Print the result
print("\nSoil Moisture Level:", soil_moisture_level)
print("Recommendation:", recommendation_sim.output['recommendation'])

print("\nRule strengths:")
print("Rule 1:", activation_rule1)
print("Rule 2:", activation_rule2)
print("Rule 3:", activation_rule3)

print("\nAggregated result before defuzzification:")
print("Aggregated:", recommendation_sim.output['recommendation'])


