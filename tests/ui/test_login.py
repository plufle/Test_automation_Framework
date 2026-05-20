"""
Login Test Suite

Validates the end-to-end OTP login flow.

Naming convention:
    test_login_<what_is_being_checked>
"""

import pytest
from pages.login_page import LoginPage
from utils.email_otp import fetch_otp


@pytest.mark.ui
@pytest.mark.smoke
class TestLoginFlow:
    """Validates the complete OTP-based login flow."""

    def test_login_with_valid_otp_lands_on_dashboard(self, unauthenticated_page, config):
        """
        After submitting a valid OTP the user should be redirected
        to /home and the 'Overview' heading should be visible.
        """
        login_page = LoginPage(unauthenticated_page)

        login_page.navigate(config["base_url"])
        login_page.fill_email(config["email_user"])
        login_page.click_send_otp()

        otp = fetch_otp(config["email_user"], config["email_pass"])

        login_page.fill_otp(otp)
        login_page.click_verify_signin()
        login_page.wait_for_url("**/home")

        assert login_page.get_by_text("Overview").is_visible(), (
            "Expected 'Overview' to be visible after successful login."
        )
