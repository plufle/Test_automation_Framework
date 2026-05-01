import allure
from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = self.page.locator("#email")
        self.send_otp_button = self.page.get_by_role("button", name="Send Verification Code")
        self.otp_input = self.page.locator("#otp")
        self.verify_signin_button = self.page.get_by_role("button", name="Verify & Sign In")

    @allure.step("Fill email input with {email}")
    def fill_email(self, email: str):
        self.email_input.fill(email)

    @allure.step("Click 'Send Verification Code' button")
    def click_send_otp(self):
        self.send_otp_button.click()

    @allure.step("Fill OTP input")
    def fill_otp(self, otp: str):
        self.otp_input.fill(otp)

    @allure.step("Click 'Verify & Sign In' button")
    def click_verify_signin(self):
        self.verify_signin_button.click()
