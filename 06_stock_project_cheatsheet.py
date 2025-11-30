# ============================================================
#  PYTHON PROJECT FOR DATA SCIENCE – CHEAT SHEET
#  Extracting and visualizing stock data (Tesla & GameStop)
# ============================================================

# --- (optional – only when running locally) -----------------
# Run once if the libraries are missing:
# !pip install yfinance
# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install plotly

# --- Imports ------------------------------------------------
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. Helper function – price & revenue chart
#    (top panel: stock price, bottom panel: revenue)
# ============================================================

def plot_price_and_revenue(stock_df, revenue_df, title: str) -> None:
    """
    Plot share price and quarterly revenue on two stacked subplots.

    Parameters
    ----------
    stock_df : pd.DataFrame
        DataFrame with at least columns: 'Date', 'Close'.
    revenue_df : pd.DataFrame
        DataFrame with at least columns: 'Date', 'Revenue'.
    title : str
        Plot title, e.g. 'Tesla (TSLA)'.
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.25,
        subplot_titles=("Share Price", "Quarterly Revenue")
    )

    # Share price
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_df["Date"]),
            y=stock_df["Close"].astype(float),
            name="Share Price"
        ),
        row=1,
        col=1
    )

    # Revenue
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_df["Date"]),
            y=revenue_df["Revenue"].astype(float),
            name="Revenue"
        ),
        row=2,
        col=1
    )

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue (USD Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=800,
        title_text=title
    )

    fig.show()


# ============================================================
# 2. Helper function – download price history from yfinance
# ============================================================

def get_stock_history(ticker_symbol: str, period: str = "max") -> pd.DataFrame:
    """
    Download historical stock data from yfinance.

    Parameters
    ----------
    ticker_symbol : str
        Ticker symbol, e.g. 'TSLA', 'GME'.
    period : str, default 'max'
        Period passed to yfinance.Ticker.history (e.g. '1y', '5y', 'max').

    Returns
    -------
    pd.DataFrame
        DataFrame with columns such as: Date, Open, High, Low, Close, Volume.
    """
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    hist.reset_index(inplace=True)  # move DatetimeIndex into a regular 'Date' column
    return hist


# ============================================================
# 3. Helper function – scrape quarterly revenue table
#    from Macrotrends (or a similar site)
# ============================================================

def get_revenue_from_macrotrends(url: str, table_label: str) -> pd.DataFrame:
    """
    Scrape a 'Quarterly Revenue' table from the Macrotrends page.

    Parameters
    ----------
    url : str
        Page URL, e.g. Tesla revenue page on Macrotrends.
    table_label : str
        Text snippet used to identify the correct table,
        e.g. 'Tesla Quarterly Revenue', 'GameStop Quarterly Revenue'.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - 'Date' (string in 'YYYY-MM-DD' format as on the page)
        - 'Revenue' (float, in USD, cleaned from '$' and commas)
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")

    target_table = None
    for tbl in tables:
        if table_label in tbl.get_text():
            target_table = tbl
            break

    if target_table is None:
        raise ValueError("Could not find revenue table on the page.")

    dates = []
    revenues = []

    for row in target_table.tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        date = cols[0].get_text(strip=True)
        revenue = cols[1].get_text(strip=True)

        if revenue == "" or revenue.lower() == "nan":
            continue

        dates.append(date)
        revenues.append(revenue)

    revenue_df = pd.DataFrame({"Date": dates, "Revenue": revenues})

    # Clean revenue format: remove '$' and commas, convert to float
    revenue_df["Revenue"] = (
        revenue_df["Revenue"]
        .str.replace(r"[$,]", "", regex=True)
        .astype(float)
    )

    # Sort ascending by date and reset index
    revenue_df = revenue_df.sort_values("Date")
    revenue_df.reset_index(drop=True, inplace=True)

    return revenue_df


# ============================================================
# 4. TESLA (TSLA) – yfinance price data + Macrotrends revenue
# ============================================================

# 4.1. Tesla share price from yfinance
tesla_stock = get_stock_history("TSLA", period="max")

# 4.2. Tesla quarterly revenue scraped from Macrotrends
tesla_revenue_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
tesla_revenue = get_revenue_from_macrotrends(
    tesla_revenue_url,
    "Tesla Quarterly Revenue"
)

# (optional) restrict date range, e.g. from 2015 onwards:
# tesla_stock = tesla_stock[tesla_stock["Date"] >= "2015-01-01"]
# tesla_revenue = tesla_revenue[tesla_revenue["Date"] >= "2015-01-01"]

# 4.3. Plot Tesla
plot_price_and_revenue(tesla_stock, tesla_revenue, "Tesla (TSLA)")


# ============================================================
# 5. GAMESTOP (GME) – yfinance price data + Macrotrends revenue
# ============================================================

# 5.1. GameStop share price from yfinance
gme_stock = get_stock_history("GME", period="max")

# 5.2. GameStop quarterly revenue scraped from Macrotrends
gme_revenue_url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
gme_revenue = get_revenue_from_macrotrends(
    gme_revenue_url,
    "GameStop Quarterly Revenue"
)

# (optional) restrict date range:
# gme_stock = gme_stock[gme_stock["Date"] >= "2015-01-01"]
# gme_revenue = gme_revenue[gme_revenue["Date"] >= "2015-01-01"]

# 5.3. Plot GameStop
plot_price_and_revenue(gme_stock, gme_revenue, "GameStop (GME)")


# ============================================================
# 6. Quick data checks (example EDA commands)
# ============================================================

print("TESLA STOCK DATA:")
print(tesla_stock.head(), "\n")

print("TESLA REVENUE DATA:")
print(tesla_revenue.head(), "\n")

print("GME STOCK DATA:")
print(gme_stock.head(), "\n")

print("GME REVENUE DATA:")
print(gme_revenue.head())
