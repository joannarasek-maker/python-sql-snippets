"""
IBM: Python for Data Science, AI & Development — Cheat Sheet (Requests / HTTP / APIs)

What’s inside:
- Install + imports
- HTTP basics (URL, request/response, status codes)
- requests: GET / headers / encoding / text / json()
- Downloading files (txt) and images (PNG) safely
- GET with URL parameters
- POST requests (form data)
- Simple, reusable helpers (timeouts, error handling)

Run:
    python 08_python_ds_ai_development_cheatsheet.py

Notes:
- In some learning platforms (Skills Network/Coursera), internet access may be restricted.
- If a request fails, check your environment and network permissions.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from PIL import Image


# =========================
# 0) Install (copy/paste)
# =========================
# pip install requests
# pip install pillow


# =========================
# 1) Quick HTTP recap
# =========================
# URL = scheme + base/domain + route/path (+ optional query params)
# Example:
#   https://www.ibm.com/           -> scheme=https, domain=www.ibm.com, route=/
# Request -> Response
# Common methods: GET (retrieve), POST (submit), PUT (update), DELETE (delete)


# =========================
# 2) Safe requests helpers
# =========================
DEFAULT_TIMEOUT = 15  # seconds


def safe_get(url: str, *, params: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    """GET with timeout + raise_for_status() (clean error messages)."""
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"GET failed for {url}. Details: {e}") from e


def safe_post(url: str, *, data: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    """POST with timeout + raise_for_status(). Sends data as form-encoded by default."""
    try:
        r = requests.post(url, data=data, timeout=timeout)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"POST failed for {url}. Details: {e}") from e


def save_bytes(content: bytes, filepath: str | Path) -> Path:
    """Save response content to file (binary-safe)."""
    path = Path(filepath).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


# =========================
# 3) GET example: IBM homepage
# =========================
def example_get_ibm() -> None:
    url = "https://www.ibm.com/"
    r = safe_get(url)

    print("\n=== GET IBM ===")
    print("Status code:", r.status_code)

    # Request headers (what you sent)
    print("\nRequest headers:")
    print(r.request.headers)

    # GET usually has no request body
    print("\nRequest body:", r.request.body)

    # Response headers (what server returns)
    header = r.headers
    print("\nResponse headers (snippet):")
    print({k: header.get(k) for k in ["Date", "Content-Type", "Content-Length", "Server"] if k in header})

    print("\nEncoding:", r.encoding)
    print("\nFirst 120 chars of HTML:")
    print(r.text[:120])


# =========================
# 4) Download an image (PNG) + open in Pillow
# =========================
def example_download_image() -> None:
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/IDSNlogo.png"
    r = safe_get(url)

    print("\n=== Download image ===")
    print("Content-Type:", r.headers.get("Content-Type"))

    out_path = save_bytes(r.content, Path(os.getcwd()) / "image.png")
    print("Saved to:", out_path)

    # Open with Pillow
    img = Image.open(out_path)
    print("Image size:", img.size, "| mode:", img.mode)
    # If you want to display in notebook: display(img)
    # If running locally, you can preview:
    # img.show()


# =========================
# 5) Download a text file (txt)
# =========================
def example_download_text_file() -> None:
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/data/Example1.txt"
    r = safe_get(url)

    print("\n=== Download text file ===")
    out_path = save_bytes(r.content, Path(os.getcwd()) / "example1.txt")
    print("Saved to:", out_path)

    # Read back (text)
    text = out_path.read_text(encoding="utf-8", errors="replace")
    print("\nFirst 200 chars:")
    print(text[:200])


# =========================
# 6) GET with URL parameters (httpbin)
# =========================
def example_get_with_params() -> None:
    base_url = "http://httpbin.org/get"
    payload = {"name": "Joseph", "ID": "123"}  # query params

    r = safe_get(base_url, params=payload)

    print("\n=== GET with params (httpbin) ===")
    print("Final URL:", r.url)
    print("Request body:", r.request.body)  # still None for GET
    print("Status code:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))

    data = r.json()
    print("\nJSON keys:", list(data.keys()))
    print("args:", data.get("args"))  # {'ID': '123', 'name': 'Joseph'}


# =========================
# 7) POST request (httpbin)
# =========================
def example_post_form() -> None:
    url_post = "http://httpbin.org/post"
    payload = {"name": "Joseph", "ID": "123"}

    r = safe_post(url_post, data=payload)

    print("\n=== POST form data (httpbin) ===")
    print("POST request URL:", r.url)
    print("POST request body:", r.request.body)  # will contain form-encoded data
    print("Status code:", r.status_code)

    data = r.json()
    print("\nform:", data.get("form"))  # {'ID': '123', 'name': 'Joseph'}


# =========================
# 8) Minimal “main” runner
# =========================
def main() -> None:
    # Uncomment what you want to run:
    example_get_ibm()
    example_get_with_params()
    example_post_form()
    example_download_image()
    example_download_text_file()


if __name__ == "__main__":
    main()
