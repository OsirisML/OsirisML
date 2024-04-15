import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Load data
print(f"Loading CSV File: {sys.argv[1]}")
try:
    df = pd.read_csv(f"../data/csv/{sys.argv[1]}")
    print(f"CSV file loaded")
except FileNotFoundError:
    print(usage_message)
    print(f"ERROR: File '{sys.argv[1]}' not found")
    sys.exit(1)
except Exception as e:
    print(usage_message)
    print(f"ERROR: {e}")
    sys.exit(1)

print(f"Creating X/Y splits and training/testing splits")

# mark the byte ranges to remove to avoid data leakage from overfitting source IP
ipv4_source_start, ipv4_source_end = 97, 129
ipv4_destination_start, ipv4_destination_end = 130, 160
ipv4_identification_start, ipv4_identification_end = 33, 48

tcp_source_port_start, tcp_source_port_end = 480, 496
tcp_destination_port_start, tcp_destination_port_end = 496, 512
tcp_sequence_start, tcp_sequence_end = 512, 544
tcp_ack_start, tcp_ack_end = 544, 576

# Combine all ranges to remove, including the first column (index 0)
columns_to_remove = [0] + \
    list(range(ipv4_source_start, ipv4_source_end + 1)) + \
    list(range(ipv4_destination_start, ipv4_destination_end + 1)) + \
    list(range(ipv4_identification_start, ipv4_identification_end + 1)) + \
    list(range(tcp_source_port_start, tcp_source_port_end + 1)) + \
    list(range(tcp_destination_port_start, tcp_destination_port_end + 1)) + \
    list(range(tcp_sequence_start, tcp_sequence_end + 1)) + \
    list(range(tcp_ack_start, tcp_ack_end + 1))

# Adjusting for removal from a DataFrame where columns are referenced by their integer location

df.drop(df.columns[columns_to_remove], axis=1, inplace=True)

# The last column is the label
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values
print(f"X and Y set")

# Need to encode labels to integers
label_encoder = LabelEncoder()
Y_encoded = label_encoder.fit_transform(y)
print(f"Y is encoded")

# Split dataset into training and testing set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_encoded, test_size=test_size_decimal, random_state=42)

# Set up parameter grid for grid search
param_grid = {
    # Hyper Parameter Optimization
    # 162 tree combinations (3 * 3 * 3 * 3 * 2)
    n_estimators = [100, 500, 1100,],
    max_depth = [5, 8, 12],
    booster=['gbtree','gblinear'],
    min_child_weight=[1,2,3],
    'gamma': [0.0, 0.1, 0.2]
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
