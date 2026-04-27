from utils.email_otp import fetch_otp
import pytest

@pytest.mark.order(1)
def test_login_with_otp(page, config):
    page.goto(config["base_url"])
    print(config["base_url"])
    page.fill("#email", config["email_user"])
    page.get_by_role("button", name="Send Verification Code").click()

    otp = fetch_otp(
        config["email_user"],
        config["email_pass"]
    )

    page.fill("#otp", otp)
    page.get_by_role("button", name="Verify & Sign In").click()
    page.wait_for_url("**/home")

    page.context.storage_state(path="auth.json")
    assert page.get_by_text("Overview").is_visible()