"""
HTTP requests & basic web scraping cheat sheet.

Covers:
- requests: GET, query parameters, headers, JSON
- simple API example (GitHub public API)
- creating a pandas DataFrame from JSON
- basic web scraping with BeautifulSoup (finding tags, links, text)
- important notes: robots.txt, polite scraping
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

# ============================================
# 1. Basic GET request
# ============================================

url = "https://api.github.com"  # public GitHub API root

response = requests.get(url)

print("Status code:", response.status_code)  # 200 = OK
print("Response headers:")
print(response.headers)

# Raw text body (for HTML / plain text)
print("First 300 chars of response.text:")
print(response.text[:300])

# If server returns JSON, use .json()
data_root = response.json()
print("Type of data_root:", type(data_root))
print("Keys in root JSON:", list(data_root.keys()))

# ============================================
# 2. GET with query parameters
# ============================================

# Example: list public events from GitHub API
events_url = "https://api.github.com/events"

params = {
    "per_page": 10  # how many results we want
}

events_response = requests.get(events_url, params=params)
print("Events status code:", events_response.status_code)

events_json = events_response.json()
print("Events JSON type:", type(events_json))  # usually list[dict]

# Create DataFrame from list of dicts
df_events = pd.DataFrame(events_json)

print("df_events.head():")
print(df_events.head())

# Select a few interesting columns (if they exist)
cols = [c for c in ["id", "type", "created_at"] if c in df_events.columns]
print("Selected columns:")
print(df_events[cols].head())

# ============================================
# 3. Error handling pattern for requests
# ============================================

try:
    r = requests.get("https://api.github.com/invalid-endpoint", timeout=10)
    r.raise_for_status()  # will raise HTTPError for bad status
except requests.exceptions.HTTPError as e:
    print("HTTP error:", e)
except requests.exceptions.RequestException as e:
    # covers all other request-related errors
    print("Request error:", e)

# ============================================
# 4. Basic web scraping with BeautifulSoup
# ============================================

"""
IMPORTANT:
- Only scrape pages that allow it (check robots.txt, terms of service).
- Keep requests rare (no loops with hundreds of rapid requests).
- This example uses a public site (IBM) as a demo.
"""

html_url = "https://www.ibm.com"
html_text = requests.get(html_url).text

# Create BeautifulSoup object
soup = BeautifulSoup(html_text, "html.parser")

# 4.1 Find the first <title> tag
title_tag = soup.find("title")
print("Page <title> tag:", title_tag)
print("Page title text:", title_tag.get_text(strip=True) if title_tag else None)

# 4.2 Find all links (<a> tags)
links = soup.find_all("a")

print(f"Found {len(links)} <a> tags. First 10 hrefs:")

for link in links[:10]:
    href = link.get("href")
    text = link.get_text(strip=True)
    print("href:", href, "| text:", text)

# 4.3 Using CSS selectors (select)
# Example: select all <a> inside a <nav> (may be empty if structure differs)
nav_links = soup.select("nav a")
print("nav_links count:", len(nav_links))

for link in nav_links[:5]:
    print("NAV href:", link.get("href"), "| text:", link.get_text(strip=True))

# 4.4 Extracting text from a specific element (if present)
# Example: first <p> paragraph
first_p = soup.find("p")
if first_p:
    print("First <p> text snippet:")
    print(first_p.get_text(strip=True)[:200])

# ============================================
# 5. From scraped data to DataFrame (toy example)
# ============================================

"""
We build a tiny DataFrame from the first N links:
- link_text
- href
"""

records = []
for link in links[:20]:
    records.append(
        {
            "link_text": link.get_text(strip=True),
            "href": link.get("href"),
        }
    )

df_links = pd.DataFrame(records)
print("df_links:")
print(df_links.head())

# ============================================
# 6. Polite scraping checklist (comments only)
# ============================================

"""
Polite scraping checklist:

1. Check robots.txt
   Example: https://www.ibm.com/robots.txt

2. Respect the site's terms of service.

3. Limit request rate:
   - add delays (time.sleep(...)) in loops
   - avoid large-scale scraping with many pages

4. Only collect data you are allowed to use and store.

5. For real projects, log what you download and from where.
"""
