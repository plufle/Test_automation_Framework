import pytest
from playwright.sync_api import sync_playwright
import yaml
import os
from dotenv import load_dotenv
load_dotenv()
import json

import json

def get_token_from_storage():
    with open("auth.json") as f:
        state = json.load(f)

    for origin in state.get("origins", []):
        for item in origin.get("localStorage", []):
            if item["name"] == "auth_token":   
                return item["value"]

    raise Exception("auth_token not found in auth.json")

    raise Exception("Token not found in auth.json")
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
def api_context(playwright: Playwright, config):
    storage = "auth.json" if os.path.exists("auth.json") else None
    token = get_token_from_storage()
    request_context = playwright.request.new_context(
        base_url=config["api_base_url"],
        storage_state=storage,
        extra_http_headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    yield request_context
    request_context.dispose()


# @pytest.fixture(scope="session", autouse=True)
# def cleanup_auth():
#     yield

#     if os.path.exists("auth.json"):
#         os.remove("auth.json")
#         print("auth.json deleted after test session")

@pytest.fixture
def page(playwright: Playwright, config):
    browser = playwright.chromium.launch(headless=config["headless"],slow_mo=500)

    if os.path.exists("auth.json"):
        context = browser.new_context(storage_state="auth.json")
    else:
        context = browser.new_context()

    page = context.new_page()

    yield page

    context.close()
    browser.close()