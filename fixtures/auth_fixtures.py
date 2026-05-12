import pytest
from utils.email_otp import fetch_otp

@pytest.fixture(scope="session")
def global_auth_state(config, tmp_path_factory, browser):
    """
    Performs login once per session and saves the storage state.
    Returns the path to the state file.
    """
    state_path = tmp_path_factory.mktemp("state") / "state.json"
    
    context = browser.new_context()
    page = context.new_page()
    
    page.goto(config["base_url"])
    page.fill("#email", config["email_user"])
    page.get_by_role("button", name="Send Verification Code").click()

    otp = fetch_otp(config["email_user"], config["email_pass"])

    page.fill("#otp", otp)
    page.get_by_role("button", name="Verify & Sign In").click()
    page.wait_for_url("**/home")
    
    # Ensure token is populated
    page.wait_for_function("window.localStorage.getItem('auth_token') != null")
    
    context.storage_state(path=state_path)
    context.close()
        
    return state_path

@pytest.fixture
def browser_context_args(browser_context_args, global_auth_state):
    """
    Apply the authenticated state to all tests using the default page fixture.
    """
    return {
        **browser_context_args,
        "storage_state": global_auth_state,
    }

@pytest.fixture
def unauthenticated_page(browser, config):
    """
    Provides a fresh, unauthenticated page specifically for login tests.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
