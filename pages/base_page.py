import allure
from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        self.page.goto(url)

    @allure.step("Wait for URL pattern: {url_pattern}")
    def wait_for_url(self, url_pattern: str):
        self.page.wait_for_url(url_pattern)

    @allure.step("Get element by role '{role}' and name '{name}'")
    def get_by_role(self, role: str, name: str = None) -> Locator:
        if name:
            return self.page.get_by_role(role, name=name)
        return self.page.get_by_role(role)

    @allure.step("Get element by text '{text}'")
    def get_by_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)
    
    @allure.step("Get locator using selector '{selector}'")
    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)
