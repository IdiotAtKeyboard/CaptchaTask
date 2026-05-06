from playwright.sync_api import Page, expect


class ContactFormPage:

    def __init__(self, page: Page):
        self.page = page
        self._name_input = page.locator("#name")
        self._email_input = page.locator("#email")
        self._company_input = page.locator("#Company")
        self._submit_btn = page.locator("button.btn_primary", has_text="Submit")
        self._captcha_error = page.locator(".g-recaptcha-error").first

    def fill_form(self, name: str, email: str, company: str):
        self._name_input.fill(name)
        self._email_input.fill(email)
        self._company_input.fill(company)

    def submit(self):
        self._submit_btn.click()

    def assert_captcha_error_visible(self):
        # Scroll captcha into view so it appears in the final screenshot
        self._captcha_error.scroll_into_view_if_needed()
        # Assert the reCAPTCHA container has the error class applied
        expect(self._captcha_error).to_be_visible(timeout=5000)
