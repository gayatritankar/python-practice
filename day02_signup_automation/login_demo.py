from playwright.sync_api import sync_playwright

def test_signup_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.heroku.com/")

        page.click("text=Sign Up")

        page.fill("input[id='first_name']", "Gayatri")
        page.fill("input[id='last_name']", "Tankar")
        page.fill("input[id='email']", "gayatri@gmail.com")
        page.fill("input[id='company']", "Amazon")

        page.wait_for_selector('#self_declared_country')
        page.select_option("#self_declared_country", "India")

        page.click("input[id='receive_newsletter_choice']")

        page.click("input[type='submit']")

        browser.close()


