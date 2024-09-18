# Scikit-learn Notes

## Introduction
Scikit-learn is a powerful machine learning library in Python. It provides a wide range of algorithms for classification, regression, clustering, and dimensionality reduction.

## Key Modules

### 1. Preprocessing
- Used for feature scaling and normalization
- Example: `StandardScaler`, `MinMaxScaler`

### 2. Model Selection
- Provides tools for model evaluation and hyperparameter tuning
- Example: `train_test_split`, `GridSearchCV`

### 3. Metrics
- Functions to assess model performance
- Example: `accuracy_score`, `mean_squared_error`

## Basic Usage Example

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Assume X and y are your features and target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

predictions = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, predictions)
print(f"Model accuracy: {accuracy}")
```

## Resources
- [Scikit-learn Official Documentation](https://scikit-learn.org/stable/documentation.html)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
