import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)

n = 1000

data = {
    "Rainfall": np.random.randint(0, 250, n),
    "Temperature": np.random.randint(15, 40, n),
    "Humidity": np.random.randint(30, 100, n),
    "Water_Level": np.random.randint(0, 150, n),
    "Drainage_Capacity": np.random.randint(10, 100, n),
    "Soil_Moisture": np.random.randint(10, 100, n)
}

df = pd.DataFrame(data)

# Assign flood risk labels using sample rules
def predict_risk(row):

    score = 0

    if row["Rainfall"] > 100:
        score += 2
    elif row["Rainfall"] > 50:
        score += 1

    if row["Water_Level"] > 90:
        score += 2
    elif row["Water_Level"] > 50:
        score += 1

    if row["Drainage_Capacity"] < 30:
        score += 2
    elif row["Drainage_Capacity"] < 50:
        score += 1

    if row["Soil_Moisture"] > 80:
        score += 1

    if score >= 4:
        return "High"
    elif score >= 2:
        return "Moderate"
    else:
        return "Low"


df["Flood_Risk"] = df.apply(predict_risk, axis=1)

# Save dataset
df.to_csv("data/flood_dataset.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("\nFlood risk distribution:")
print(df["Flood_Risk"].value_counts())
