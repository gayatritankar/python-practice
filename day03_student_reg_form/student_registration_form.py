import time

from playwright.sync_api import sync_playwright

def test_student_registration_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demoqa.com/automation-practice-form")

        page.fill("input[id = 'firstName']", "Karan")
        page.fill("input[id='lastName']", "Shah")
        page.fill("input[id='userEmail']", "karan01@ymail.com")
        page.click("input#gender-radio-1", force=True)
        page.fill("input[id='userNumber']", "8762345091")
        #open the calendar
        page.click("#dateOfBirthInput")  #id, so use # as css selector
        #select year
        page.click("#dateOfBirthInput")
        page.select_option(".react-datepicker__year-select", "1978")
        page.select_option(".react-datepicker__month-select", "0")  # January
        page.click(".react-datepicker__day--011:not(.react-datepicker__day--outside-month)")
        page.fill("input[id='subjectsInput']", "Computer Science")
        page.keyboard.press("Enter")
        page.click("#hobbies-checkbox-1", force=True)
        page.click("#hobbies-checkbox-2",   force=True)
        page.set_input_files("input[id='uploadPicture']", "C:/Users/DELL/Downloads/anime.jpg")
        page.fill("textarea[id='currentAddress']", "HitechCity")
        page.click("#state")  # open the dropdown
        page.get_by_text("Haryana", exact=True).click()  # select Haryana
        page.click("#city")  # open city dropdown
        page.get_by_text("Karnal", exact=True).click()  # select Karnal

        page.locator("#submit").scroll_into_view_if_needed()
        time.sleep(10)



