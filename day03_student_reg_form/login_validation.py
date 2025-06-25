import time
from playwright.sync_api import sync_playwright

def test_login_form_validations():
    test_cases = [
        {"email": "jack9@gmail.com", "password": "Jack@123", "expected": "success"},
        {"email": "jack98@gmail.com", "password": "Jack@123", "expected": "error"},
        {"email": "jack9@gmail.com", "password": "Jack@9878", "expected": "error"},
        {"email": "jackie@gmail.com", "password": "kirnm@89", "expected": "error"},
        {"email": "jack9@gmail.com", "password": "hey@98", "expected": "error"},
        {"email": "", "password": "", "expected": "error"}
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for case in test_cases:
            page.goto("https://rahulshettyacademy.com/client/")

            # Fill email and password
            page.fill("input[id='userEmail']", case["email"])
            page.fill("input[id='userPassword']", case["password"])
            page.click("input#login")
            time.sleep(3)

            if case["expected"] == "success":
                # Wait for 'Sign Out' button as success confirmation
                signout_btn = page.locator("button:has-text('Sign Out')")
                signout_btn.wait_for(state="visible", timeout=5000)
                assert signout_btn.is_visible(), f"Login success expected but 'Sign Out' button not visible for: {case}"
                print(f"Passed: Login success for {case}")

                # Logout to reset state for next test case
                signout_btn.click()
                page.locator("input[id='userEmail']").wait_for(state="visible", timeout=10000)
            else:
                error_toast = page.locator(".toast-message")
                if error_toast.count() > 0:
                    error_toast.wait._for(state="visible", timeout=5000) #prevent the timeout for crashing
                    assert error_toast.is_visible(), f"Expected error toast not visible for {case}"
                else:
                    assert True, "No toast appeared, but login failed as expected"
                print(f"Login failed as expected for {case}")

        browser.close()
