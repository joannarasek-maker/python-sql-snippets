"""
IBM: Data Analysis with Python — CHEAT SHEET

Scope:
- pandas & NumPy basics
- loading and inspecting data
- data cleaning & missing values
- filtering & sorting
- feature engineering
- aggregation & groupby
- pivot tables
- correlation analysis
- basic EDA workflow

Author: Joanna Rasek
Source: IBM Data Analyst Professional Certificate
"""

# =========================
# 1. IMPORTS
# =========================

import numpy as np
import pandas as pd

# =========================
# 2. LOAD DATA
# =========================

df = pd.read_csv("data.csv")
# df = pd.read_excel("data.xlsx")
# df = pd.read_json("data.json")

# =========================
# 3. QUICK INSPECTION
# =========================

df.head()
df.tail()
df.shape
df.info()
df.describe(include="all")
df.columns
df.dtypes

# =========================
# 4. DATA TYPES
# =========================

df["price"] = df["price"].astype(float)
df["year"] = df["year"].astype(int)

# =========================
# 5. MISSING VALUES
# =========================

df.isnull().sum()

df.dropna(inplace=True)

df["price"].fillna(df["price"].mean(), inplace=True)
df["brand"].fillna("Unknown", inplace=True)

# =========================
# 6. DUPLICATES
# =========================

df.duplicated().sum()
df.drop_duplicates(inplace=True)

# =========================
# 7. INDEXING & SELECTION
# =========================

df["price"]
df[["price", "brand"]]

df.loc[0]
df.iloc[0]

df.loc[:, ["price", "brand"]]
df.iloc[0:5, 0:3]

# =========================
# 8. FILTERING
# =========================

df[df["price"] > 20000]

df[
    (df["price"] > 20000) &
    (df["year"] >= 2020)
]

df[df["brand"].isin(["Toyota", "BMW"])]

# =========================
# 9. SORTING
# =========================

df.sort_values(by="price", ascending=False)
df.sort_values(by=["brand", "price"], ascending=[True, False])

# =========================
# 10. FEATURE ENGINEERING
# =========================

df["price_k"] = df["price"] / 1000
df["age"] = 2024 - df["year"]

df["price_category"] = df["price"].apply(
    lambda x: "High" if x > 30000 else "Low"
)

# =========================
# 11. VALUE COUNTS
# =========================

df["brand"].value_counts()
df["brand"].value_counts(normalize=True)

# =========================
# 12. AGGREGATION
# =========================

df["price"].mean()
df["price"].median()
df["price"].std()
df["price"].min()
df["price"].max()

# =========================
# 13. GROUPBY
# =========================

df.groupby("brand")["price"].mean()

df.groupby("brand").agg(
    avg_price=("price", "mean"),
    max_price=("price", "max"),
    count=("price", "count")
)

# =========================
# 14. PIVOT TABLES
# =========================

pd.pivot_table(
    df,
    values="price",
    index="brand",
    columns="year",
    aggfunc="mean"
)

# =========================
# 15. CORRELATION
# =========================

df.corr(numeric_only=True)
df[["price", "age"]].corr()

# =========================
# 16. STRING OPERATIONS
# =========================

df["brand"] = df["brand"].str.upper()
df["brand"].str.contains("BMW")
df["brand"].str.replace(" ", "_")

# =========================
# 17. RENAME COLUMNS
# =========================

df.rename(
    columns={"old_name": "new_name"},
    inplace=True
)

# =========================
# 18. EXPORT DATA
# =========================

df.to_csv("clean_data.csv", index=False)
df.to_excel("clean_data.xlsx", index=False)

# =========================
# 19. IBM EDA WORKFLOW
# =========================

"""
1. Load data
2. Inspect structure & summary
3. Handle missing values
4. Remove duplicates
5. Convert data types
6. Feature engineering
7. Aggregations & groupby
8. Correlation analysis
9. Export clean dataset
"""

# =========================
# END
# =========================
