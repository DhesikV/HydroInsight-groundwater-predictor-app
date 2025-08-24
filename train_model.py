import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("clean_groundwater.csv")

# Create label (1 = groundwater available, 0 = over-exploited)
df["Available"] = (df["Stage of GW extraction (%)"] < 100).astype(int)

# Features we’ll use
features = [
    "Monsoon season recharge from rainfall",
    "Monsoon season recharge from other sources",
    "Non-monsoon season recharge from rainfall",
    "Non-monsoon season recharge from other sources",
    "Total annual groundwater recharge",
    "Total Annual Extraction",
]

X = df[features]
y = df["Available"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
acc = accuracy_score(y_test, model.predict(X_test))
print("✅ Model trained. Accuracy:", acc)

# Save model
joblib.dump(model, "groundwater_model.pkl")
print("💾 Model saved as groundwater_model.pkl")
