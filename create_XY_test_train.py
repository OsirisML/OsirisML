import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the CSV file
print("Loading CSV File...")
df = pd.read_csv('labeled_dataset.csv')
print("CSV LOADED")

# Extract features (X) and labels (y)
X = df.iloc[:, 1:-1].values
y = df.iloc[:, -1].values
print("X and Y set")

# Encode labels to integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print("Y is encoded")

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Print the shapes of the datasets
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

# Print the first 5 and last 5 lines of X_train
print("X_train first 5 lines:")
print(X_train.head())
print("\nX_train last 5 lines:")
print(X_train.tail())

# Print the first 5 and last 5 lines of X_test
print("\nX_test first 5 lines:")
print(X_test.head())
print("\nX_test last 5 lines:")
print(X_test.tail())

# Print the first 5 and last 5 lines of y_train
print("\ny_train first 5 lines:")
print(y_train[:5])
print("\ny_train last 5 lines:")
print(y_train[-5:])

# Print the first 5 and last 5 lines of y_test
print("\ny_test first 5 lines:")
print(y_test[:5])
print("\ny_test last 5 lines:")
print(y_test[-5:])
