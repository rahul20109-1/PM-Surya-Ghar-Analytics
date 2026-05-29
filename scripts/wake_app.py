from playwright.sync_api import sync_playwright

URL = "https://pm-surya-ghar-analytics.streamlit.app/bottleneck_analysis"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle", timeout=120000)

    # Wait a bit so Streamlit fully loads
    page.wait_for_timeout(15000)

    print("App visited successfully")

    browser.close()
