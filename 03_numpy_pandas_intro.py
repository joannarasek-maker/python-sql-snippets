"""
NumPy & pandas intro cheat sheet.

Covers:
- NumPy arrays: creation, dtype, shape
- basic vectorized operations and statistics
- special arrays (zeros, ones, random)
- boolean masks and indexing
- pandas Series and DataFrame
- selecting rows/columns, filtering
- simple groupby and new columns
"""

# ============================================
# 1. NumPy – basic arrays
# ============================================

import numpy as np
import pandas as pd

# 1D array
a = np.array([1, 2, 3, 4])
print("a:", a)
print("a dtype:", a.dtype)
print("a shape:", a.shape)   # (4,)

# 2D array
b = np.array([[1, 2], [3, 4]])
print("b:\n", b)
print("b shape:", b.shape)   # (2, 2)

# Vectorized operations
c = np.array([10, 20, 30, 40])
print("a + c:", a + c)       # elementwise addition
print("a * 2:", a * 2)       # scalar multiplication

# Elementwise functions
print("np.sqrt(a):", np.sqrt(a))
print("np.log(a):", np.log(a))

# Basic statistics
print("mean:", a.mean())
print("std:", a.std())
print("min / max:", a.min(), a.max())
print("sum:", a.sum())

# ============================================
# 2. Special arrays and random
# ============================================

zeros = np.zeros((2, 3))
ones = np.ones((3, 2))
rand = np.random.rand(2, 2)      # random numbers from [0, 1)

print("zeros:\n", zeros)
print("ones:\n", ones)
print("rand:\n", rand)

# Reproducible randomness (seed)
np.random.seed(42)
rand_ints = np.random.randint(low=0, high=10, size=(3, 3))
print("rand_ints:\n", rand_ints)

# ============================================
# 3. Indexing, slicing, boolean masks
# ============================================

arr = np.array([5, 10, 15, 20, 25])
print("arr:", arr)

# Indexing and slicing
print("arr[0]:", arr[0])
print("arr[1:4]:", arr[1:4])      # [10, 15, 20]

# Boolean mask
mask = arr > 10
print("mask:", mask)
print("arr[mask]:", arr[mask])    # values > 10

# Setting values with mask
arr[mask] = 99
print("arr after mask assignment:", arr)

# ============================================
# 4. pandas Series
# ============================================

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print("Series s:\n", s)

print("s['b']:", s["b"])          # access by label
print("s.values:", s.values)      # underlying NumPy array
print("s.index:", s.index)

# Basic methods
print("s.describe():\n", s.describe())

# ============================================
# 5. pandas DataFrame – creation
# ============================================

data = {
    "City": ["Toronto", "Chicago", "New York", "Toronto"],
    "Population": [2.9, 2.7, 8.4, 2.9],
    "Country": ["Canada", "USA", "USA", "Canada"],
    "Year": [2020, 2020, 2020, 2021],
}

df = pd.DataFrame(data)
print("DataFrame df:\n", df)

print("df.head():\n", df.head())
print("df.info():")
print(df.info())
print("df.describe():\n", df.describe(numeric_only=True))

# ============================================
# 6. Selecting columns and rows
# ============================================

# Single column (returns Series)
print("df['City']:\n", df["City"])

# Multiple columns (returns DataFrame)
print("df[['City', 'Country']]:\n", df[["City", "Country"]])

# Row by position (iloc)
print("df.iloc[0]:\n", df.iloc[0])

# Row by index label (loc) – here index is default 0,1,2,3
print("df.loc[1]:\n", df.loc[1])

# Slicing rows
print("df.iloc[1:3]:\n", df.iloc[1:3])

# ============================================
# 7. Filtering rows (boolean indexing)
# ============================================

# Cities in USA
usa_cities = df[df["Country"] == "USA"]
print("usa_cities:\n", usa_cities)

# Population >= 3.0
big_cities = df[df["Population"] >= 3.0]
print("big_cities:\n", big_cities)

# Multiple conditions: use & and | with parentheses
canada_2020 = df[(df["Country"] == "Canada") & (df["Year"] == 2020)]
print("canada_2020:\n", canada_2020)

# ============================================
# 8. New columns and basic transformations
# ============================================

# Copy to avoid modifying original in larger projects
df2 = df.copy()

# New column
df2["Population_millions"] = df2["Population"]
print("df2 with new column:\n", df2)

# Simple transformation
df2["Population_log"] = np.log(df2["Population"])
print("df2 with log column:\n", df2)

# ============================================
# 9. Groupby examples
# ============================================

# Average population per country
group_country = df.groupby("Country")["Population"].mean()
print("Mean population by Country:\n", group_country)

# Count rows per city
city_counts = df["City"].value_counts()
print("City counts:\n", city_counts)

# Group by multiple columns
group_city_year = df.groupby(["City", "Year"])["Population"].mean()
print("Mean population by City & Year:\n", group_city_year)

# Convert groupby result to DataFrame (reset index)
group_city_year_df = group_city_year.reset_index()
print("group_city_year_df:\n", group_city_year_df)
