import pandas as pd

df = pd.read_csv("clean_groundwater.csv")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nHead:\n", df.head())
