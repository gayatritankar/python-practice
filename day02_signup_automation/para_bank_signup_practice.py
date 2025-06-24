import time

from playwright.sync_api import sync_playwright

def test_para_bank_signup():
    unique_username = f"priya{int(time.time())}" #time.time(), Returns the current Unix timestamp

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        page.goto("https://parabank.parasoft.com/parabank/register.htm")


        page.fill("input[id='customer.firstName']", "Priya")
        page.fill("input[id='customer.lastName']", "Shah")
        page.fill("input[id='customer.address.street']", "Madhapur")
        page.fill("input[name='customer.address.city']", "Hyderabad")
        page.fill("input[name='customer.address.state']", "Telangana")
        page.fill("input[name='customer.address.zipCode']", "500081")
        page.fill("input[name='customer.phoneNumber']", "9345623098")
        page.fill("input[name='customer.ssn']", "84567898")

        page.fill("input[name='customer.username']", unique_username)
        page.fill("input[name='customer.password']", "Priya@0000")
        page.fill("input[name='repeatedPassword']", "Priya@0000")

        time.sleep(3)

        page.click("input[value='Register']")

        page.wait_for_url("**/register.htm", timeout=10000)

        #Validate Welcome message
        welcome_text = page.text_content("#rightPanel h1")
        extracted_username = welcome_text.replace("Welcome", "").strip()
        success_msg = page.inner_text("#rightPanel p")

        assert welcome_text.startswith("Welcome"), "Welcome message not found"
        assert extracted_username.lower() == unique_username.lower(), "Username mismatch"
        assert "successfully" in success_msg.lower(), "Success message not displayed"

        print("Signup successful and verified.")
        print("Welcome message:", welcome_text)

        time.sleep(5)
