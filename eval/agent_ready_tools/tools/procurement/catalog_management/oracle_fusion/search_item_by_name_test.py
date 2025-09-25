from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.search_item_by_name import (
    oracle_fusion_search_item_by_name,
)


def test_oracle_fusion_search_item_by_name() -> None:
    """Test that the `oracle_fusion_search_item_by_name` function returns expected item details."""

    # Define test data
    search_term = "macbook"
    test_data = {
        "item_id": 300000025339742,
        "item_number": "Macbook Pro 15 inch",
        "item_class": "CI Laptops",
        "item_description": "macbook pro 15 inch for Wxo test",
        "primary_uom_value": "Ea",
        "organization_code": "001",
        "lifecycle_phase": "Active",
        "item_status": "Active",
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.search_item_by_name.get_oracle_fusion_client"
    ) as mock_get_client:
        # Create a mock client
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "ItemId": test_data["item_id"],
                    "ItemNumber": test_data["item_number"],
                    "ItemClass": test_data["item_class"],
                    "ItemDescription": test_data["item_description"],
                    "PrimaryUOMValue": test_data["primary_uom_value"],
                    "OrganizationCode": test_data["organization_code"],
                    "LifecyclePhaseValue": test_data["lifecycle_phase"],
                    "ItemStatusValue": test_data["item_status"],
                }
            ]
        }

        # Call the function
        response = oracle_fusion_search_item_by_name(search_term=search_term).content

        assert response
        assert response[0].item_id == test_data["item_id"]
        assert response[0].item_number == test_data["item_number"]
        assert response[0].item_class == test_data["item_class"]
        assert response[0].item_description == test_data["item_description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name="itemsV2", params={"q": f"ItemDescription LIKE '%{search_term}%'"}
        )
