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
    def get_metric_card_by_title(self, title: str) -> Locator:
        """
        Primary locator: look for common card-like class names that
        contain the expected title text.
        """
        card_container = self.page.locator(
            f"[class*='card']:has-text('{title}'), "
            f"[class*='Card']:has-text('{title}'), "
            f"[class*='stat']:has-text('{title}'), "
            f"[class*='metric']:has-text('{title}')"
        ).first
        return card_container

    @allure.step("Get metric card (fallback) by title '{title}'")
    def get_metric_card_fallback(self, title: str) -> Locator:
        """
        Fallback locator — finds the deepest div that contains both
        the title and a digit, avoiding broad layout wrappers.
        """
        return (
            self.page.locator("div")
            .filter(has_text=title)
            .filter(has_text=re.compile(r"\d"))
            .last
        )

    def get_metric_card(self, title: str, timeout: int = 10000) -> Locator:
        """
        Smart card locator — tries the primary selector first, then
        falls back automatically.  Returns whichever locator is attached.
        """
        primary = self.get_metric_card_by_title(title)
        try:
            primary.wait_for(state="attached", timeout=timeout)
            return primary
        except Exception:
            fallback = self.get_metric_card_fallback(title)
            fallback.wait_for(state="attached", timeout=timeout)
            return fallback

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
        """Return a locator for a sidebar navigation link."""
        return self.page.get_by_role("link", name=name)

    @allure.step("Get navigation item (fallback) with name '{name}'")
    def get_nav_item_fallback(self, name: str) -> Locator:
        """Fallback — locate by visible text when there is no link role."""
        return self.page.locator(f"text={name}")

    def get_nav(self, name: str, timeout: int = 10000) -> Locator:
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
