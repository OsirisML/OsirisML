import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np

# Trains an XGBoost model using only the top 20 most important features

TOP_20_FEATURES = [
    'ipv4_ttl_1',
    'tcp_opt_104',
    'tcp_opt_40',
    'tcp_opt_7',
    'ipv4_ttl_0',
    'tcp_opt_161',
    'tcp_opt_21',
    'tcp_opt_20',
    'tcp_opt_96',
    'ipv4_tos_4',
    'ipv4_dfbit_0',
    'tcp_ackf_0',
    'tcp_syn_0',
    'tcp_wsize_0',
    'tcp_wsize_2',
    'tcp_rst_0',
    'tcp_wsize_5',
    'tcp_opt_36',
    'tcp_wsize_1',
    'tcp_doff_3',
]

test_size_decimal = 0.2
usage_message = "Usage: python3 xgboostmodel_top10.py <data.csv> <model_name.json> OPTIONAL:<decimal for test split size, [0 - 1)>"

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print(usage_message)
    print("Note: only provide the file name, not the path. The csv file must be located in ../data/csv")
    sys.exit(1)
elif len(sys.argv) == 4:
    try:
        test_size_decimal = float(sys.argv[3])
        if not 0 <= test_size_decimal < 1:
            print(usage_message)
            print("Test split size must be a decimal value between 0 (inclusive) and 1")
            sys.exit(1)
    except ValueError:
        print(usage_message)
        print("Invalid test split size. Please provide a decimal value between 0 and 1")
        sys.exit(1)

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

# Verify all features exist in the data
missing = [f for f in TOP_20_FEATURES if f not in df.columns]
if missing:
    print(f"ERROR: Missing features in CSV: {missing}")
    sys.exit(1)

# Select only the top 10 features and the label column
X = df[TOP_20_FEATURES].values
y = df.iloc[:, -1].values
print(f"Using {len(TOP_20_FEATURES)} features: {TOP_20_FEATURES}")

# Encode labels to integers
label_encoder = LabelEncoder()
Y_encoded = label_encoder.fit_transform(y)
print(f"Y is encoded")

# Split dataset into training and testing set
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y_encoded, test_size=test_size_decimal, random_state=42)

# Initialize and train model
model = xgb.XGBClassifier(max_depth=10, use_label_encoder=False, eval_metric='mlogloss')
print(f"Fitting begins...")
model.fit(X_train, Y_train)
print(f"Fit complete!")
model.save_model("json/" + sys.argv[2])

# Predictions
print("Testing model with test size of " + str(test_size_decimal))
predictions = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(Y_test, predictions)
f1 = f1_score(Y_test, predictions, average='macro')

print(f"Model Accuracy: {accuracy}")
print(f"F1 Score (Macro Average): {f1}")

# Plot feature importance
feature_importance_dir = "feature_importance"
os.makedirs(feature_importance_dir, exist_ok=True)

importances = model.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(len(TOP_20_FEATURES)), importances[sorted_idx])
plt.xticks(range(len(TOP_20_FEATURES)), np.array(TOP_20_FEATURES)[sorted_idx], rotation=45, ha='right', fontsize=9)
plt.title("Top 20 Feature Importances (weight)")
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(os.path.join(feature_importance_dir, "top10_feature_importance.png"), dpi=150)
plt.close()
print(f"Saved feature importance plot to {feature_importance_dir}/top10_feature_importance.png")
