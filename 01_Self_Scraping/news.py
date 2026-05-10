import time
import random
from playwright.sync_api import sync_playwright

def close_button(page):
    page.wait_for_selector("text = ×")
    page.click("text =×")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.rtl.lu/news/international")
    page.wait_for_timeout(3000)


    
    page.wait_for_timeout(3000)
    for i in range(1, 5):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(random.randint(1000, 3000))

    news_list = page.locator("div.ContentList_list__MV1_m.ContentList_PageListArchiveA___meKF > div")
    print(news_list.count())

    with page.expect_navigation():
        news_list.nth(3).click()
        page.wait_for_timeout(2500)
        page.wait_for_selector("text = ×")
        page.click("text =×")
        for i in range(1, 3):
            page.mouse.wheel(0, 300)
        page.go_back()
        page.wait_for_timeout(2000)

    page.close()