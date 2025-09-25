from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_contacts import (
    oracle_fusion_get_supplier_contacts,
)


def test_oracle_fusion_get_supplier_contacts() -> None:
    """Test that the `oracle_fusion_get_supplier_contacts` function returns expected contact
    details."""

    # Define test data
    test_data = {
        "supplier_id": "300100153044388",
        "supplier_contact_id": 300000025229266,
        "first_name": "Alice",
        "last_name": "Smith",
        "phone_country_code": "+91",
        "phone_area_code": "345",
        "phone_number": "9876543210",
        "mobile_country_code": "+91",
        "mobile_area_code": "2",
        "mobile_number": "9123456789",
        "email": "test.user@example.com",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_contacts.get_oracle_fusion_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "SupplierContactId": test_data["supplier_contact_id"],
                    "FirstName": test_data["first_name"],
                    "LastName": test_data["last_name"],
                    "PhoneCountryCode": test_data["phone_country_code"],
                    "PhoneAreaCode": test_data["phone_area_code"],
                    "PhoneNumber": test_data["phone_number"],
                    "MobileCountryCode": test_data["mobile_country_code"],
                    "MobileAreaCode": test_data["mobile_area_code"],
                    "MobileNumber": test_data["mobile_number"],
                    "Email": test_data["email"],
                }
            ]
        }

        # Call the function
        response = oracle_fusion_get_supplier_contacts(supplier_id=test_data["supplier_id"]).content

        assert response
        assert response[0].supplier_contact_id == test_data["supplier_contact_id"]
        assert response[0].email == test_data["email"]
        assert response[0].first_name == test_data["first_name"]
        assert response[0].last_name == test_data["last_name"]
        assert response[0].phone_number == test_data["phone_number"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data["supplier_id"]}/child/contacts",
            params={"limit": 20, "offset": 0},
        )
