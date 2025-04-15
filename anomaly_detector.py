import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies():
    data = pd.read_csv("toy_factory_data.csv")
    X = data[["actual_output", "defects", "downtime"]]
    
    # Train model
    model = IsolationForest(contamination=0.1)
    model.fit(X)
    
    # Predict anomalies
    data["is_anomaly"] = model.predict(X)
    anomalies = data[data["is_anomaly"] == -1]
    
    return anomalies