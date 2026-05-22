"""
Dashboard UI Test Suite

Each test validates exactly ONE thing (atomic tests).
Uses DashboardPage page object and test_data constants exclusively.

Naming convention:
    test_<area>_<what_is_being_checked>
"""

import re
import pytest
import allure
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage
from services.api_service import DashboardAPIService
from test_data.dashboard_data import (
    DASHBOARD_URL_PATTERN,
    OVERVIEW_HEADING,
    EXPECTED_CARDS,
    EXPECTED_NAV_ITEMS,
)


# ---------------------------------------------------------------------------
# Fixtures — setup via page objects, not raw locators
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def module_page(browser, browser_context_args, config):
    """
    Module-scoped page that navigates to the dashboard once.
    This avoids unnecessary navigation/setup for every single test.
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    
    dashboard = DashboardPage(page)
    dashboard.navigate(config["base_url"])
    dashboard.wait_for_url("**/home")
    dashboard.get_heading(OVERVIEW_HEADING).first.wait_for(
        state="visible", timeout=20000
    )
    yield page
    context.close()


@pytest.fixture
def dashboard(module_page):
    """Return a DashboardPage instance bound to the shared module page."""
    return DashboardPage(module_page)


@pytest.fixture
def dashboard_api(api_context):
    """Return a DashboardAPIService for API-vs-UI comparison tests."""
    return DashboardAPIService(api_context)


# ---------------------------------------------------------------------------
# Page basics — one assertion per test
# ---------------------------------------------------------------------------

@pytest.mark.ui
class TestDashboardPageBasics:
    """Basic page-level sanity checks."""

    @pytest.mark.smoke
    def test_page_title_contains_product_name(self, dashboard):
        """The browser tab title should contain 'SatoriXR'."""
        title = dashboard.get_title()
        assert "SatoriXR" in title, (
            f"Expected 'SatoriXR' in page title, got: '{title}'"
        )

    @pytest.mark.smoke
    def test_url_resolves_to_home_route(self, dashboard):
        """After login the URL should match the /home pattern."""
        url = dashboard.get_url()
        assert DASHBOARD_URL_PATTERN.match(url), (
            f"Expected URL to match '{DASHBOARD_URL_PATTERN.pattern}', got: '{url}'"
        )

    @pytest.mark.regression
    def test_no_error_banners_on_load(self, dashboard):
        """No generic error banners should be visible on the dashboard."""
        error_locator = dashboard.locator(
            "text=error, text=something went wrong, text=404"
        )
        assert error_locator.count() == 0, (
            "An error message is visible on the dashboard."
        )


# ---------------------------------------------------------------------------
# Overview section — one assertion per test
# ---------------------------------------------------------------------------

@pytest.mark.ui
class TestOverviewSection:
    """Validates the Overview heading."""

    @pytest.mark.smoke
    def test_overview_heading_is_visible(self, dashboard):
        """The 'Overview' heading must be visible."""
        heading = dashboard.get_heading(OVERVIEW_HEADING)
        expect(heading).to_be_visible(timeout=10000)

    @pytest.mark.regression
    def test_overview_heading_text_is_exact(self, dashboard):
        """The heading should read exactly 'Overview'."""
        heading = dashboard.get_heading(OVERVIEW_HEADING).first
        heading.wait_for(state="visible", timeout=10000)
        actual = heading.inner_text().strip()
        assert actual == OVERVIEW_HEADING, (
            f"Expected heading '{OVERVIEW_HEADING}', got '{actual}'"
        )


# ---------------------------------------------------------------------------
# Summary cards — parametrized = one test run per card
# ---------------------------------------------------------------------------

@pytest.mark.ui
class TestSummaryCards:
    """Validates metric cards. Each parametrized run = one card = one assertion."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_is_visible(self, dashboard, card_title):
        """The metric card should be visible on the dashboard."""
        card = dashboard.get_metric_card(card_title)
        expect(card).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_displays_a_number(self, dashboard, card_title):
        """The metric card should contain at least one digit."""
        card = dashboard.get_metric_card(card_title)
        expect(card).to_contain_text(re.compile(r"\d+"), timeout=15000)


# ---------------------------------------------------------------------------
# API-vs-UI consistency — single comparison assertion
# ---------------------------------------------------------------------------

@pytest.mark.ui
@pytest.mark.api
class TestApiUiConsistency:
    """Cross-layer validation between API data and UI display."""

    @pytest.mark.regression
    def test_products_card_matches_api_count(self, dashboard, dashboard_api):
        """The 'Total Products' card value should equal the API active count."""
        with allure.step("Fetch active products count from API"):
            api_count = dashboard_api.get_active_products_count()

        with allure.step("Extract numeric value from 'Total Products' card"):
            ui_count = dashboard.get_metric_card_value("Total Products")

        assert ui_count is not None, (
            "Could not extract a numeric value from the 'Total Products' card."
        )
        assert ui_count == api_count, (
            f"UI shows {ui_count} products but API returned {api_count}."
        )


# ---------------------------------------------------------------------------
# Sidebar navigation — parametrized = one test run per nav item
# ---------------------------------------------------------------------------

@pytest.mark.ui
class TestSidebarNavigation:
    """Validates sidebar nav items. Each parametrized run = one item."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("nav_label", EXPECTED_NAV_ITEMS)
    def test_nav_item_is_visible(self, dashboard, nav_label):
        """The navigation item should be visible in the sidebar."""
        nav = dashboard.get_nav(nav_label)
        expect(nav.first).to_be_visible()
