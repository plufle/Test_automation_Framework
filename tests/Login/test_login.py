"""
Login Test Suite

This module contains UI tests for the login functionality.
"""
from utils.email_otp import fetch_otp
import pytest

@pytest.mark.order(1)
class TestLogin:
    """Validates the login flow using OTP."""

    def test_login_with_otp(self, page, config):
        """
        Tests the complete login flow using an email OTP.
        
        Navigates to the login page, requests an OTP, fetches it via email,
        submits the OTP, and verifies successful login by ensuring the
        'Overview' section is visible on the dashboard. Saves the auth state.
        """
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

        assert page.get_by_text("Overview").is_visible(), "Expected 'Overview' to be visible after login."