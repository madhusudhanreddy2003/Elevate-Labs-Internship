# news_scraper.py
"""
Task 3: Web Scraper for News Headlines

Features:
- Scrape top headlines from multiple news websites
- Filter only top N headlines (default = 10)
- CLI menu to choose site, format, and options
- Save headlines to .txt
- Export headlines to PDF using FPDF
- Filenames include date and time
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# --------------- CONFIG ---------------

SITES = {
    "bbc": "https://www.bbc.com/news",
    "reuters": "https://www.reuters.com/world/",
    "aljazeera": "https://www.aljazeera.com/news/",
}

DEFAULT_TOP_N = 10
OUTPUT_DIR = "outputs"  # all files saved here


# --------------- HELPERS ---------------

def timestamp_str():
    """Return current timestamp as string: YYYY-MM-DD_HH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def human_time():
    """Human readable time string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_html(url):
    """Fetch HTML from a URL with basic error handling."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"Failed to fetch {url}. Status code:", resp.status_code)
            return None
    except Exception as e:
        print(f"Error while fetching {url}: {e}")
        return None


def extract_headlines(html, max_items=DEFAULT_TOP_N):
    """
    Extract headlines from HTML.
    Strategy: find all <h1> and <h2> tags, collect unique non-trivial texts.
    """
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all(["h1", "h2"])

    headlines = []
    seen = set()
    for tag in tags:
        text = tag.get_text(strip=True)
        if text and len(text) > 5:
            if text not in seen:
                seen.add(text)
                headlines.append(text)
        if len(headlines) >= max_items:
            break
    return headlines


def save_to_txt(site_name, headlines):
    ensure_output_dir()
    ts = timestamp_str()
    filename = os.path.join(OUTPUT_DIR, f"{site_name}_headlines_{ts}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"News Headlines from {site_name} - Generated at {human_time()}\n")
        f.write("-" * 80 + "\n\n")
        for i, h in enumerate(headlines, start=1):
            f.write(f"{i}. {h}\n")
    print(f"[TXT] Saved to: {filename}")


def save_to_pdf(site_name, headlines):
    ensure_output_dir()
    ts = timestamp_str()
    filename = os.path.join(OUTPUT_DIR, f"{site_name}_headlines_{ts}.pdf")

    try:
        from fpdf import FPDF
    except ImportError:
        print("[PDF] fpdf is not installed. Run: pip install fpdf")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"News Headlines - {site_name.title()}", ln=True)

    # Timestamp
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Generated at: {human_time()}", ln=True)
    pdf.ln(4)

    # Headlines
    pdf.set_font("Arial", "", 12)
    for i, h in enumerate(headlines, start=1):
        pdf.multi_cell(0, 7, f"{i}. {h}")
        pdf.ln(1)

    pdf.output(filename)
    print(f"[PDF] Saved to: {filename}")


def scrape_site(site_key, top_n=DEFAULT_TOP_N, save_txt=True, save_pdf=False):
    site_key = site_key.lower()
    if site_key not in SITES:
        print("Unknown site:", site_key)
        return

    url = SITES[site_key]
    print(f"\nScraping {site_key} -> {url}")
    html = fetch_html(url)
    if not html:
        print("No HTML fetched. Skipping.")
        return

    headlines = extract_headlines(html, max_items=top_n)
    if not headlines:
        print("No headlines found.")
        return

    print(f"\nTop {len(headlines)} headlines from {site_key}:")
    for i, h in enumerate(headlines, start=1):
        print(f"{i}. {h}")

    if save_txt:
        save_to_txt(site_key, headlines)
    if save_pdf:
        save_to_pdf(site_key, headlines)


def scrape_all_sites(top_n=DEFAULT_TOP_N, save_txt=True, save_pdf=False):
    for site in SITES:
        scrape_site(site, top_n=top_n, save_txt=save_txt, save_pdf=save_pdf)


# --------------- CLI MENU ---------------

def get_int(prompt, default=None):
    s = input(prompt).strip()
    if not s and default is not None:
        return default
    try:
        return int(s)
    except ValueError:
        print("Invalid number. Using default:", default)
        return default


def choose_output_format():
    print("\nChoose output format:")
    print("1. Save as TXT only")
    print("2. Save as PDF only")
    print("3. Save as both TXT and PDF")
    choice = input("Enter choice (1-3): ").strip()
    if choice == "1":
        return True, False
    elif choice == "2":
        return False, True
    elif choice == "3":
        return True, True
    else:
        print("Invalid choice. Defaulting to TXT only.")
        return True, False


def choose_site():
    print("\nAvailable news sites:")
    keys = list(SITES.keys())
    for i, k in enumerate(keys, start=1):
        print(f"{i}. {k}  ({SITES[k]})")
    choice = input("Choose site (number) or press Enter for 'bbc': ").strip()
    if not choice:
        return "bbc"
    try:
        idx = int(choice)
        if 1 <= idx <= len(keys):
            return keys[idx - 1]
    except ValueError:
        pass
    print("Invalid choice. Using default: bbc")
    return "bbc"


def main_menu():
    while True:
        print("\n==============================")
        print("  News Headlines Scraper CLI ")
        print("==============================")
        print("1. Scrape a single website")
        print("2. Scrape all websites")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            site = choose_site()
            top_n = get_int(f"How many top headlines? (default {DEFAULT_TOP_N}): ", default=DEFAULT_TOP_N)
            save_txt, save_pdf = choose_output_format()
            scrape_site(site, top_n=top_n, save_txt=save_txt, save_pdf=save_pdf)

        elif choice == "2":
            top_n = get_int(f"How many top headlines per site? (default {DEFAULT_TOP_N}): ", default=DEFAULT_TOP_N)
            save_txt, save_pdf = choose_output_format()
            scrape_all_sites(top_n=top_n, save_txt=save_txt, save_pdf=save_pdf)

        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main_menu()
