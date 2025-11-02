import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data_path = 'RainPrediction - Sheet1.csv'
df = pd.read_csv(data_path)

# Clean data: remove rows with NaN
df.dropna(inplace=True)

# Preprocessing: Remove outliers using IQR
def remove_outliers_iqr(df, columns):
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

numerical_cols = ['Humidity', 'Temperature', 'Heat Index', 'Atmospheric pressure', 'Altitude']
df = remove_outliers_iqr(df, numerical_cols)

# EDA: Check class distribution of target variable 'Rain'
print("Class distribution in 'Rain' column:")
print(df['Rain'].value_counts())
print("\nClass distribution percentage:")
print(df['Rain'].value_counts(normalize=True))

# Plot class distribution
sns.countplot(x='Rain', data=df)
plt.title('Class Distribution of Rain')
plt.savefig('rain_distribution.png')
plt.close()

# Features and target
X = df.drop('Rain', axis=1)
y = df['Rain']

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into train (60%), temp (40%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X_scaled, y, test_size=0.4, random_state=42, stratify=y)

# Split temp into validation (20%) and test (20%)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print(f"Train set size: {X_train.shape[0]}")
print(f"Validation set size: {X_val.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Define models to train
models = {
    'Logistic Regression (lbfgs)': LogisticRegression(random_state=42, solver='lbfgs'),
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(random_state=42)
}

# Train models and evaluate
results = []

for model_name, model in models.items():
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    val_pred = model.predict(X_val)
    test_pred = model.predict(X_test)

    train_acc = accuracy_score(y_train, train_pred)
    val_acc = accuracy_score(y_val, val_pred)
    test_acc = accuracy_score(y_test, test_pred)

    results.append({
        'model': model_name,
        'train': train_acc,
        'validation': val_acc,
        'test': test_acc
    })

# Create results dataframe
results_df = pd.DataFrame(results)
print("\nModel accuracy results:")
print(results_df)

# Save results to CSV
results_df.to_csv('model_results.csv', index=False)
