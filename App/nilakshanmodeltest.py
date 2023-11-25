import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the tomato dataset
tomato_data = pd.read_excel('tomato.xlsx', engine='openpyxl')

# Split the data into features (X) and target (y)
X_tomato = tomato_data.drop(columns='Tomato(Kg/ha)')
y_tomato = tomato_data['Tomato(Kg/ha)']

# Split the data into training and testing sets
X_train_tomato, X_test_tomato, y_train_tomato, y_test_tomato = train_test_split(X_tomato, y_tomato, test_size=0.2, random_state=42)

# Train a linear regression model for tomato yield
model_tomato = LinearRegression()
model_tomato.fit(X_train_tomato, y_train_tomato)

# Load the chili dataset
chili_data = pd.read_excel('chilli.xlsx', engine='openpyxl')

# Split the data into features (X) and target (y)
X_chili = chili_data.drop(columns='CHILLI(Kg/ha)')
y_chili = chili_data['CHILLI(Kg/ha)']

# Split the data into training and testing sets
X_train_chili, X_test_chili, y_train_chili, y_test_chili = train_test_split(X_chili, y_chili, test_size=0.2, random_state=42)

# Train a linear regression model for chili yield
model_chili = LinearRegression()
model_chili.fit(X_train_chili, y_train_chili)

# Evaluate the models
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mae, mse, r2

mae_tomato, mse_tomato, r2_tomato = evaluate_model(model_tomato, X_test_tomato, y_test_tomato)
mae_chili, mse_chili, r2_chili = evaluate_model(model_chili, X_test_chili, y_test_chili)

# Print the evaluation results
print("Tomato Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae_tomato}")
print(f"Mean Squared Error (MSE): {mse_tomato}")
print(f"R-squared (R^2): {r2_tomato}\n")

print("Chili Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae_chili}")
print(f"Mean Squared Error (MSE): {mse_chili}")
print(f"R-squared (R^2): {r2_chili}")
