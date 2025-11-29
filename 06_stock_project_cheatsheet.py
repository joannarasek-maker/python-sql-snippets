# ============================================================
#  PYTHON PROJECT FOR DATA SCIENCE – CHEAT SHEET
#  Extracting and visualizing stock data (Tesla & GameStop)
# ============================================================

# (opcjonalnie – tylko przy pracy lokalnej)
# !pip install yfinance
# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
