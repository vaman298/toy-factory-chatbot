import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load data
data = pd.read_csv("toy_factory_data.csv")

# Convert text to numbers
data["machine_id"] = data["machine_id"].map({"M1": 1, "M2": 2, "M3": 3})
data["downtime_reason"] = data["downtime_reason"].map({"None": 0, "Broken": 1, "No Power": 2, "No Material": 3})

# Features and Target
X = data[["machine_id", "downtime_reason", "actual_output"]]
y = (data["downtime"] > 30).astype(int)  # 1 if downtime >30 mins

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "downtime_model.pkl")
print("Model trained and saved!")