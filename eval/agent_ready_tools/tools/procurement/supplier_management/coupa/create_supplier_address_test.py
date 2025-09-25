from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_address import (
    coupa_create_supplier_address,
)


def test_coupa_create_supplier_address() -> None:
    """Tests create_supplier_address using a mock client."""

    test_data = {
        "supplier_id": 56,
        "street1": "Road no: 43, New town",
        "city": "New orleons",
        "country": "US",
        "postal_code": "897",
        "name": "temp address for branch",
        "street2": None,
        "state": None,
        "purpose": "branch",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_address.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": "56",
            "supplier-addresses": [
                {
                    "name": test_data["name"],
                    "street1": test_data["street1"],
                    "city": test_data["city"],
                    "postal-code": test_data["postal_code"],
                    "country": {"code": test_data["country"]},
                    "purposes": [{"name": test_data["purpose"]}],
                }
            ],
        }

        response = coupa_create_supplier_address(
            supplier_id=test_data["supplier_id"],
            street1=test_data["street1"],
            city=test_data["city"],
            country=test_data["country"],
            postal_code=test_data["postal_code"],
            name=test_data["name"],
            street2=test_data["street2"],
            state=test_data["state"],
            purpose=test_data["purpose"],
        ).content

        assert response
        assert response.supplier_id == 56

        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data["supplier_id"]}",
            payload={
                "supplier-addresses": [
                    {
                        "name": test_data["name"],
                        "street1": test_data["street1"],
                        "city": test_data["city"],
                        "postal-code": test_data["postal_code"],
                        "country": {"code": test_data["country"]},
                        "purposes": [{"name": test_data["purpose"]}],
                    }
                ]
            },
            params={"fields": '["id"]'},
        )
