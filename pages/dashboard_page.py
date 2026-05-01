import allure
from playwright.sync_api import Page, Locator
from .base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get heading with name '{name}'")
    def get_heading(self, name: str) -> Locator:
        return self.page.get_by_role("heading", name=name)

    @allure.step("Get metric card by title '{title}'")
    def get_metric_card_by_title(self, title: str) -> Locator:
        """
        Return a locator for the metric card container based on its title.
        """
        card_container = self.page.locator(
            f"[class*='card']:has-text('{title}'), "
            f"[class*='Card']:has-text('{title}'), "
            f"[class*='stat']:has-text('{title}'), "
            f"[class*='metric']:has-text('{title}')"
        ).first

        return card_container

    @allure.step("Get metric card (fallback locator) by title '{title}'")
    def get_metric_card_fallback(self, title: str) -> Locator:
        """
        Fallback locator if the primary one doesn't work.
        """
        import re
        # Find the deepest div that contains both the title and a digit.
        # This cleanly avoids catching large layout wrappers like the sidebar.
        return self.page.locator("div").filter(has_text=title).filter(has_text=re.compile(r"\d")).last

    @allure.step("Get navigation item with name '{name}'")
    def get_nav_item(self, name: str) -> Locator:
        """
        Return a locator for the navigation link.
        """
        return self.page.get_by_role("link", name=name)
        
    @allure.step("Get navigation item (fallback locator) with name '{name}'")
    def get_nav_item_fallback(self, name: str) -> Locator:
        return self.page.locator(f"text={name}")
