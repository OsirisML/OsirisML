import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

print("Loading CSV File...")
df = pd.read_csv('labeled_dataset.csv')
print("CSV LOADED")

# The last column is the label
X = df.iloc[:, 1:-1].values
y = df.iloc[:, -1].values
print("X and Y set")

# Need to encode labels to integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print("Y is encoded")

# Split dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Print the first 5 and last 5 rows of each array
print("\nX_train first 5 lines:")
print(X_train[:5])
print("\nX_train last 5 lines:")
print(X_train[-5:])

print("\nX_test first 5 lines:")
print(X_test[:5])
print("\nX_test last 5 lines:")
print(X_test[-5:])

print("\ny_train first 5 lines:")
print(y_train[:5])
print("\ny_train last 5 lines:")
print(y_train[-5:])

print("\ny_test first 5 lines:")
print(y_test[:5])
print("\ny_test last 5 lines:")
print(y_test[-5:])
