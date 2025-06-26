import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

def test_login():
    test_data = [
        {"email": "jack9@gmail.com", "password": "Jack@123", "expected": "success"},
        {"email": "jack@gmail.comm", "password": "jack@0989", "expected": "error"}
    ]

    # screenshots folder validation - it will be helpful to validate previous success/error message
    base_dir = "screenshots"
    # Create unique, clean filename with Date and Time: Ex 20250626-1803
    timestamp_run = datetime.now().strftime("run_%Y%m%d_%H%M")
    screenshot_dir = os.path.join(base_dir, timestamp_run)
    os.makedirs(screenshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for data in test_data:
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://rahulshettyacademy.com/client/")

            # Fill login form
            page.fill("input#userEmail", data["email"])
            page.fill("input#userPassword", data["password"])
            page.click("input#login")

            timestamp = datetime.now().strftime("run_%Y%m%d_%H%M")

            email_clean = re.sub(r'\W+', '_', data["email"])
            base_filename = f"{email_clean}_{timestamp}"

            try:
                # Wait for toast and get message
                toast_locator = page.locator("div[aria-label]")
                toast_locator.wait_for(state="visible", timeout=5000)
                message = toast_locator.text_content()
                print(f"🔍 Login with {data['email']} ➤ UI Message: {message}")

                # Save screenshot
                page.screenshot(path=os.path.join(screenshot_dir, base_filename + ".png"))

                # ✅ Validate login behavior
                if data["expected"] == "success":
                    assert "Login Successfully" in message, f"Expected success, got: {message}"
                    assert "/dashboard" in page.url, f"Did not navigate to dashboard, got: {page.url}"
                    storage = context.storage_state()
                    assert "token" in str(storage), "Token missing after successful login"
                else:
                    assert "Incorrect" in message or "wrong" in message.lower(), f"Expected error message, got: {message}"
                    assert "/client" in page.url, f"Failed login should stay on login page, got: {page.url}"
                    storage = context.storage_state()
                    assert "token" not in str(storage), "Token should not exist after failed login"

            except Exception as e:
                # Save screenshot on failure
                page.screenshot(path=os.path.join(screenshot_dir, base_filename + "_error.png"))
                raise AssertionError(f"Test Failed for {data['email']}: {str(e)}")

            context.close()

        browser.close()
