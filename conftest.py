import pytest
from playwright.sync_api import sync_playwright
import yaml
import os
from dotenv import load_dotenv
load_dotenv()

def get_env():
    return {
        "email_user": os.getenv("EMAIL_USER"),
        "email_pass": os.getenv("EMAIL_PASS"),
    }
def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def config():
    base_config = load_config()
    env_config = get_env()
    base_config.update(env_config)
    return base_config

import pytest
from playwright.sync_api import Playwright

@pytest.fixture(scope="session")
def api_context(playwright: Playwright, config, page):
    if page.url == "about:blank":
        page.goto(config["base_url"])
        
    token = page.evaluate("window.localStorage.getItem('auth_token')")
    if not token:
        raise Exception("auth_token not found in browser localStorage. Did login run?")

    request_context = playwright.request.new_context(
        base_url=config["api_base_url"],
        extra_http_headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def page(playwright: Playwright, config):
    browser = playwright.chromium.launch(headless=config["headless"],slow_mo=500)

    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
    browser.close()