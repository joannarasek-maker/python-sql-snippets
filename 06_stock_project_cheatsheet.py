# ============================================================
#  PYTHON PROJECT FOR DATA SCIENCE – CHEAT SHEET
#  Extracting and visualizing stock data (Tesla & GameStop)
# ============================================================

# --- (opcjonalnie – tylko przy pracy lokalnej) ------------
# Uruchom raz, jeśli brakuje bibliotek:
# !pip install yfinance
# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install plotly

# --- Importy -----------------------------------------------
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. Funkcja rysująca wykres ceny akcji i przychodu
#    (górny panel: kurs akcji, dolny panel: revenue)
# ============================================================

def plot_price_and_revenue(stock_df, revenue_df, title):
    """
    stock_df   – DataFrame z kolumnami: Date, Close
    revenue_df – DataFrame z kolumnami: Date, Revenue
    title      – tytuł wykresu (np. 'Tesla (TSLA)')
    """

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.25,
        subplot_titles=("Share Price", "Quarterly Revenue")
    )

    # Kurs akcji
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_df["Date"]),
            y=stock_df["Close"].astype(float),
            name="Share Price"
        ),
        row=1,
        col=1
    )

    # Przychód
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
# 2. Funkcja pomocnicza – pobieranie danych z yfinance
# ============================================================

def get_stock_history(ticker_symbol, period="max"):
    """
    Pobiera dane historyczne dla wybranego tickera z yfinance.
    Zwraca DataFrame z kolumnami: Date, Open, High, Low, Close, Volume, ...
    """
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    hist.reset_index(inplace=True)   # przeniesienie daty do zwykłej kolumny
    return hist


# ============================================================
# 3. Funkcja pomocnicza – web-scraping tabeli przychodów
#    z serwisu Macrotrends (lub podobnej strony)
# ============================================================

def get_revenue_from_macrotrends(url, table_label):
    """
    Pobiera tabelę 'Quarterly Revenue' ze strony Macrotrends.

    url         – adres strony (np. Tesla revenue page)
    table_label – fragment tekstu rozpoznający właściwą tabelę,
                  np. 'Tesla Quarterly Revenue', 'GameStop Quarterly Revenue'
    Zwraca DataFrame z kolumnami: Date, Revenue (float, w mln USD).
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
        raise ValueError("Nie znaleziono tabeli z przychodami.")

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

    # Czyszczenie formatu przychodów: usuwamy $ i przecinki
    revenue_df["Revenue"] = (
        revenue_df["Revenue"]
        .str.replace(r"[$,]", "", regex=True)
        .astype(float)
    )

    # Porządkujemy rosnąco po dacie
    revenue_df = revenue_df.sort_values("Date")
    revenue_df.reset_index(drop=True, inplace=True)

    return revenue_df


# ============================================================
# 4. TESLA (TSLA) – dane z yfinance + revenue z Macrotrends
# ============================================================

# 4.1. Kurs akcji Tesli z yfinance
tesla_stock = get_stock_history("TSLA", period="max")

# 4.2. Web-scraping tabeli z przychodami Tesli
tesla_revenue_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
tesla_revenue = get_revenue_from_macrotrends(
    tesla_revenue_url,
    "Tesla Quarterly Revenue"
)

# (opcjonalnie można przyciąć zakres dat, np. po 2015 roku)
# tesla_stock = tesla_stock[tesla_stock["Date"] >= "2015-01-01"]
# tesla_revenue = tesla_revenue[tesla_revenue["Date"] >= "2015-01-01"]

# 4.3. Wykres Tesli
plot_price_and_revenue(tesla_stock, tesla_revenue, "Tesla (TSLA)")


# ============================================================
# 5. GAMESTOP (GME) – dane z yfinance + revenue z Macrotrends
# ============================================================

# 5.1. Kurs akcji GameStop z yfinance
gme_stock = get_stock_history("GME", period="max")

# 5.2. Web-scraping tabeli z przychodami GameStop
gme_revenue_url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
gme_revenue = get_revenue_from_macrotrends(
    gme_revenue_url,
    "GameStop Quarterly Revenue"
)

# (opcjonalne przycięcie dat)
# gme_stock = gme_stock[gme_stock["Date"] >= "2015-01-01"]
# gme_revenue = gme_revenue[gme_revenue["Date"] >= "2015-01-01"]

# 5.3. Wykres GameStop
plot_price_and_revenue(gme_stock, gme_revenue, "GameStop (GME)")


# ============================================================
# 6. Szybkie podsumowanie danych (przykładowe komendy EDA)
# ============================================================

# Podgląd danych Tesli
print("TESLA STOCK DATA:")
print(tesla_stock.head(), "\n")

print("TESLA REVENUE DATA:")
print(tesla_revenue.head(), "\n")

# Podgląd danych GameStop
print("GME STOCK DATA:")
print(gme_stock.head(), "\n")

print("GME REVENUE DATA:")
print(gme_revenue.head())
