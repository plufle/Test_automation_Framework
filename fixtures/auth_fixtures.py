"""
Authentication fixtures.

- global_auth_state  : session-scoped login → saves storage state once.
- browser_context_args : injects authenticated state into every test's context.
- unauthenticated_page : clean browser context for login-flow tests.
"""

import os
from pathlib import Path
import pytest
from pages.login_page import LoginPage
from utils.email_otp import fetch_otp
from utils.waits import wait_for_local_storage


@pytest.fixture(scope="session")
def global_auth_state(config, browser):
    """
    Performs login once per session using the LoginPage page object
    and saves the authenticated storage state to disk.
    Reuses existing state if available.

    Returns the path to the state.json file.
    """
    state_dir = Path(".auth")
    state_dir.mkdir(exist_ok=True)
    state_path = state_dir / "state.json"

    if state_path.exists():
        return str(state_path)

    context = browser.new_context()
    page = context.new_page()

    # Use the LoginPage page object — no raw locators in fixtures
    login_page = LoginPage(page)
    login_page.navigate(config["base_url"])
    login_page.fill_email(config["email_user"])
    login_page.click_send_otp()

    otp = fetch_otp(config["email_user"], config["email_pass"])

    login_page.fill_otp(otp)
    login_page.click_verify_signin()
    login_page.wait_for_url("**/home")

    # Wait until the auth token is stored in localStorage
    wait_for_local_storage(page, "auth_token")

    context.storage_state(path=str(state_path))
    context.close()

    return str(state_path)


@pytest.fixture
def browser_context_args(browser_context_args, global_auth_state):
    """
    Injects the authenticated storage state into the default browser
    context used by pytest-playwright's `page` fixture.

    Every test gets its own fresh context pre-loaded with auth,
    ensuring complete test isolation.
    """
    return {
        **browser_context_args,
        "storage_state": global_auth_state,
    }


@pytest.fixture
def unauthenticated_page(browser):
    """
    Provides a fresh, unauthenticated page for login-flow tests.

    Creates its own isolated context so it cannot leak state to or
    from other tests.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
