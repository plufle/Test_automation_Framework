# Automation Framework

This repository contains an automated testing framework built with Python, Pytest, Playwright, and Requests. It supports both UI and API testing and provides comprehensive test reporting using Allure.

## Features

- **UI Testing**: Powered by [Playwright](https://playwright.dev/python/) for fast, reliable, and cross-browser web testing.
- **API Testing**: Uses the `requests` library to interact with RESTful APIs.
- **Reporting**: Integrates directly with [Allure Framework](https://allurereport.org/) for beautiful, detailed test reports.
- **Configuration**: Uses YAML files (`config/config.yaml`) for clean and structured environment configurations.
- **Page Object Model (POM)**: Structure ready for standard Page Object patterns in the `pages/` directory.

## Directory Structure

```text
automation-framework/
├── api/                  # API testing helpers and request handlers
├── config/               # Environment configuration files (e.g., config.yaml)
├── fixtures/             # Reusable testing fixtures and mock data
├── logs/                 # Test execution logs
├── pages/                # Page Object Model (POM) classes for UI tests
├── reports/              # Raw Allure test results generated during execution
├── testdata/             # JSON/CSV or other files used for data-driven testing
├── tests/                # All test execution scripts
│   ├── DashBoard/        # Dashboard API and UI specific test cases
│   └── Login/            # Login specific test cases
├── utils/                # Utility and helper functions
├── .gitignore            # Ignored files and folders for Git
├── conftest.py           # Pytest entrypoint containing shared test fixtures
├── pytest.ini            # Pytest configuration file
├── requirements.txt      # Python dependencies
└── run_tests.ps1         # PowerShell script to execute tests and open reports
```

## Prerequisites

1. **Python 3.8+** installed on your system.
2. **Pip** (Python package installer).
3. **Allure Commandline** installed and added to your system path (to generate and serve the reports).
4. **Node.js** (Optional, but often used to install the Allure CLI).

## Setup Instructions

1. **Create and Activate a Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**
   ```powershell
   playwright install
   ```

4. **Environment Variables**
   Create a `.env` file in the project root directory and add the following email credentials required for OTP login testing:
   ```env
   EMAIL_USER=your-email@example.com
   EMAIL_PASS=your-email-password
   ```

## Running Tests

### Using the Helper Script

The quickest way to run all tests and automatically generate/open the Allure report is to use the provided PowerShell script:

```powershell
.\run_tests.ps1
```

**What the script does:**
1. Cleans up old reports from the `reports/` folder.
2. Runs `pytest` and saves new Allure results into `reports/`.
3. Compiles the results into an interactive HTML report in `allure-report/`.
4. Starts a local webserver and opens the report in your default browser.

### Manually via CLI

If you want to run specific tests or skip generating the report immediately:

- **Run all tests:**
  ```bash
  pytest
  ```

- **Run only UI tests:**
  ```bash
  pytest tests/DashBoard/test_dashboard_ui.py
  ```

- **Run only API tests:**
  ```bash
  pytest tests/DashBoard/test_dashboard_api.py
  ```

- **Run tests and collect Allure results manually:**
  ```bash
  pytest --alluredir=reports/
  allure serve reports/
  ```

## Writing Tests

- **UI Tests**: Add new UI tests to the `tests/DashBoard/` folder using Playwright. Use the standard Page Object Model patterns via `pages/`. Tests are now automatically configured to take screenshots, videos, and Playwright traces on failure.
- **API Tests**: Add new API tests using the pre-authenticated `api_context` fixture.

## Debugging Failures

By default, the framework retains screenshots, videos, and full Playwright traces for any failed tests. 
When viewing the Allure report, you can inspect the attachments on failed steps.
To manually inspect a trace, use the Playwright CLI:
```bash
playwright show-trace test-results/<trace-zip-file>
```
