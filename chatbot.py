import pandas as pd
import joblib
from anomaly_detector import detect_anomalies

# Load data and model
data = pd.read_csv("toy_factory_data.csv")
downtime_model = joblib.load("downtime_model.pkl")

# Valid machines
valid_machines = ["M1", "M2", "M3"]

def predict_downtime_risk(machine):
    if machine not in valid_machines:
        return f"Error: {machine} is invalid. Use M1, M2, or M3."
    
    # Get latest data for the machine
    machine_data = data[data["machine_id"] == machine]
    if machine_data.empty:
        return "No data found for this machine."
    
    latest = machine_data.iloc[-1]
    
    # Convert text to numbers (same as training)
    machine_code = {"M1": 1, "M2": 2, "M3": 3}.get(latest["machine_id"], 1)
    downtime_reason_code = {"None": 0, "Broken": 1, "No Power": 2, "No Material": 3}.get(latest["downtime_reason"], 0)
    actual_output = latest["actual_output"]
    
    # Prepare input for the model
    input_data = pd.DataFrame([[machine_code, downtime_reason_code, actual_output]],
                              columns=["machine_id", "downtime_reason", "actual_output"])
    
    # Predict
    risk = downtime_model.predict_proba(input_data)[0][1] * 100
    return f"{risk:.2f}% risk of downtime in 2 hours."

def ask_robot():
    print("Robot: Hi! I can answer:")
    print("- Total defects by machine (e.g., 'total defects for M1')")
    print("- Operator's production (e.g., 'units by operator John')")
    print("- Downtime risk (e.g., 'predict risk for M2')")
    
    while True:
        question = input("\nYou: ").strip().lower()
        
        # Check for anomalies
        anomalies = detect_anomalies()
        if not anomalies.empty:
            print("\nALERT! Anomaly detected in last hour:")
            print(anomalies[["machine_id", "actual_output", "defects"]].tail(1))
        
        # Total defects query
        if "total defects" in question:
            machine = None
            # Search for valid machine in the question
            for word in question.upper().split():
                if word in valid_machines:
                    machine = word
                    break
            if not machine:
                print("Error: Specify a valid machine (M1, M2, M3).")
                continue
            
            defects = data[data["machine_id"] == machine]["defects"].sum()
            print(f"Total defects for {machine}: {defects}")
        
        # Operator units query
        elif "units" in question and "operator" in question:
            operator = None
            # Extract operator name (supports "by John", "operator John", etc.)
            parts = question.title().split()
            for i, word in enumerate(parts):
                if word == "Operator" and i < len(parts)-1:
                    operator = parts[i+1]
                    break
                elif word in data["operator"].values:
                    operator = word
                    break
            
            if not operator:
                print("Error: Specify an operator name (e.g., 'John').")
                continue
            
            units = data[data["operator"] == operator]["actual_output"].sum()
            print(f"{operator} produced {units} units last shift.")
        
        # Downtime risk prediction
        elif "predict" in question and "risk" in question:
            machine = None
            for word in question.upper().split():
                if word in valid_machines:
                    machine = word
                    break
            if not machine:
                print("Error: Specify a machine (M1, M2, M3).")
                continue
            
            print(predict_downtime_risk(machine))
        
        else:
            print("Ask about defects, units, or downtime risk.")

if __name__ == "__main__":
    ask_robot()