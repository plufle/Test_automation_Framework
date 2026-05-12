"""
Dashboard API Test Suite

Validates dashboard data endpoints using the DashboardAPIService.
"""
import pytest
from services.api_service import DashboardAPIService


@pytest.fixture(scope="module")
def dashboard_api(api_context):
    """Provide a DashboardAPIService wired to the authenticated API context."""
    return DashboardAPIService(api_context)


class TestAuthAPI:
    """Validates the authentication API endpoints."""

    def test_verify_token(self, dashboard_api):
        """Verifies that the auth token is valid and returns correct user details."""
        data = dashboard_api.verify_token()

        assert data["success"] is True
        assert "user" in data

        user = data["user"]
        assert "email" in user
        assert "accessType" in user
        assert "role" in user
        assert "tenant" in user


class TestDashboardStatsAPI:
    """Validates the dashboard statistics endpoints."""

    def test_get_stats(self, dashboard_api):
        """Fetches the dashboard statistics and validates the response schema."""
        data = dashboard_api.get_stats()

        assert isinstance(data["models"], int)
        assert isinstance(data["scenes"], int)
        assert isinstance(data["products"], int)
        assert isinstance(data["shares"], int)
        assert isinstance(data["totalSessions"], int)
        assert isinstance(data["totalUsers"], int)

        assert isinstance(data["revenue"], str)
        assert isinstance(data["user"], str)
        assert isinstance(data["tenant"], str)

    def test_stats_vs_products(self, dashboard_api):
        """Validates that the active products count in stats matches the products list."""
        stats = dashboard_api.get_stats()
        active_count = dashboard_api.get_active_products_count()
        assert stats["products"] == active_count


class TestProductsAPI:
    """Validates the products API endpoints."""

    def test_get_products(self, dashboard_api):
        """Fetches the products list and validates the fields of the first product."""
        products = dashboard_api.get_products()
        assert isinstance(products, list)

        if len(products) > 0:
            product = products[0]
            assert "id" in product
            assert "name" in product
            assert "type" in product
            assert "date" in product
            assert "status" in product
            assert isinstance(product["modelCount"], int)
            assert isinstance(product["experienceCount"], int)


class TestScenesAPI:
    """Validates the scenes API endpoints."""

    def test_get_scenes(self, dashboard_api):
        """Fetches the scenes list and validates the fields of the first scene."""
        data = dashboard_api.get_scenes()

        assert "scenes" in data
        assert isinstance(data["scenes"], list)

        if len(data["scenes"]) > 0:
            scene = data["scenes"][0]
            assert "id" in scene
            assert "name" in scene
            assert "displayTitle" in scene
            assert "productId" in scene
            assert "status" in scene
