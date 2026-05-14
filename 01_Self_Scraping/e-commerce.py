from playwright.sync_api import sync_playwright
import pandas as pd
import random 
from bs4 import BeautifulSoup


# Product Data container
product_data = []

# function for handling error in emplty page cases
def safe_text(tag, default=""):
    return tag.get_text(strip=True) if tag else default

# Product info extracting function
def extract_product_details(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    product_vars_details = {}
    product_vars = soup.select(".vim.x-sku")
    for var in product_vars:
        option_name = safe_text(var.select_one(".btn__cell"))
        options = [safe_text(option) for option in var.select("div.listbox__option")]
        product_vars_details[option_name] = options


    product_details = {
        "product_name" : safe_text(soup.select_one(".x-item-title__mainTitle")),

        "product_price" : safe_text(soup.select_one(".x-price-primary")),

        "product_condition" : safe_text(soup.select_one("div.x-item-condition-text")),
        "product_vars_details" : product_vars_details,

        "seller_name" : safe_text(soup.select_one(".x-sellercard-atf__info__about-seller a")),

        "seller_review" : safe_text(soup.select_one(".x-sellercard-atf__data-item-wrapper > div:nth-child(1)")),
        
        "seller_profile" : soup.select_one(".x-sellercard-atf__info__about-seller a").get('href')
            
    }
    
    return product_details


# Playwright Run browser Automation
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

    # Collecting 20 product data
    products_20 = list(range(1, 20))

    for i in range(len(products_20)):
        with context.expect_page() as new_page_info:

            # select a random product index
            product_index = random.choice(products_20)
            # remove that index from list not beingh selected this index again
            products_20.remove(product_index)
            items.nth(product_index).click()

        new_page = new_page_info.value
        new_page.wait_for_timeout(3000)

        for i in range(1, 3):
            new_page.mouse.wheel(0, 400)
            new_page.wait_for_timeout(1500)
        
        # Extract product details
        product_data.append(
            extract_product_details(new_page.content())
        )

        new_page.close()
        page.wait_for_timeout(3000)



    page.close()

print(product_data)

df = pd.DataFrame(product_data)
df.to_excel("ebay_vans_products.xlsx", sheet_name="vans_item", index=False)
print(df)
