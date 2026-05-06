# Assaia Contact Form – Captcha Validation Tests

![CI](https://github.com/<your-username>/CaptchaTask/actions/workflows/ci.yml/badge.svg)

Automated UI tests verifying that the **"Get in touch"** form on [assaia.com](https://www.assaia.com/) blocks submission when reCAPTCHA is not completed.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [pytest](https://docs.pytest.org/) | Test runner |
| [allure-pytest](https://docs.qameta.io/allure/) | Test reporting |
| [Poetry](https://python-poetry.org/) | Dependency management |

---

## Project Structure

```
CaptchaTask/
├── pages/
│   ├── home_page.py          # HomePage POM (navigates to site, accepts cookies)
│   └── contact_form_page.py  # ContactFormPage POM (fills form, asserts captcha error)
├── tests/
│   ├── conftest.py           # Fixtures: browser, context, page, contact_form
│   └── test_contact_form.py  # Parametrized captcha validation test
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── pyproject.toml
└── README.md
```

---

## Setup

```bash
poetry install
poetry run playwright install chromium
```

## Run Tests

```bash
poetry run pytest tests/test_contact_form.py
```

## View Allure Report

```bash
allure serve allure-results
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-change`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request
