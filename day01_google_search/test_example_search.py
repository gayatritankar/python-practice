from playwright.sync_api import sync_playwright

def test_example_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.python.org/")

        page.fill("input[name='q']", "Python")
        page.click("button[type='submit']")

        page.screenshot(path="python_search.png")
        browser.close()
