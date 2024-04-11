import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Load data
X_train = np.load('../data/npy/X_train.npy', allow_pickle=True)
X_test = np.load('../data/npy/X_test.npy', allow_pickle=True)
y_train = np.load('../data/npy/Y_train.npy', allow_pickle=True)
y_test = np.load('../data/npy/Y_test.npy', allow_pickle=True)

# Encode labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Set up parameter grid for grid search
param_grid = {
    'learning_rate': [0.1, 0.01, 0.001],
    'n_estimators': [100, 500, 1000],
    'max_depth': [4, 6, 8],
    'min_child_weight': [1, 3, 5],
    'gamma': [0.0, 0.1, 0.2],
}

# Initialize XGBoost model
print("running xgboost")
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

# Perform grid search
print("searching grid for optimal parameters")
grid_search = GridSearchCV(model, param_grid, scoring='accuracy', cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train_encoded)

# Get best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# Write best parameters to a file
with open("answers.txt", "w") as file:
    file.write("Best Parameters:\n")
    for key, value in best_params.items():
        file.write(f"{key}: {value}\n")

# Train best model
best_model = xgb.XGBClassifier(**best_params, use_label_encoder=False, eval_metric='mlogloss')
print("fitting model")
best_model.fit(X_train, y_train_encoded)

# Predictions
print("predicting...")
predictions = best_model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test_encoded, predictions)
f1 = f1_score(y_test_encoded, predictions, average='macro')

print(f"Model Accuracy: {accuracy}")
print(f"F1 Score (Macro Average): {f1}")
