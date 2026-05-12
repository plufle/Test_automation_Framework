# Automation Framework

This repository contains an automated testing framework built with Python, Pytest, Playwright, and Requests. It supports both UI and API testing and provides comprehensive test reporting using Allure.

## Features

- **UI Testing**: Powered by [Playwright](https://playwright.dev/python/) for fast, reliable, and cross-browser web testing.
- **API Testing**: Uses Playwright's API request context for authenticated RESTful API testing.
- **Reporting**: Integrates directly with [Allure Framework](https://allurereport.org/) for beautiful, detailed test reports.
- **Configuration**: Uses YAML files (`config/config.yaml`) + `.env` for clean and structured environment configurations.
- **Page Object Model (POM)**: All UI interaction is encapsulated in `pages/` — locators and actions only, no assertions.
- **Service Layer**: API calls are wrapped in `services/` to keep tests focused on validation.
- **Reusable Fixtures**: Authentication, API context, reporting, and config are managed via modular fixtures in `fixtures/`.

## Directory Structure

```text
automation-framework/
├── config/                    # Environment configuration (YAML + .env)
│   ├── __init__.py
│   └── config.yaml
├── fixtures/                  # Reusable pytest fixtures (modular)
│   ├── __init__.py
│   ├── api_fixtures.py        # Authenticated API request context
│   ├── auth_fixtures.py       # Session-scoped login & storage state
│   ├── config_fixtures.py     # YAML + env config loader
│   └── reporting_fixtures.py  # Allure screenshot/video on failure
├── pages/                     # Page Object Model classes (locators + actions ONLY)
│   ├── __init__.py
│   ├── base_page.py           # Common actions shared by all pages
│   ├── dashboard_page.py      # Dashboard-specific locators & helpers
│   └── login_page.py          # Login flow locators & actions
├── services/                  # Business-logic wrappers (API clients, etc.)
│   ├── __init__.py
│   └── api_service.py         # DashboardAPIService — wraps all API calls
├── test_data/                 # Constants & data-driven test inputs
│   ├── __init__.py
│   └── dashboard_data.py      # URL patterns, card titles, nav items
├── tests/                     # All test execution scripts
│   ├── __init__.py
│   ├── api/                   # API-only tests
│   │   ├── __init__.py
│   │   └── test_dashboard_api.py
│   └── ui/                    # UI (browser) tests
│       ├── __init__.py
│       ├── test_dashboard_ui.py
│       └── test_login.py
├── utils/                     # Utility and helper functions
│   ├── __init__.py
│   ├── email_otp.py           # IMAP-based OTP fetcher
│   └── waits.py               # Reusable wait strategies
├── .gitignore
├── conftest.py                # Pytest entrypoint — registers fixture plugins
├── pytest.ini                 # Pytest configuration & custom markers
├── requirements.txt           # Python dependencies
└── run_tests.ps1              # PowerShell script to execute tests and open reports
```

## Architecture Principles

| Principle | Implementation |
|-----------|---------------|
| **Separation of concerns** | `tests/` → assertions only · `pages/` → locators + actions · `services/` → API wrappers · `fixtures/` → setup/teardown |
| **No assertions in Page Objects** | Pages return locators/values; tests make the assertions |
| **DRY test data** | All constants live in `test_data/` — tests import, never hardcode |
| **Service layer** | `DashboardAPIService` centralises HTTP calls; tests validate responses |
| **Smart fallback locators** | `DashboardPage.get_metric_card()` auto-falls-back when primary selector misses |

## Prerequisites

1. **Python 3.10+** installed on your system.
2. **Pip** (Python package installer).
3. **Allure Commandline** installed and added to your system path.

## Setup Instructions

1. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   # .\venv\Scripts\activate       # Windows PowerShell
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**
   ```bash
   playwright install
   ```

4. **Environment Variables**
   Create a `.env` file in the project root:
   ```env
   EMAIL_USER=your-email@example.com
   EMAIL_PASS=your-email-password
   ```

## Running Tests

### All tests
```bash
pytest
```

### Only UI tests
```bash
pytest tests/ui/
```

### Only API tests
```bash
pytest tests/api/
```

### By marker
```bash
pytest -m ui
pytest -m api
pytest -m smoke
```

### With Allure report
```bash
pytest --alluredir=reports/
allure serve reports/
```

### Using the helper script (Windows)
```powershell
.\run_tests.ps1
```

## Writing Tests

- **UI Tests**: Add to `tests/ui/`. Use page objects from `pages/` and data from `test_data/`. Never put raw locators in test files.
- **API Tests**: Add to `tests/api/`. Create service methods in `services/api_service.py` for new endpoints; tests call services and assert.
- **New Pages**: Inherit from `BasePage`. Keep only locators and actions — no assertions.

## Debugging Failures

The framework retains screenshots, videos, and full Playwright traces for any failed tests.

```bash
# View a trace interactively
playwright show-trace test-results/<trace-zip-file>
```
