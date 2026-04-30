import re
import pytest

@pytest.fixture(autouse=True, scope="module")
def setup_dashboard_page(page, config):
    page.goto(config["base_url"])
    page.wait_for_url("**/home")
# ---------------------------------------------------------------------------
# Constants – expected UI text
# ---------------------------------------------------------------------------

DASHBOARD_URL_PATTERN = re.compile(r".*/home.*")

OVERVIEW_HEADING = "Overview"

EXPECTED_CARDS = [
    "Total Products",
    "Experiences",
    "Sessions",
    "Users",
]

EXPECTED_NAV_ITEMS = [
    "Home",
    "Products",
    "Experiences",
    "Analytics",
    "Settings",
]


# ---------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _visible_text(page, selector: str) -> str:
    """Return the inner text of the first element matching *selector*."""
    return page.locator(selector).first.inner_text().strip()


def _card_locator(page, card_title: str):
    """
    Return a Locator for the card whose visible heading matches *card_title*.
    Works with div/section/article containers that contain a child span or
    heading with the given text.
    """
    return page.locator(f"text={card_title}").first



@pytest.mark.order(2)
class TestDashboardPageBasics:
    """Basic page-level sanity checks."""

    def test_page_title_contains_satorixr(self, page):
        """The browser tab title should contain the product name."""
        title = page.title()
        assert "SatoriXR" in title, (
            f"Expected 'SatoriXR' in page title, got: '{title}'"
        )

    def test_url_navigates_to_home(self, page):
        """After login the URL should resolve to the /home route."""
        url = page.url
        assert DASHBOARD_URL_PATTERN.match(url), (
            f"Expected URL to match '{DASHBOARD_URL_PATTERN.pattern}', got: '{url}'"
        )

    def test_page_has_no_error_messages(self, page):
        """There should be no generic error banners visible on load."""
        error_locator = page.locator(
            "text=error, text=something went wrong, text=404"
        )
        assert error_locator.count() == 0, (
            "An error message is visible on the dashboard."
        )



@pytest.mark.order(2)
class TestOverviewSection:
    """Validates the Overview section heading and its supporting text."""

    def test_overview_heading_is_visible(self, page):
        """The 'Overview' heading must be present and visible."""
        heading = page.get_by_role("heading", name=OVERVIEW_HEADING)
        assert heading.is_visible(), (
            f"Expected heading '{OVERVIEW_HEADING}' to be visible on the dashboard."
        )

    def test_overview_heading_text(self, page):
        """The first main heading should read exactly 'Overview'."""
        heading = page.get_by_role("heading", name=OVERVIEW_HEADING).first
        assert heading.inner_text().strip() == OVERVIEW_HEADING, (
            f"Heading text mismatch. Expected '{OVERVIEW_HEADING}', "
            f"got '{heading.inner_text().strip()}'"
        )



@pytest.mark.order(2)
class TestSummaryCards:
    """Validates that each key metric card is present and has content."""

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_is_visible(self, page, card_title):
        """Each metric card label must be visible on the dashboard."""
        locator = _card_locator(page, card_title)
        assert locator.count() > 0, (
            f"Card with title '{card_title}' was not found on the dashboard."
        )
        assert locator.is_visible(), (
            f"Card '{card_title}' is in the DOM but not visible."
        )

    @pytest.mark.parametrize("card_title", EXPECTED_CARDS)
    def test_card_displays_numeric_value(self, page, card_title):
        """
        Each metric card should display a numeric value (integer or decimal).
        We look for a sibling/descendant that contains at least one digit.
        """
        card_container = page.locator(
            f"[class*='card']:has-text('{card_title}'), "
            f"[class*='Card']:has-text('{card_title}'), "
            f"[class*='stat']:has-text('{card_title}'), "
            f"[class*='metric']:has-text('{card_title}')"
        ).first

        if card_container.count() == 0:
            card_container = page.locator(
                f"text={card_title}"
            ).locator("xpath=ancestor::*[3]").first

        container_text = card_container.inner_text()
        has_number = re.search(r"\d", container_text) is not None
        assert has_number, (
            f"Card '{card_title}' does not appear to contain a numeric value. "
            f"Full text found: '{container_text}'"
        )



@pytest.mark.order(2)
class TestSidebarNavigation:
    """Validates that the primary sidebar navigation links are all present."""

    @pytest.mark.parametrize("nav_label", EXPECTED_NAV_ITEMS)
    def test_nav_item_is_visible(self, page, nav_label):
        """Each primary navigation item must appear in the sidebar."""
        locator = page.get_by_role("link", name=nav_label)
        if locator.count() == 0:
            locator = page.locator(f"text={nav_label}")

        assert locator.count() > 0, (
            f"Navigation item '{nav_label}' was not found on the page."
        )
        assert locator.first.is_visible(), (
            f"Navigation item '{nav_label}' is present but not visible."
        )



@pytest.mark.order(2)
class TestDashboardLayout:
    """Higher-level layout and structural checks."""

    # def test_dashboard_has_exactly_one_h1(self, page):
    #     """Best practice: there should be exactly one <h1> on the dashboard."""
    #     h1_count = page.locator("h1").count()
    #     assert h1_count == 1, (
    #         f"Expected exactly 1 <h1> on the dashboard, found {h1_count}."
    #     )

    def test_all_expected_cards_present(self, page):
        """All required cards must be present in a single assertion for clarity."""
        missing = []
        for title in EXPECTED_CARDS:
            locator = _card_locator(page, title)
            if locator.count() == 0 or not locator.is_visible():
                missing.append(title)

        assert not missing, (
            f"The following cards are missing from the dashboard: {missing}"
        )

    def test_all_nav_items_present(self, page):
        """All required sidebar nav items must be present in a single assertion."""
        missing = []
        for label in EXPECTED_NAV_ITEMS:
            locator = page.locator(f"text={label}")
            if locator.count() == 0 or not locator.first.is_visible():
                missing.append(label)

        assert not missing, (
            f"The following nav items are missing from the sidebar: {missing}"
        )