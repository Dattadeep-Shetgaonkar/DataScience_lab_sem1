import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv(r"C:\Users\shetg\Downloads\Q21_Housing prices regression-20251101T205107Z-1-001\Q21_Housing prices regression\malaysia_house_price_data_2025.csv")
 
# Display first few rows
print("Dataset Head:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Encode categorical variables
le_state = LabelEncoder()
le_tenure = LabelEncoder()
le_type = LabelEncoder()

df['State_encoded'] = le_state.fit_transform(df['State'])
df['Tenure_encoded'] = le_tenure.fit_transform(df['Tenure'])
df['Type_encoded'] = le_type.fit_transform(df['Type'])

# Features and target
features = ['Median_PSF', 'Transactions', 'State_encoded', 'Tenure_encoded', 'Type_encoded']
X = df[features]
y = df['Median_Price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=0.1),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'SVR': SVR(kernel='rbf'),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Polynomial Regression (degree 2)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
models['Polynomial Regression'] = LinearRegression()

# Train and evaluate
results = {}
for name, model in models.items():
    if name == 'Polynomial Regression':
        model.fit(X_train_poly, y_train)
        y_pred = model.predict(X_test_poly)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'MSE': mse, 'R2': r2}
    print(f"{name}: MSE = {mse:.2f}, R2 = {r2:.2f}")

print("\nModel Comparison:")
for name, metrics in results.items():
    print(f"{name}: MSE = {metrics['MSE']:.2f}, R2 = {metrics['R2']:.2f}")
