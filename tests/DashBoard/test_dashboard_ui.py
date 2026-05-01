import pytest
from pages.dashboard_page import DashboardPage
from test_data.dashboard_data import (
    DASHBOARD_URL_PATTERN,
    OVERVIEW_HEADING,
    EXPECTED_CARDS,
    EXPECTED_NAV_ITEMS,
)

from playwright.sync_api import expect

@pytest.fixture(autouse=True, scope="function")
def setup_dashboard_page(page, config):
    page.goto(config["base_url"])
    page.wait_for_url("**/home")
    page.locator("text=Overview").first.wait_for(state="visible", timeout=2000)

class TestDashboardPageBasics:
    """Basic page-level sanity checks."""

    def test_page_title_contains_satorixr(self, page):
        """The browser tab title should contain the product name."""
        title = page.title()
        assert "SatoriXR" in title, f"Expected 'SatoriXR' in page title, got: '{title}'"

    def test_url_navigates_to_home(self, page):
        """After login the URL should resolve to the /home route."""
        dashboard_page = DashboardPage(page)
        url = dashboard_page.page.url
        assert DASHBOARD_URL_PATTERN.match(url), f"Expected URL to match '{DASHBOARD_URL_PATTERN.pattern}', got: '{url}'"

    def test_page_has_no_error_messages(self, page):
        """There should be no generic error banners visible on load."""
        dashboard_page = DashboardPage(page)
        error_locator = dashboard_page.locator("text=error, text=something went wrong, text=404")
        assert error_locator.count() == 0, "An error message is visible on the dashboard."

class TestOverviewSection:
    """Validates the Overview section heading and its supporting text."""

    def test_overview_heading_is_visible(self, page):
        """The 'Overview' heading must be present and visible."""
        dashboard_page = DashboardPage(page)
        heading = dashboard_page.get_heading(OVERVIEW_HEADING)
        expect(heading).to_be_visible(timeout=10000)

    def test_overview_heading_text(self, page):
        """The first main heading should read exactly 'Overview'."""
        dashboard_page = DashboardPage(page)
        heading = dashboard_page.get_heading(OVERVIEW_HEADING).first
        heading.wait_for(state="visible", timeout=10000)
        assert heading.inner_text().strip() == OVERVIEW_HEADING, (
            f"Heading text mismatch. Expected '{OVERVIEW_HEADING}', got '{heading.inner_text().strip()}'"
        )

class TestSummaryCards:
    """Validates that each key metric card is present and has content."""

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_is_visible(self, page, card_title):
        """Each metric card label must be visible on the dashboard."""
        dashboard_page = DashboardPage(page)
        locator = dashboard_page.get_metric_card_by_title(card_title)
        
        try:
            locator.wait_for(state="attached", timeout=10000)
        except Exception:
            locator = dashboard_page.get_metric_card_fallback(card_title)
            locator.wait_for(state="attached", timeout=10000)
            
        expect(locator).to_be_visible()

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_displays_numeric_value(self, page, card_title):
        """
        Each metric card should display a numeric value (integer or decimal).
        """
        import re
        dashboard_page = DashboardPage(page)
        card_container = dashboard_page.get_metric_card_by_title(card_title)

        try:
            card_container.wait_for(state="attached", timeout=10000)
        except Exception:
            card_container = dashboard_page.get_metric_card_fallback(card_title)
            card_container.wait_for(state="attached", timeout=10000)

        expect(card_container).to_contain_text(re.compile(r"\d+"), timeout=15000)

    def test_products_card_matches_api_data(self, page, api_context):
        """Validates that the Total Products card on UI matches the active products count from API."""
        import allure
        import re
        
        dashboard_page = DashboardPage(page)
        
        with allure.step("Fetch products from API"):
            response = api_context.get("/api/products")
            assert response.status == 200, "API failed to fetch products"
            products = response.json()
            active_products_count = len([p for p in products if p.get("status") != "archived"])
            
        with allure.step("Get 'Total Products' metric from UI"):
            card_locator = dashboard_page.get_metric_card_by_title("Total Products")
            try:
                card_locator.wait_for(state="attached", timeout=10000)
            except Exception:
                card_locator = dashboard_page.get_metric_card_fallback("Total Products")
                card_locator.wait_for(state="attached", timeout=10000)
                
            expect(card_locator).to_contain_text(re.compile(r"\d+"), timeout=15000)
            ui_text = card_locator.inner_text()
            
        with allure.step("Extract number from UI text"):
            match = re.search(r"\d+", ui_text)
            assert match is not None, f"Could not find numeric value in '{ui_text}'"
            ui_count = int(match.group(0))
            
        with allure.step("Compare API data with UI data"):
            assert ui_count == active_products_count, (
                f"UI shows {ui_count} products but API returned {active_products_count} active products."
            )


class TestSidebarNavigation:
    """Validates that the primary sidebar navigation links are all present."""

    @pytest.mark.parametrize("nav_label", EXPECTED_NAV_ITEMS)
    def test_nav_item_is_visible(self, page, nav_label):
        """Each primary navigation item must appear in the sidebar."""
        dashboard_page = DashboardPage(page)
        locator = dashboard_page.get_nav_item(nav_label)
        
        try:
            locator.wait_for(state="attached", timeout=10000)
        except Exception:
            locator = dashboard_page.get_nav_item_fallback(nav_label)
            locator.wait_for(state="attached", timeout=10000)

        expect(locator.first).to_be_visible()

class TestDashboardLayout:
    """Higher-level layout and structural checks."""
    
    def test_all_expected_cards_present(self, page):
        """All required cards must be present in a single assertion for clarity."""
        dashboard_page = DashboardPage(page)
        missing = []
        for title in EXPECTED_CARDS:
            locator = dashboard_page.get_metric_card_by_title(title)
            try:
                locator.wait_for(state="attached", timeout=10000)
            except Exception:
                locator = dashboard_page.get_metric_card_fallback(title)
            
            if locator.count() == 0 or not locator.is_visible():
                missing.append(title)

        assert not missing, f"The following cards are missing from the dashboard: {missing}"

    def test_all_nav_items_present(self, page):
        """All required sidebar nav items must be present in a single assertion."""
        dashboard_page = DashboardPage(page)
        missing = []
        for label in EXPECTED_NAV_ITEMS:
            locator = dashboard_page.get_nav_item_fallback(label)
            try:
                locator.first.wait_for(state="attached", timeout=10000)
            except Exception:
                pass
            
            if locator.count() == 0 or not locator.first.is_visible():
                missing.append(label)

        assert not missing, f"The following nav items are missing from the sidebar: {missing}"