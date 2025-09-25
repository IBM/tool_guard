from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_contact import (
    coupa_update_supplier_contact,
)


def test_coupa_update_supplier_contact() -> None:
    """Test that the supplier contact details were updated by `update_supplier_contact` tool."""

    # Define test data
    test_data = {
        "supplier_id": 1234,
        "contact_id": 1300,
        "email": "tester.qa@ibm.com",
        "first_name": "Test101",
        "last_name": "Watsonx",
        "country_code": "91",
        "area_code": "40",
        "phone_number": "9822998765",
        "purpose_name": None,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_contact.get_coupa_client"
    ) as mock_coupa_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_data["supplier_id"],
            "primary-contact": {"email": test_data["email"]},
        }

        # Call the function under test
        response = coupa_update_supplier_contact(
            supplier_id=test_data["supplier_id"],
            contact_id=test_data["contact_id"],
            email=test_data["email"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            country_code=test_data["country_code"],
            area_code=test_data["area_code"],
            phone_number=test_data["phone_number"],
            purpose_name=test_data["purpose_name"],
        ).content

        # Ensure that coupa_update_supplier_contact() executed and returned proper values
        assert response.id == test_data["supplier_id"]
        assert response.contact_email == test_data["email"]
        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}",
            payload={
                "contacts": [
                    {
                        "id": test_data["contact_id"],
                        "name-given": test_data["first_name"],
                        "name-family": test_data["last_name"],
                        "email": test_data["email"],
                        "phone-work": {
                            "country-code": test_data["country_code"],
                            "area-code": test_data["area_code"],
                            "number": test_data["phone_number"],
                        },
                    }
                ]
            },
            params={"fields": '["id","number","status","name",{"primary_contact":["email"]}]'},
        )
