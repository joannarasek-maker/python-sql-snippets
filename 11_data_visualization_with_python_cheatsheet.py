"""
IBM: Data Visualization with Python — GitHub Cheat Sheet

What you get in this file:
- Matplotlib: line, bar, histogram, scatter (+ best-fit line), subplots, pie, boxplot
- Seaborn: countplot, barplot, histplot (stack), scatterplot, regplot
- WordCloud: generate + display
- Folium: basic map, tiles, markers, CircleMarker, FeatureGroup, MarkerCluster, Choropleth
- Pandas pivot + bar chart
- Plotly Express treemap

How to use:
1) Install what you need (see INSTALL section).
2) Run sections you need by uncommenting.
3) Replace example DataFrames with your own datasets.

Recommended filename:
    11_data_visualization_with_python_cheatsheet.py
"""

# =========================
# INSTALL (run once)
# =========================
# pip install matplotlib seaborn folium wordcloud plotly pandas numpy

# =========================
# IMPORTS
# =========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Optional (uncomment if installed)
# import seaborn as sns
# import folium
# from folium import plugins
# from wordcloud import WordCloud, STOPWORDS
# import plotly.express as px


# =========================
# DEMO DATA (safe defaults)
# =========================
df_demo = pd.DataFrame(
    {
        "x": np.arange(1, 21),
        "y": np.random.default_rng(42).normal(0, 1, 20).cumsum(),
        "category": ["A"] * 10 + ["B"] * 10,
        "value": np.random.default_rng(1).integers(1, 100, 20),
        "region": ["NSW", "QL", "SA", "TA", "VI"] * 4,
        "year": [2023] * 10 + [2024] * 10,
    }
)

# =========================
# 1) MATPLOTLIB BASICS
# =========================
def mpl_template():
    plt.figure(figsize=(8, 4))
    plt.plot(df_demo["x"], df_demo["y"])
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Matplotlib Template: Line Plot")
    plt.show()


# =========================
# 2) LINE PLOT
# =========================
def mpl_line():
    plt.figure(figsize=(8, 4))
    plt.plot(df_demo["x"], df_demo["y"])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Line Plot")
    plt.show()


# =========================
# 3) BAR PLOT
# =========================
def mpl_bar():
    counts = df_demo["category"].value_counts()
    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)
    plt.xlabel("category")
    plt.ylabel("count")
    plt.title("Bar Chart")
    plt.show()


# =========================
# 4) HISTOGRAM
# =========================
def mpl_hist():
    plt.figure(figsize=(7, 4))
    plt.hist(df_demo["value"], bins=10)
    plt.xlabel("value")
    plt.ylabel("count")
    plt.title("Histogram")
    plt.show()


# =========================
# 5) SCATTER + BEST FIT LINE (np.polyfit)
# =========================
def mpl_scatter_best_fit():
    x = df_demo["x"]
    y = df_demo["y"]
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y)

    z = np.polyfit(x, y, 1)  # slope, intercept
    p = np.poly1d(z)
    plt.plot(x, p(x))

    eq = f"y = {z[0]:.3f}x + {z[1]:.3f}"
    plt.title(f"Scatter + Best Fit Line\n{eq}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


# =========================
# 6) SUBPLOTS
# =========================
def mpl_subplots():
    fig = plt.figure(figsize=(12, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(df_demo["x"], df_demo["y"])
    ax1.set_title("Line")

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.hist(df_demo["value"], bins=10)
    ax2.set_title("Histogram")

    plt.show()


# =========================
# 7) PIE CHART
# =========================
def mpl_pie():
    counts = df_demo["category"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Pie Chart")
    plt.axis("equal")
    plt.show()


# =========================
# 8) BOX PLOT
# =========================
def mpl_box():
    plt.figure(figsize=(6, 4))
    plt.boxplot(df_demo["value"])
    plt.title("Box Plot")
    plt.show()


# =========================
# 9) SEABORN EXAMPLES (uncomment imports to use)
# =========================
def seaborn_examples():
    """
    Requires:
        import seaborn as sns
    """
    # Countplot
    plt.figure(figsize=(7, 4))
    sns.countplot(x="region", data=df_demo)
    plt.title("Seaborn Countplot")
    plt.show()

    # Barplot
    plt.figure(figsize=(7, 4))
    sns.barplot(x="category", y="value", data=df_demo)
    plt.title("Seaborn Barplot")
    plt.show()

    # Histplot (stacked)
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df_demo, x="value", hue="category", multiple="stack")
    plt.title("Seaborn Histplot (stacked)")
    plt.show()

    # Scatterplot
    plt.figure(figsize=(7, 4))
    sns.scatterplot(data=df_demo, x="x", y="y", hue="category")
    plt.title("Seaborn Scatterplot")
    plt.show()

    # Regplot (regression line)
    plt.figure(figsize=(7, 4))
    sns.regplot(x="x", y="y", data=df_demo, scatter_kws={"s": 80})
    plt.title("Seaborn Regplot")
    plt.show()


# =========================
# 10) WORDCLOUD (uncomment imports to use)
# =========================
def wordcloud_example():
    """
    Requires:
        from wordcloud import WordCloud, STOPWORDS
    """
    text = "data science python visualization matplotlib seaborn folium plotly dashboard storytelling " * 10
    wc = WordCloud(background_color="white", stopwords=set(STOPWORDS)).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("WordCloud")
    plt.show()


# =========================
# 11) FOLIUM MAPS (uncomment imports to use)
# =========================
def folium_examples():
    """
    Requires:
        import folium
        from folium import plugins
    Creates HTML files in current folder for viewing in browser.
    """
    # Basic world map
    world_map = folium.Map(location=[0, 0], zoom_start=2)

    # Tiles styles
    m_dark = folium.Map(location=[0, 0], zoom_start=2, tiles="Cartodb_dark_matter")
    m_light = folium.Map(location=[0, 0], zoom_start=2, tiles="Cartodb_positron")

    # Marker + CircleMarker
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    folium.Marker([37.7749, -122.4194], popup="San Francisco").add_to(m)

    fg = folium.map.FeatureGroup()
    fg.add_child(
        folium.features.CircleMarker(
            location=[37.7749, -122.4194],
            radius=6,
            color="red",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup="CircleMarker"
        )
    )
    m.add_child(fg)

    # MarkerCluster
    cluster_map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    cluster = plugins.MarkerCluster().add_to(cluster_map)
    folium.Marker([37.7749, -122.4194], popup="Example").add_to(cluster)

    # Save to HTML
    world_map.save("folium_world_map.html")
    m_dark.save("folium_dark_map.html")
    m_light.save("folium_light_map.html")
    m.save("folium_markers_map.html")
    cluster_map.save("folium_cluster_map.html")

    print("Saved folium HTML files to current directory.")


# =========================
# 12) FOLIUM CHOROPLETH (template)
# =========================
def folium_choropleth_template():
    """
    Requires:
        import folium
    You need:
        - geojson path or object
        - DataFrame with region + value columns
    """
    # Example template (replace placeholders):
    # m = folium.Map(location=[0, 0], zoom_start=2)
    # folium.Choropleth(
    #     geo_data="path/to/geojson.json",
    #     data=df,
    #     columns=["region", "value"],
    #     key_on="feature.properties.name",
    #     fill_color="YlOrRd",
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name="Legend Title"
    # ).add_to(m)
    # m.save("choropleth.html")
    pass


# =========================
# 13) PIVOT TABLE + BAR CHART (pandas)
# =========================
def pivot_bar_example():
    # Create pivot (example)
    pivot = df_demo.pivot_table(index="year", columns="category", values="value", aggfunc="mean")
    pivot.plot(kind="bar", figsize=(9, 4))
    plt.title("Pivot Table Bar Chart")
    plt.xlabel("year")
    plt.ylabel("mean value")
    plt.legend(title="category")
    plt.show()


# =========================
# 14) PLOTLY TREEMAP (template)
# =========================
def plotly_treemap_template():
    """
    Requires:
        import plotly.express as px
    """
    sales_df = pd.DataFrame({
        "Category": ["A", "A", "B", "B"],
        "Subcategory": ["A1", "A2", "B1", "B2"],
        "Sales": [100, 150, 200, 80]
    })
    fig = px.treemap(
        sales_df,
        path=["Category", "Subcategory"],
        values="Sales",
        title="Sales Treemap"
    )
    fig.show()


# =========================
# MAIN (run what you want)
# =========================
def main():
    mpl_template()
    mpl_line()
    mpl_bar()
    mpl_hist()
    mpl_scatter_best_fit()
    mpl_subplots()
    mpl_pie()
    mpl_box()
    pivot_bar_example()

    # Uncomment after installing libs:
    # seaborn_examples()
    # wordcloud_example()
    # folium_examples()
    # plotly_treemap_template()


if __name__ == "__main__":
    main()
