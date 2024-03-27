import pandas as pd
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.model_selection import train_test_split

df = pd.read_csv('labeled_dataset.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Need to encode labels to integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

dtrain = xgb.DMatrix(X_train, label=y_train)
dtrain.save_binary('train.buffer')
dtest = xgb.DMatrix(X_test, label=y_test)
dtrain.save_binary('test.buffer')