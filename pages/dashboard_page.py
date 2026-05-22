"""
DashboardPage — Page Object for the SatoriXR /home dashboard.

Locators + actions only. No assertions.
"""

import re
import allure
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Provides locators and actions for the main dashboard view."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ------------------------------------------------------------------
    # Heading locators
    # ------------------------------------------------------------------

    @allure.step("Get heading with name '{name}'")
    def get_heading(self, name: str) -> Locator:
        """Return a locator for a heading element by accessible name."""
        return self.page.get_by_role("heading", name=name)

    # ------------------------------------------------------------------
    # Metric card locators
    # ------------------------------------------------------------------

    @allure.step("Get metric card by title '{title}'")
    def get_metric_card(self, title: str) -> Locator:
        """
        Locates a metric card container by targeting its container classes 'div.bg-white.rounded-xl'
        and filtering by the card title text.
        """
        return self.page.locator("div.bg-white.rounded-xl").filter(has_text=title)

    # ------------------------------------------------------------------
    # Metric card data extraction
    # ------------------------------------------------------------------

    @allure.step("Extract numeric value from metric card '{title}'")
    def get_metric_card_value(self, title: str) -> int | None:
        """
        Return the first integer found in the card's inner text,
        or None if no number is present.
        """
        card = self.get_metric_card(title)
        text = card.inner_text()
        match = re.search(r"\d+", text)
        return int(match.group(0)) if match else None

    # ------------------------------------------------------------------
    # Navigation locators
    # ------------------------------------------------------------------

    @allure.step("Get navigation item with name '{name}'")
    def get_nav_item(self, name: str) -> Locator:
        """Return a locator for a sidebar navigation link or button."""
        if name == "Settings":
            return self.page.get_by_role("button", name=name)
        return self.page.get_by_role("link", name=name)

    @allure.step("Get navigation item (fallback) with name '{name}'")
    def get_nav_item_fallback(self, name: str) -> Locator:
        """Fallback — locate by visible text when there is no link role."""
        if name == "Settings":
            return self.page.locator("button").filter(has_text=name)
        return self.page.locator(f"text={name}")

    def get_nav(self, name: str, timeout: int = 2000) -> Locator:
        """
        Smart nav locator — tries by role first, then falls back to
        text-based lookup.
        """
        primary = self.get_nav_item(name)
        try:
            primary.wait_for(state="attached", timeout=timeout)
            return primary
        except Exception:
            fallback = self.get_nav_item_fallback(name)
            fallback.wait_for(state="attached", timeout=timeout)
            return fallback
