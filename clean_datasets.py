
import pandas as pd
import os

os.makedirs("cleaned_data", exist_ok=True)

# 1. Clean rainfall dataset
rain = pd.read_csv("data/daily_rainfall.csv")

rain.columns = (
    rain.columns
    .str.strip()
    .str.replace("\n", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
)

rain["Date"] = pd.to_datetime(rain["Date"], errors="coerce")

rain["Daily Departure Per"] = pd.to_numeric(
    rain["Daily Departure Per"].astype(str).str.replace("%", ""),
    errors="coerce"
)

rain.to_csv("cleaned_data/daily_rainfall_cleaned.csv", index=False)


# 2. Clean DFSI dataset
dfsi = pd.read_csv("data/DFSI.csv")

dfsi = dfsi.rename(columns={"Unnamed: 0": "District"})
dfsi["DFSI"] = dfsi["DFSI"].fillna(dfsi["DFSI"].median())

dfsi.to_csv("cleaned_data/DFSI_cleaned.csv", index=False)


# 3. Clean flood impact dataset
impact = pd.read_csv("data/District_FloodImpact.csv")

impact["Mean_Flood_Duration"] = (
    impact["Mean_Flood_Duration"]
    .fillna(impact["Mean_Flood_Duration"].median())
)

impact.to_csv("cleaned_data/FloodImpact_cleaned.csv", index=False)


# 4. Clean flood inventory
flood = pd.read_csv("data/India_Flood_Inventory_v3.csv")

flood["Start Date"] = pd.to_datetime(
    flood["Start Date"], errors="coerce"
)

flood["End Date"] = pd.to_datetime(
    flood["End Date"], errors="coerce"
)

flood.to_csv("cleaned_data/FloodInventory_cleaned.csv", index=False)


# 5. Copy other datasets without changing their values
files = [
    "District_FloodedArea.csv",
    "district_wise_details.csv",
    "rwl_tele_hr_national-institute-of-hydrology-roorkee_27_1991_2020.csv"
]

for file in files:
    df = pd.read_csv(os.path.join("data", file))
    output = file.replace(".csv", "_cleaned.csv")
    df.to_csv(os.path.join("cleaned_data", output), index=False)

print("All cleaning operations completed!")
print("Check the cleaned_data folder.")
