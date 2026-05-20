pytest_plugins = [
    "fixtures.config_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.api_fixtures",
    "fixtures.reporting_fixtures",
]
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: dev, qa, prod"
    )

def pytest_collection_modifyitems(items):
    """Automatically configure retries for tests marked as 'flaky'."""
    for item in items:
        if item.get_closest_marker("flaky"):
            item.add_marker(pytest.mark.flaky(reruns=3, reruns_delay=2))
