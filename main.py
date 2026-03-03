import pandas as pd
import numpy as np
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Load dataset
df = pd.read_csv("phishing_urls.csv")

# Keep only needed columns
df = df[["url", "label"]]

def extract_features(url):
    features = []

    url = str(url)

    # 1. Has IP address
    if re.match(r"^(http[s]?://)?(\d{1,3}\.){3}\d{1,3}", url):
        features.append(1)
    else:
        features.append(0)

    # 2. URL length
    features.append(len(url))

    # 3. Has @
    features.append(1 if "@" in url else 0)

    # 4. Has -
    features.append(1 if "-" in url else 0)

    # 5. Number of dots
    features.append(url.count("."))

    # 6. Has https
    features.append(1 if "https" in url else 0)

    # 7. Number of /
    features.append(url.count("/"))

    # 8. Has suspicious words
    suspicious_words = ["login", "secure", "bank", "update", "verify"]
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    return features


# Build feature matrix
X = np.array([extract_features(url) for url in df["url"]])
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
pickle.dump(model, open("url_model.pkl", "wb"))

print("Model trained and saved successfully!")

