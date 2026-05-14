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

    items = page.locator("ul.srp-results.srp-grid.clearfix > li")
    count = items.count()

    for i in range(1, 5):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(2000)
    
    print("total_items: ", count)

    
    for i in range(1, 5):

        with context.expect_page() as new_page_info:
            items.nth(i).click()

        new_page = new_page_info.value
        page.wait_for_timeout(3000)

        for i in range(1, 3):
            new_page.mouse.wheel(0, 400)
            new_page.wait_for_timeout(1500)
        
        new_page.close()


    # ecommerce_product_detail_page_html = new_page.content()
    # with open("ecommerce_product_detail_page_html.html", "w", encoding="utf-8") as f:
    #     f.write(ecommerce_product_detail_page_html)
    # page.go_back()
    # page.wait_for_timeout(2000)

    page.close()

