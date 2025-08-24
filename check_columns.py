import pandas as pd

df = pd.read_csv("clean_groundwater.csv")

print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())
