import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
print(f"Loading csv")
df = pd.read_csv('labeled_dataset.csv')
print(f"CSV LOADED")
# The last column is the label
X = df.iloc[:, :-2].drop('src_ip', axis=1).values
y = df.iloc[:, -1].values


# Need to encode labels to integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print(f"Y is encoded")

# Split dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

print(f"src_ip is dropped")
# Initialize and train model
print(f"classifying begins")
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
print(f"classifying ended and fitting begins")
model.fit(X_train, y_train)
print(f"fit complete")

# Predictions
predictions = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average='macro')

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"F1 Score (Macro Average): {f1 * 100:.2f}%")

