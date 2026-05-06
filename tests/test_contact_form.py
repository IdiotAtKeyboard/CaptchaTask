import allure
import pytest
from pages.contact_form_page import ContactFormPage


TEST_DATA = [
    pytest.param("Alice Johnson", "alice@example.com", "Acme Corp", id="alice-acme-corp"),
    pytest.param("Bob Smith", "bob@example.com", "TechStart Inc", id="bob-techstart"),
]


@allure.feature("Contact Form")
@allure.story("Captcha Validation")
@pytest.mark.parametrize("name,email,company", TEST_DATA)
def test_contact_form_captcha_validation(contact_form: ContactFormPage, name: str, email: str, company: str):
    """Verify that submitting the 'Get in touch' form without solving captcha shows an error."""

    # Given the contact form is open
    with allure.step(f"When I fill in Name='{name}', Email='{email}', Company='{company}'"):
        contact_form.fill_form(name, email, company)

    # And I click the Submit button without solving the captcha
    with allure.step("And I click the Submit button without solving the captcha"):
        contact_form.submit()

    # Then a captcha error should be visible on the form
    with allure.step("Then a captcha error should be visible on the form"):
        contact_form.assert_captcha_error_visible()
