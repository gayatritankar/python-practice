import time
import os
from playwright.sync_api import sync_playwright

test_data = [
    {"email": "jack9@gmail.com", "password": "Jack@123", "expected": "success"},
    {"email": "jack9gmail.com", "password": "Jack@123", "expected": "error"},
    {"email": "", "password": "Jack@123", "expected": "error"},
    {"email": "jack9@gmail.com", "password": "", "expected": "error"},
    {"email": "", "password": "", "expected": "error"},
    {"email": "wrong@email.com", "password": "wrongpass", "expected": "error"},
]

def take_screenshot(page, data):
    timestamp = str(int(time.time()))
    email = data['email'] if data['email'] else 'empty'
    safe_email = email.replace('@', '_at_').replace('.', '_')
    filename = f"{safe_email}_{timestamp}.png"
    path = os.path.join("screenshots", filename)
    page.screenshot(path=path)
    print(f"📸 Screenshot saved: {path}")

def run_all_logins():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/client")
        page.wait_for_selector("input#userEmail")

        for data in test_data:
            print(f"\n🔍 Testing: {data}")
            page.fill("input#userEmail", data["email"])
            page.fill("input#userPassword", data["password"])
            page.click("input#login")

            if data["expected"] == "success":
                try:
                    page.wait_for_selector("div.card", timeout=5000)
                    print("✅ Login successful as expected.")
                except:
                    print("❌ Expected success, but login failed.")
                    take_screenshot(page, data)

                page.goto("https://rahulshettyacademy.com/client")
                page.wait_for_selector("input#userEmail")

            else:
                error_found = False
                for _ in range(6):
                    # Try various ways to get the error
                    toast = page.query_selector("div.toast-message")
                    inline_errors = page.query_selector_all("div[style*='color: rgb(220, 53, 69)'], label, span")

                    if toast:
                        msg = toast.inner_text().strip()
                        print(f"⚠️ Toast error: {msg}")
                        error_found = True
                        break

                    for err in inline_errors:
                        text = err.inner_text().strip()
                        if text and any(word in text.lower() for word in ["required", "valid", "email", "password"]):
                            print(f"⚠️ Inline error: {text}")
                            error_found = True
                            break

                    if error_found:
                        break

                    time.sleep(1)

                if not error_found:
                    print("❌ Expected error, but no error message shown.")

                take_screenshot(page, data)
                page.goto("https://rahulshettyacademy.com/client")
                page.wait_for_selector("input#userEmail")

        print("\n✅ All test cases executed in a single browser session.")
        print("📌 Close the browser window manually when done.")
