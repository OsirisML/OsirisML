import numpy as np
from sklearn.metrics import accuracy_score
import xgboost as xgb 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score

x_train = np.load('X_train.npy', allow_pickle=True)
x_test = np.load('X_test.npy', allow_pickle=True)
y_train = np.load('y_train.npy', allow_pickle=True)
y_test = np.load('y_test.npy', allow_pickle=True)

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model.fit(x_train, y_train_encoded)

predictions = model.predict(x_test)
accuracy = accuracy_score(y_test_encoded, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
f1 = f1_score(y_test_encoded, predictions, average='macro')
print(f"F1 Score (Macro Average): {f1 * 100:.2f}%")