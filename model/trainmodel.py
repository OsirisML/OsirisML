import pandas as pd
import numpy as np
from pandas.core.algorithms import mode
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import sys

usage_message = "python3 trainmodel.py <model to train> <training data>"
if len(sys.argv) != 3:
    print(usage_message)
    sys.exit(1)

print(f"Loading CSV File...")
csvPath = '../data/csv/' + sys.argv[2]
df = pd.read_csv(csvPath)
print(f"CSV LOADED")

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
y_encoded = label_encoder.fit_transform(y)
print(f"Y is encoded")

# Split dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42)
# Load the current model
model = xgb.Booster()
modelPath = '../model/json/' + sys.argv[1]
model.load_model(modelPath)
dtrain = xgb.DMatrix(X_train, label=y_train)
print(f"Training begins...")
params = {
    'max_depth': 10,
    'eta': 0.05
}

# Define your DMatrix for training and validation
dtrain = xgb.DMatrix(X_train, label=Y_train)
dval = xgb.DMatrix(X_val, label=Y_val)

# Specify the evaluation metric and set up the watchlist
evals = [(dtrain, 'train'), (dval, 'validation')]
eval_metric = 'error'  # You can change this to the appropriate metric for your problem

# Train the model with early stopping
bst = xgb.train(params, dtrain, num_boost_round=1000, evals=evals, early_stopping_rounds=10)

print(f"Training complete!")
bst.save_model("updated_xgboost_model.json")

# Predictions
dtest = xgb.DMatrix(X_test)
predictions_prob = bst.predict(dtest)
predictions = np.asarray([np.argmax(line) for line in predictions_prob])

# Evaluation
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average='macro')

print(f"Model Accuracy: {accuracy}")
print(f"F1 Score (Macro Average): {f1}")
