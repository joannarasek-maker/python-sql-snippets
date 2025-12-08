"""
07_ml_pipeline_streamlit_template.py

Universal templates for:
- project folder structure
- sklearn ColumnTransformer + Pipeline (num + cat)
- train/test split + metrics + saving model
- minimal Streamlit app loading a .pkl model

Use as a cheat sheet and copy/paste into real projects.
"""

# ============================================================
# 1. PROJECT STRUCTURE (COMMENT ONLY)
# ============================================================
"""
Recommended ML project layout:

project/
  data/          # raw + clean data
  notebooks/     # EDA and modelling notebooks
  models/        # saved models (.pkl, .joblib)
  app/           # Streamlit or other app code
  requirements.txt
  README.md
"""


# ============================================================
# 2. COLUMNTRANSFORMER + PIPELINE (NUM + CAT)
# ============================================================

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Example feature lists – REPLACE with your own
numeric_features = ["num_feature_1", "num_feature_2", "num_feature_3"]
categorical_features = ["cat_feature_1", "cat_feature_2"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

rf_pipeline = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

# Usage in a real project:
# rf_pipeline.fit(X_train, y_train)
# y_pred = rf_pipeline.predict(X_test)


# ============================================================
# 3. TRAIN / TEST SPLIT + METRICS + SAVE MODEL
# ============================================================

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import joblib
import pandas as pd


def train_eval_save_model(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    model_pipeline: Pipeline,
    model_path: str = "models/model.pkl",
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Generic helper:
    - splits data
    - fits model
    - prints R² and RMSE
    - saves model to disk

    Parameters
    ----------
    df : pd.DataFrame
        Full dataset (features + target).
    feature_cols : list
        List of columns used as features.
    target_col : str
        Name of target column.
    model_pipeline : Pipeline
        sklearn Pipeline (with preprocessing + estimator).
    model_path : str
        Where to save the trained model.
    """

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"R²:   {r2:.3f}")
    print(f"RMSE: {rmse:,.0f}")

    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to: {model_path}")

    return model_pipeline, r2, rmse


# Example usage (replace with real data):
# df = pd.read_csv("data/your_clean_data.csv")
# feature_cols = numeric_features + categorical_features
# train_eval_save_model(df, feature_cols, target_col="price",
#                       model_pipeline=rf_pipeline,
#                       model_path="models/house_prices_rf.pkl")


# ============================================================
# 4. MINIMAL STREAMLIT APP TEMPLATE
# ============================================================

streamlit_template = r"""
# Save this content as app/app.py in a real project
# and run:  streamlit run app/app.py

import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/model.pkl")  # update path if needed

st.title("Generic ML Predictor")

st.write("Enter feature values to get a prediction.")

# Example input fields – REPLACE with your own
f1 = st.number_input("Numeric feature 1", value=0.0)
f2 = st.number_input("Numeric feature 2", value=0.0)
cat = st.text_input("Categorical feature", value="A")

if st.button("Predict"):
    X_new = pd.DataFrame(
        [
            {
                "num_feature_1": f1,
                "num_feature_2": f2,
                "cat_feature_1": cat,
            }
        ]
    )
    y_pred = model.predict(X_new)[0]
    st.success(f"Prediction: {y_pred:.2f}")
"""

# Note:
# The variable `streamlit_template` is just a text blob containing
# an example Streamlit app. Copy it into a separate file when needed.
if __name__ == "__main__":
    # This block is only for quick inspection when running the file directly.
    print("This file contains templates for:")
    print("- project structure")
    print("- sklearn ColumnTransformer + Pipeline")
    print("- training + metrics + saving model")
    print("- minimal Streamlit app (see `streamlit_template` variable)")
