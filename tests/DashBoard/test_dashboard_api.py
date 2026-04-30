"""
Dashboard API Test Suite

This module contains API tests for validating the dashboard data endpoints.
"""
import pytest

@pytest.mark.order(3)
class TestAuthAPI:
    """Validates the authentication API endpoints."""

    def test_verify_token(self, api_context):
        """Verifies that the auth token is valid and returns correct user details."""
        response = api_context.get("api/auth/verify-token")

        assert response.status == 200
        data = response.json()
        print(data)
        assert data["success"] is True
        assert "user" in data

        user = data["user"]

        assert "email" in user
        assert "accessType" in user
        assert "role" in user
        assert "tenant" in user


@pytest.mark.order(3)
class TestDashboardStatsAPI:
    """Validates the dashboard statistics endpoints."""

    def test_get_stats(self, api_context):
        """Fetches the dashboard statistics and validates the response schema."""
        response = api_context.get("/api/stats")

        assert response.status == 200

        data = response.json()
        print(data)
        assert isinstance(data["models"], int)
        assert isinstance(data["scenes"], int)
        assert isinstance(data["products"], int)
        assert isinstance(data["shares"], int)
        assert isinstance(data["totalSessions"], int)
        assert isinstance(data["totalUsers"], int)

        assert isinstance(data["revenue"], str)
        assert isinstance(data["user"], str)
        assert isinstance(data["tenant"], str)

    def test_stats_vs_products(self, api_context):
        """Validates that the active products count in stats matches the products list."""
        stats = api_context.get("/api/stats").json()
        products = api_context.get("/api/products").json()

        active_products = [
            p for p in products
            if p.get("status") != "archived"
        ]

        assert stats["products"] == len(active_products)



@pytest.mark.order(3)
class TestProductsAPI:
    """Validates the products API endpoints."""

    def test_get_products(self, api_context):
        """Fetches the products list and validates the fields of the first product."""
        response = api_context.get("/api/products")

        assert response.status == 200
        data = response.json()
        print(data)
        assert isinstance(data, list)

        if len(data) > 0:
            product = data[0]

            assert "id" in product
            assert "name" in product
            assert "type" in product
            assert "date" in product
            assert "status" in product

            assert isinstance(product["modelCount"], int)
            assert isinstance(product["experienceCount"], int)



@pytest.mark.order(3)
class TestScenesAPI:
    """Validates the scenes API endpoints."""

    def test_get_scenes(self, api_context):
        """Fetches the scenes list and validates the fields of the first scene."""
        response = api_context.get("/api/scenes")

        assert response.status == 200

        data = response.json()
        print(data)
        assert "scenes" in data
        assert isinstance(data["scenes"], list)

        if len(data["scenes"]) > 0:
            scene = data["scenes"][0]

            assert "id" in scene
            assert "name" in scene
            assert "displayTitle" in scene
            assert "productId" in scene
            assert "status" in scene