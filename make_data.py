from faker import Faker
import pandas as pd
import random

fake = Faker()

# Create fake data for 100 hours
data = []
for _ in range(100):
    data.append({
        "date": fake.date_this_year(),
        "shift": random.choice(["Morning", "Afternoon", "Night"]),
        "machine_id": fake.random_element(elements=("M1", "M2", "M3")),
        "operator": fake.name(),
        "product": fake.random_element(elements=("Toy Car", "Doll", "Robot")),
        "target_output": random.randint(50, 100),
        "actual_output": random.randint(40, 100),
        "defects": random.randint(0, 10),
        "downtime": random.randint(0, 60),
        "downtime_reason": fake.random_element(elements=("Broken", "No Power", "No Material", "None"))
    })

# Save to a CSV file (like a LEGO instruction sheet)
df = pd.DataFrame(data)
df.to_csv("toy_factory_data.csv", index=False)
df.to_csv(r"C:\Users\amanv\OneDrive\Desktop\Best_Group\toy_factory_data.csv", index=False)
print("Done! Created toy_factory_data.csv")