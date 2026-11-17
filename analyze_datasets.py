
import pandas as pd
import os

folder = "data"

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)
        df = pd.read_csv(path)

        print("\n" + "=" * 50)
        print("DATASET:", file)
        print("=" * 50)

        print("Rows and columns:", df.shape)

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nFirst 5 records:")
        print(df.head())

        print("\nMissing values:")
        print(df.isnull().sum())

        print("\nDuplicate records:", df.duplicated().sum())

        print("\nData types:")
        print(df.dtypes)

print("\nAll datasets analysed!")
