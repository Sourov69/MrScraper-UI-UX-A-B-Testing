from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # going to the ecommerce site
    page.goto("https://www.ebay.com/")
    page.wait_for_timeout(3000)

    # Enter search item into searchbox
    page.get_by_placeholder(text="Search for anything").fill("vans")
    page.get_by_placeholder(text="Search for anything").press("Enter")
    page.wait_for_timeout(3000)

    items = page.locator("#srp-river-results > ul > li")

    for i in range(1, 6):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(2000)
    for i in items:
        print(i)
    page.close()

