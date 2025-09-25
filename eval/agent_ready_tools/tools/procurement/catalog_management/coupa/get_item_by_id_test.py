from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_by_id import (
    coupa_get_item_by_id,
)


def test_coupa_get_item_by_id() -> None:
    """test the get_item_by_id tool."""

    test_data = {
        "item_id": 2,
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "id": 2,
            "description": "Laptops and Tablets",
            "item-number": "5KH25",
            "name": "Laptops and Tablets",
            "active": True,
            "storage-quantity": None,
            "consumption-quantity": None,
        }

        response = coupa_get_item_by_id(test_data["item_id"]).content

        assert response
        assert response.item_id == test_data["item_id"]

        params = {
            "fields": '["id", "item-number", "name", "description", "active", "storage-quantity", "consumption-quantity"]',
        }
        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name=f"items/{test_data['item_id']}", params=params
        )
