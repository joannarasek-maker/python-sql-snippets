"""
Intro to machine learning with scikit-learn.

Covers:
- representing data for ML (features X, labels y)
- simple LinearRegression on a tiny dataset
- train / test split and evaluation (MSE, R^2)
- basic classification example (LogisticRegression on iris)
- simple Pipeline with scaling + model

This is a learning cheat sheet, not production code.
"""

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    confusion_matrix,
    classification_report,
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_iris

# ============================================
# 1. Data representation: features X and labels y
# ============================================

# Example: very small dataset
# Columns: [is_female (0/1), height_cm]
X = np.array(
    [
        [1.0, 170],  # female, 170 cm
        [0.0, 180],  # male, 180 cm
        [1.0, 160],
        [0.0, 175],
        [1.0, 165],
    ]
)

# Target: weight in kg
y = np.array([65, 80, 55, 78, 60])

print("X shape:", X.shape)  # (n_samples, n_features)
print("y shape:", y.shape)  # (n_samples, )


# ============================================
# 2. Simple LinearRegression
# ============================================

reg = LinearRegression()
reg.fit(X, y)  # train model

print("\n=== Simple LinearRegression on tiny dataset ===")
print("Coefficients:", reg.coef_)        # one per feature
print("Intercept:", reg.intercept_)

# Predict on the training data (for demo only)
y_pred = reg.predict(X)
print("Predictions:", y_pred)
print("True values:", y)

mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print("MSE:", mse)
print("R^2:", r2)


# ============================================
# 3. Train / test split on a larger synthetic dataset
# ============================================

# Synthetic regression data:
# feature 0: hours studied
# feature 1: number of practice problems
rng = np.random.RandomState(42)
n_samples = 200

hours = rng.uniform(0, 10, size=n_samples)
problems = rng.randint(0, 50, size=n_samples)

X_reg = np.column_stack([hours, problems])

# True relationship (hidden):
# exam_score = 5 * hours + 0.3 * problems + noise
noise = rng.normal(0, 5, size=n_samples)
y_reg = 5 * hours + 0.3 * problems + noise

print("\nX_reg shape:", X_reg.shape)
print("y_reg shape:", y_reg.shape)

# Split into train / test
X_train, X_test, y_train, y_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Train model
reg2 = LinearRegression()
reg2.fit(X_train, y_train)

# Evaluate
y_train_pred = reg2.predict(X_train)
y_test_pred = reg2.predict(X_test)

print("\n=== Regression with train/test split ===")
print("Train MSE:", mean_squared_error(y_train, y_train_pred))
print("Train R^2:", r2_score(y_train, y_train_pred))
print("Test MSE:", mean_squared_error(y_test, y_test_pred))
print("Test R^2:", r2_score(y_test, y_test_pred))

print("Coefficients (hours, problems):", reg2.coef_)
print("Intercept:", reg2.intercept_)


# ============================================
# 4. Classification example: iris dataset
# ============================================

iris = load_iris()
X_clf = iris.data          # shape: (150, 4)
y_clf = iris.target        # 0, 1, 2 (setosa, versicolor, virginica)
target_names = iris.target_names

print("\nX_clf shape:", X_clf.shape)
print("y_clf shape:", y_clf.shape)
print("Target classes:", target_names)

# Train/test split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

# Logistic regression for multi-class classification
log_reg = LogisticRegression(
    max_iter=1000, multi_class="auto", solver="lbfgs"
)
log_reg.fit(X_train_c, y_train_c)

y_pred_c = log_reg.predict(X_test_c)

print("\n=== LogisticRegression on iris dataset ===")
print("Accuracy:", accuracy_score(y_test_c, y_pred_c))

cm = confusion_matrix(y_test_c, y_pred_c)
print("Confusion matrix:\n", cm)

print("\nClassification report:")
print(classification_report(y_test_c, y_pred_c, target_names=target_names))


# ============================================
# 5. Pipelines: scaling + model
# ============================================

"""
Many models work better when features are scaled (standardized).
Pipeline = sequence of steps: preprocessing -> model.

Here: StandardScaler (zero mean, unit variance) + LinearRegression.
"""

pipe = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ]
)

pipe.fit(X_train, y_train)  # reuse regression data from section 3
y_test_pipe = pipe.predict(X_test)

print("\n=== Pipeline: StandardScaler + LinearRegression ===")
print("Test MSE (pipeline):", mean_squared_error(y_test, y_test_pipe))
print("Test R^2 (pipeline):", r2_score(y_test, y_test_pipe))


# ============================================
# 6. ML project skeleton (functions only, no real code)
# ============================================

def load_data(path: str) -> pd.DataFrame:
    """Load data from CSV and return a pandas DataFrame."""
    return pd.read_csv(path)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare data:
    - handle missing values
    - encode categorical features
    - scale / normalize if needed
    """
    # TODO: add real preprocessing steps
    return df


def train_regression_model(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    """Train a simple regression model and return it."""
    model = LinearRegression()
    model.fit(X, y)
    return model


def main():
    """
    Example skeleton – not executed in this cheat sheet.
    In a real project you would:
    - load data
    - preprocess
    - split into train/test
    - train model
    - evaluate and save results
    """
    pass


if __name__ == "__main__":
    # For this cheat sheet we do not call main().
    # All examples above run on import.
    print("\nCheat sheet 05_ml_sklearn_intro.py executed.")
