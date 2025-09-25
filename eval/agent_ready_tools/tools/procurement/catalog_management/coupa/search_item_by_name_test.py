from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.search_item_by_name import (
    coupa_search_item_by_name,
)


def test_coupa_search_item_by_name() -> None:
    """test the search_item_by_name tool."""

    # Define test data:
    test_data = {
        "search_term": "laptops",
        "id": 2,
        "description": "Laptops and Tablets",
        "item_number": "5KH25",
        "name": "Rapus A1",
        "active": True,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.search_item_by_name.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["id"],
                "description": test_data["description"],
                "item_number": test_data["item_number"],
                "name": test_data["name"],
                "active": test_data["active"],
                "storage-quantity": None,
                "consumption-quantity": None,
            }
        ]

        # Get item suppliers
        response = coupa_search_item_by_name(test_data["search_term"]).content

        # Ensure that get_item_suppliers() executed and returned proper values
        assert response
        assert response.total_count == len(response.found_items)
        assert response.found_items[0].item_id == test_data["id"]
        assert response.found_items[0].item_name == test_data["name"]
        assert response.found_items[0].item_number == test_data["item_number"]
        assert response.found_items[0].is_active == test_data["active"]
        assert response.found_items[0].description == test_data["description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="items",
            params={
                "name[contains]": test_data["search_term"],
                "fields": '["id", "item-number", "name", "description", "active", "storage-quantity", "consumption-quantity"]',
            },
        )
