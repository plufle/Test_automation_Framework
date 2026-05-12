import re

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
