from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_tax_registrations import (
    coupa_get_supplier_tax_registrations,
)


def test_coupa_get_supplier_tax_registrations() -> None:
    """Test get supplier tax registrations."""
    test_tax_registrations = {
        "supplier-addresses": [
            {
                "tax-registrations": [
                    {
                        "id": "22",
                        "number": "100",
                        "active": True,
                        "country": {"name": "United States"},
                    },
                    {
                        "id": "23242",
                        "number": "777",
                        "active": True,
                        "country": {"name": "Antarctica"},
                    },
                ]
            },
            {"tax-registrations": []},
            {"tax-registrations": []},
        ]
    }

    supplier_id = "4"

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_tax_registrations.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = test_tax_registrations

        response = coupa_get_supplier_tax_registrations(supplier_id=supplier_id).content

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{supplier_id}",
            params={
                "fields": '[{"supplier_addresses":[{"tax_registrations":["id","number","active",{"country":["name"]}]}]}]'
            },
        )
