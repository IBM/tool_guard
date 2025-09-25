from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_address import (
    oracle_fusion_get_supplier_addresses,
)


def test_oracle_fusion_get_supplier_address() -> None:
    """Test the getting of supplier's address details from Oracle Fusion using a mock client."""

    test_address_result = {
        "items": [
            {
                "SupplierAddressId": 434334,
                "Country": "United states",
                "AddressName": "HQ",
                "AddressLine1": "block 76/A",
                "AddressLine2": None,
                "City": "Texas",
                "State": "Texas",
                "PostalCode": None,
                "County": None,
                "Province": None,
            }
        ]
    }

    test_data = {"supplier_id": "434334"}

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_address.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_address_result
        response = oracle_fusion_get_supplier_addresses(supplier_id=test_data["supplier_id"])

        assert response
        assert response.content is not None
        assert (
            response.content[0].address_id == test_address_result["items"][0]["SupplierAddressId"]
        )
        assert response.content[0].country == test_address_result["items"][0]["Country"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/child/addresses",
            params={"limit": 20, "offset": 0},
        )
