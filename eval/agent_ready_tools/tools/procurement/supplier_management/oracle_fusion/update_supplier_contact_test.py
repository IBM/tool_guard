from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_contact import (
    oracle_fusion_update_supplier_contact,
)


def test_oracle_fusion_update_supplier_contacts() -> None:
    """Test that the `oracle_fusion_update_supplier_contact` function updates contact details."""

    # Define test data
    test_data = {
        "supplier_id": "300100153044388",
        "supplier_contact_id": "300000025229266",
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
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_contact.get_oracle_fusion_client"
    ) as mock_oracle_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = {
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

        # Call the function
        response = oracle_fusion_update_supplier_contact(
            supplier_id=test_data["supplier_id"],
            supplier_contact_id=test_data["supplier_contact_id"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            phone_country_code=test_data["phone_country_code"],
            phone_area_code=test_data["phone_area_code"],
            phone_number=test_data["phone_number"],
            mobile_country_code=test_data["mobile_country_code"],
            mobile_area_code=test_data["mobile_area_code"],
            mobile_number=test_data["mobile_number"],
            email=test_data["email"],
        ).content

        assert response
        assert response.email == test_data["email"]
        assert response.first_name == test_data["first_name"]
        assert response.last_name == test_data["last_name"]
        assert response.phone_number == test_data["phone_number"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data["supplier_id"]}/child/contacts/{test_data['supplier_contact_id']}",
            payload={
                "FirstName": test_data["first_name"],
                "LastName": test_data["last_name"],
                "PhoneCountryCode": test_data["phone_country_code"],
                "PhoneAreaCode": test_data["phone_area_code"],
                "PhoneNumber": test_data["phone_number"],
                "MobileCountryCode": test_data["mobile_country_code"],
                "MobileAreaCode": test_data["mobile_area_code"],
                "MobileNumber": test_data["mobile_number"],
                "Email": test_data["email"],
            },
        )
