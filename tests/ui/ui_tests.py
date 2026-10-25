from datetime import datetime
from random import randint

from playwright.sync_api import Page, expect


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    user_email = f'test_{randint(1, 9999)}@email.qa'

    page.type(username_locator, 'Жмышенко Валерий Альбертович')
    page.type(email_locator, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.click('[data-qa-id="register_submit_button"]')
    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)


def test_webtables(page: Page):
    page.goto("https://demoqa.com/webtables")
    page.get_by_role("button", name="Add").click()
    expect(page.locator(".modal-content")).to_be_visible()
    expect(page.get_by_text("Registration Form")).to_be_visible()
    page.get_by_role("textbox", name="First Name").fill("123")
    page.locator("input[placeholder='Last Name']").fill("1234")
    page.get_by_role("textbox", name="name@example.com").fill("vlad@gmail.com")
    page.get_by_role("textbox", name="Age").fill("20")
    page.get_by_role("textbox", name="Salary").fill("150000")
    page.get_by_role("textbox", name="Department").fill("oaoaoao")
    page.get_by_role("button", name="Submit").click()


def test_practice_form(page: Page):
    page.goto("https://demoqa.com/automation-practice-form")
    page.get_by_role("textbox", name="First Name").fill("Vlad")
    page.get_by_role("textbox", name="Last Name").fill("Tretyakov")
    page.get_by_role("textbox", name="name@example.com").fill("vlad@gmail.cum")
    page.get_by_role("radio", name="Male", exact=True).check()
    page.get_by_role("textbox", name="Mobile Number").fill("8950244408")
    assert page.locator("#dateOfBirthInput").get_attribute("value") == datetime.today().strftime("%d %b %Y")
    page.locator("#dateOfBirthInput").click()
    page.locator(".react-datepicker__month-select").select_option("5")
    page.locator(".react-datepicker__year-select").select_option("2007")
    page.get_by_role("gridcell", name="20th").click()
    page.locator("#subjectsInput").fill("e")
    page.get_by_role("option", name="English").click()
    page.get_by_role("checkbox", name="Sports").check()
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("12321123123123")
    page.locator("#state").get_by_role("combobox").click()
    page.get_by_role("option", name="Uttar Pradesh").click()
    page.locator("#city").get_by_role("combobox").click()
    page.get_by_role("option", name="Lucknow").click()
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Thanks for submitting the form")).to_be_visible()
    page.get_by_role("button", name="Close").click()
    expect(page.get_by_role("contentinfo")).to_have_text("© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED.")


def test_activity(page: Page):
    page.goto("https://demoqa.com/radio-button")
    assert page.get_by_role("radio", name="Yes").is_enabled()
    assert page.get_by_role("radio", name="Impressive").is_enabled()
    assert page.get_by_role("radio", name="No").is_disabled()

def test_visible(page: Page):
    page.goto("https://demoqa.com/checkbox")
    assert page.get_by_text('Home', exact=True).is_visible()
    assert not page.get_by_text('Desktop', exact=True).is_visible()

    page.locator(".rc-tree-switcher").click()

    assert page.get_by_text('Home', exact=True).is_visible()
    assert page.get_by_text('Desktop', exact=True).is_visible()


def test_visible_5sec(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")
    expect(page.get_by_role("button", name="Will enable 5 seconds")).to_be_visible()
    expect(page.get_by_role("button", name="Color Change")).to_be_visible()
    expect(page.get_by_role("button", name="Visible After 5 Seconds")).not_to_be_visible()
    expect(page.get_by_role("button", name="Visible After 5 Seconds")).to_be_visible(timeout=5000)


def test_radio_buttons_activity_and_checked_state(page: Page):
    page.goto("https://demoqa.com/radio-button")
    expect(page.get_by_role("radio", name="Yes")).to_be_enabled()
    expect(page.get_by_role("radio", name="Impressive")).to_be_enabled()
    expect(page.get_by_role("radio", name="No")).to_be_disabled()

    page.get_by_role("radio", name="Yes").check()

    expect(page.get_by_role("radio", name="Yes")).to_be_checked()
    expect(page.get_by_role("radio", name="Impressive")).not_to_be_checked()