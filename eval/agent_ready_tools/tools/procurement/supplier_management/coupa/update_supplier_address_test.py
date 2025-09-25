from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_address import (
    coupa_update_supplier_address,
)


def test_coupa_update_supplier_address() -> None:
    """Tests `update_supplier_address` using a mock client."""

    test_data = {
        "supplier_id": 1,
        "address_id": "229031",
        "street1": "Road no: 43, New town",
        "city": "New orleons",
        "country": None,
        "postal_code": None,
        "name": None,
        "street2": None,
        "state": None,
        "purpose": "Mailing",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_address.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_data["supplier_id"],
            "supplier-addresses": [
                {
                    "name": test_data["name"],
                    "id": test_data["address_id"],
                    "street1": test_data["street1"],
                    "street2": test_data["street2"],
                    "city": test_data["city"],
                    "state": test_data["state"],
                    "postal-code": test_data["postal_code"],
                    "country": {"code": test_data["country"]},
                    "purposes": [{"name": test_data["purpose"]}],
                }
            ],
        }

        response = coupa_update_supplier_address(
            supplier_id=test_data["supplier_id"],
            address_id=test_data["address_id"],
            street1=test_data["street1"],
            city=test_data["city"],
            purpose=test_data["purpose"],
        ).content

        assert response
        assert response.supplier_id == 1

        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data["supplier_id"]}",
            payload={
                "supplier-addresses": [
                    {
                        "id": test_data["address_id"],
                        "street1": test_data["street1"],
                        "city": test_data["city"],
                        "purposes": [{"name": test_data["purpose"]}],
                    }
                ]
            },
            params={"fields": '["id"]'},
        )
