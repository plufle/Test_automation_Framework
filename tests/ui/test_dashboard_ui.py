"""
Dashboard UI Test Suite

Validates that all expected elements are present and visible on the
/home (Overview) dashboard after a successful login.

Uses the DashboardPage page object and test_data constants exclusively.
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
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True, scope="function")
def setup_dashboard_page(page, config):
    """Navigate to the dashboard and wait for the Overview section to load."""
    page.goto(config["base_url"])
    page.wait_for_url("**/home")
    page.locator("text=Overview").first.wait_for(state="visible", timeout=20000)


@pytest.fixture
def dashboard(page):
    """Return a DashboardPage instance for the current page."""
    return DashboardPage(page)


@pytest.fixture
def dashboard_api(api_context):
    """Return a DashboardAPIService for API-vs-UI comparison tests."""
    return DashboardAPIService(api_context)


# ---------------------------------------------------------------------------
# Tests — Page basics
# ---------------------------------------------------------------------------

class TestDashboardPageBasics:
    """Basic page-level sanity checks."""

    def test_page_title_contains_satorixr(self, dashboard):
        """The browser tab title should contain the product name."""
        title = dashboard.get_title()
        assert "SatoriXR" in title, f"Expected 'SatoriXR' in page title, got: '{title}'"

    def test_url_navigates_to_home(self, dashboard):
        """After login the URL should resolve to the /home route."""
        url = dashboard.get_url()
        assert DASHBOARD_URL_PATTERN.match(url), (
            f"Expected URL to match '{DASHBOARD_URL_PATTERN.pattern}', got: '{url}'"
        )

    def test_page_has_no_error_messages(self, dashboard):
        """There should be no generic error banners visible on load."""
        error_locator = dashboard.locator("text=error, text=something went wrong, text=404")
        assert error_locator.count() == 0, "An error message is visible on the dashboard."


# ---------------------------------------------------------------------------
# Tests — Overview section
# ---------------------------------------------------------------------------

class TestOverviewSection:
    """Validates the Overview section heading and its supporting text."""

    def test_overview_heading_is_visible(self, dashboard):
        """The 'Overview' heading must be present and visible."""
        heading = dashboard.get_heading(OVERVIEW_HEADING)
        expect(heading).to_be_visible(timeout=10000)

    def test_overview_heading_text(self, dashboard):
        """The first main heading should read exactly 'Overview'."""
        heading = dashboard.get_heading(OVERVIEW_HEADING).first
        heading.wait_for(state="visible", timeout=10000)
        assert heading.inner_text().strip() == OVERVIEW_HEADING, (
            f"Heading text mismatch. Expected '{OVERVIEW_HEADING}', "
            f"got '{heading.inner_text().strip()}'"
        )


# ---------------------------------------------------------------------------
# Tests — Summary cards
# ---------------------------------------------------------------------------

class TestSummaryCards:
    """Validates that each key metric card is present and has content."""

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_is_visible(self, dashboard, card_title):
        """Each metric card label must be visible on the dashboard."""
        card = dashboard.get_metric_card(card_title)
        expect(card).to_be_visible()

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_displays_numeric_value(self, dashboard, card_title):
        """Each metric card should display a numeric value (integer or decimal)."""
        card = dashboard.get_metric_card(card_title)
        expect(card).to_contain_text(re.compile(r"\d+"), timeout=15000)

    def test_products_card_matches_api_data(self, dashboard, dashboard_api):
        """Validates that the Total Products card on UI matches the API count."""
        with allure.step("Fetch active products count from API"):
            api_count = dashboard_api.get_active_products_count()

        with allure.step("Get 'Total Products' metric from UI"):
            ui_count = dashboard.get_metric_card_value("Total Products")
            assert ui_count is not None, "Could not extract numeric value from 'Total Products' card"

        with allure.step("Compare API data with UI data"):
            assert ui_count == api_count, (
                f"UI shows {ui_count} products but API returned {api_count} active products."
            )


# ---------------------------------------------------------------------------
# Tests — Sidebar navigation
# ---------------------------------------------------------------------------

class TestSidebarNavigation:
    """Validates that the primary sidebar navigation links are all present."""

    @pytest.mark.parametrize("nav_label", EXPECTED_NAV_ITEMS)
    def test_nav_item_is_visible(self, dashboard, nav_label):
        """Each primary navigation item must appear in the sidebar."""
        nav = dashboard.get_nav(nav_label)
        expect(nav.first).to_be_visible()


# ---------------------------------------------------------------------------
# Tests — Layout & structural
# ---------------------------------------------------------------------------

class TestDashboardLayout:
    """Higher-level layout and structural checks."""

    def test_all_expected_cards_present(self, dashboard):
        """All required cards must be present in a single assertion for clarity."""
        missing = []
        for title in EXPECTED_CARDS:
            try:
                card = dashboard.get_metric_card(title)
                if not card.is_visible():
                    missing.append(title)
            except Exception:
                missing.append(title)

        assert not missing, f"The following cards are missing from the dashboard: {missing}"

    def test_all_nav_items_present(self, dashboard):
        """All required sidebar nav items must be present in a single assertion."""
        missing = []
        for label in EXPECTED_NAV_ITEMS:
            try:
                nav = dashboard.get_nav(label)
                if not nav.first.is_visible():
                    missing.append(label)
            except Exception:
                missing.append(label)

        assert not missing, f"The following nav items are missing from the sidebar: {missing}"
