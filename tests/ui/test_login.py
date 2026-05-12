"""
Login Test Suite

Validates the end-to-end OTP login flow using the LoginPage page object.
"""
import pytest
from pages.login_page import LoginPage
from utils.email_otp import fetch_otp


class TestLogin:
    """Validates the login flow using OTP."""

    def test_login_with_otp(self, unauthenticated_page, config):
        """
        Tests the complete login flow using an email OTP.

        Navigates to the login page, requests an OTP, fetches it via email,
        submits the OTP, and verifies successful login by ensuring the
        'Overview' section is visible on the dashboard.
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
            "Expected 'Overview' to be visible after login."
        )
