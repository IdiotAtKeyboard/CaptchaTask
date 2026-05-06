from playwright.sync_api import Page


class HomePage:
    URL = "https://www.assaia.com/"

    def __init__(self, page: Page):
        self.page = page
        self._get_in_touch_btn = page.locator(".btn_label", has_text="Get in touch").first
        self._accept_cookies_btn = page.locator("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        if self._accept_cookies_btn.is_visible():
            self._accept_cookies_btn.click()

    def click_get_in_touch(self):
        self._get_in_touch_btn.click()
        self.page.locator("#wf-form-test-new-cta-form").wait_for(state="visible")
