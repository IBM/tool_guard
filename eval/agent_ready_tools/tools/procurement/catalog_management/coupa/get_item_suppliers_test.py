from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_suppliers import (
    CoupaItemSupplierDetails,
    CoupaSearchSuppliersResponse,
    coupa_get_item_suppliers,
)


def test_coupa_get_item_suppliers() -> None:
    """test the get_item_supplier tool."""

    # Define test data:
    test_data = {
        "item_id": "25",
        "name": "Insight",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.get_item_suppliers.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "supplier": {
                    "id": test_data["item_id"],
                    "name": test_data["name"],
                    "number": None,
                    "status": "active",
                }
            }
        ]

        response = coupa_get_item_suppliers(item_id=test_data["item_id"]).content

        # Ensure that get_item_suppliers() executed and returned proper values
        assert response
        assert response.total_count == 1
        assert isinstance(response, CoupaSearchSuppliersResponse)
        assert len(response.suppliers) == 1
        assert isinstance(response.suppliers[0], CoupaItemSupplierDetails)
        assert response.suppliers[0].id == int(test_data["item_id"])
        assert response.suppliers[0].name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name=f"items/{test_data['item_id']}/supplier_items",
            params={"fields": '[{"supplier":["id","name","number","status"]}]'},
        )
