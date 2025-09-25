from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.get_commodities import (
    coupa_get_commodities,
)


def test_coupa_get_commodities() -> None:
    """Test the get_commodities tool."""

    # Define test data
    test_data = {
        "name": "Beverages",
        "parent_name": "Breakroom/Kitchen",
        "is_active": True,
        "limit": 20,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.get_commodities.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "name": test_data["name"],
                "parent": {"name": test_data["parent_name"]},
                "active": test_data["is_active"],
            }
        ]

        response = coupa_get_commodities().content

        assert response
        assert response.commodities[0].name == test_data["name"]
        assert response.commodities[0].parent_name == test_data["parent_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="commodities",
            params={"limit": test_data["limit"]},
        )


def test_coupa_get_commodities_with_name() -> None:
    """Test the get_commodities tool with filter parameter name."""

    # Define test data
    test_data = {
        "name": "Beverages",
        "parent_name": "Breakroom/Kitchen",
        "is_active": True,
        "limit": 20,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.get_commodities.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "name": test_data["name"],
                "parent": {"name": test_data["parent_name"]},
                "active": test_data["is_active"],
            }
        ]

        response = coupa_get_commodities(commodity_name=test_data["name"]).content

        assert response
        assert response.commodities[0].name == test_data["name"]
        assert response.commodities[0].parent_name == test_data["parent_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="commodities",
            params={"name[contains]": test_data["name"], "limit": test_data["limit"]},
        )
