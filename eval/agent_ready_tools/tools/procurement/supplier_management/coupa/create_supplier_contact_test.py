from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_contact import (
    coupa_create_supplier_contact,
)


def test_coupa_create_supplier_contact() -> None:
    """Tests coupa_create_supplier_contact using a mock client."""

    test_data = {
        "supplier_id": 2,
        "email": "test101@ibm.com",
        "first_name": "Test101",
        "last_name": "Watsonx",
        "country_code": None,
        "area_code": None,
        "phone_number": None,
        "purpose": "executive_contact",
        "contact_id": "3234",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_contact.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_data["supplier_id"],
            "contacts": [
                {
                    "id": test_data["contact_id"],
                    "email": test_data["email"],
                    "name-given": test_data["first_name"],
                    "name-family": test_data["last_name"],
                    "phone-work": {
                        "country-code": test_data["country_code"],
                        "area-code": test_data["area_code"],
                        "number": test_data["phone_number"],
                    },
                    "purposes": [{"name": test_data["purpose"]}],
                }
            ],
        }

        response = coupa_create_supplier_contact(
            supplier_id=test_data["supplier_id"],
            email=test_data["email"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            purpose=test_data["purpose"],
        ).content

        assert response
        assert response.supplier_id == 2

        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data["supplier_id"]}",
            payload={
                "contacts": [
                    {
                        "email": test_data["email"],
                        "name-given": test_data["first_name"],
                        "name-family": test_data["last_name"],
                        "phone-work": {},
                        "purposes": [{"name": test_data["purpose"]}],
                    }
                ]
            },
            params={"fields": '["id"]'},
        )
