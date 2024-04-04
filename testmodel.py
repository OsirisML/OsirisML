import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder

#load in model
print(f"Being loading model")
model = xgb.XGBClassifier()
model.load_model('xgboost_model.bin')
print(f"Model is loaded in")

#read in data
print(f"Begin reading in data")
df = pd.read_csv("friday_labeled_dataset.csv")
print(f"Data is read in")

#remove src ip and labels column
X = df.iloc[:, 1:-1]
y_test = df.iloc[:, -1]
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_test)

print(f"Predictions started...")

#make predictions
pred = model.predict(X)
print(f"Predictions finished: ")
acc = accuracy_score(y_encoded, pred)
f1 = f1_score(y_encoded, pred, average='macro')

print(f"Model Accuracy: {acc * 100:.2f}%")
print(f"Macro F1 Score: {f1 * 100:.2f}%")
