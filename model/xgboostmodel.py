import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Creates a binary file for the OS fingerprint model using XGBoost
# By default, a test size of 0.2 is used. See usage to use an additional sys arg to change this

test_size_decimal = 0.2
usage_message = "Usage: python3 <this_script.py> <csv filename wth .csv> <model name with no extension> OPTIONAL:<decimal for test split size, [0 - 1)>"

# Check if the correct number of arguments are provided
if len(sys.argv) != 3 and len(sys.argv) != 4:
    print(usage_message)
    print("Note: only provide the file name, not the path. The csv file must be located in ../data/csv")
    sys.exit(1)  # Exit with error code 1
elif len(sys.argv) == 4: # valid number of arguments
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
# else: test size is left to 0.2 by default


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
# Initialize and train model
model = xgb.XGBClassifier(learning_rate=0.001, n_estimators=100, max_depth=8, min_child_weight=1, gamma=0,
    use_label_encoder=False, eval_metric='mlogloss')
print(f"Fitting begins...")
model.fit(X_train, Y_train)
print(f"Fit complete!")
model.save_model("json/" + sys.argv[2] + ".json")
# Predictions
print("Testing model with test size of " + str(test_size_decimal))
predictions = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(Y_test, predictions)
f1 = f1_score(Y_test, predictions, average='macro')

print(f"Model Accuracy: {accuracy}")
print(f"F1 Score (Macro Average): {f1}")
