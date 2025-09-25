from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier_contact import (
    oracle_fusion_create_supplier_contact,
)


def test_oracle_fusion_create_supplier_contact() -> None:
    """Tests oracle_fusion_create_supplier_contact using a mock client."""

    test_data = {
        "supplier_id": "300000025",
        "first_name": "Marius",
        "last_name": "Gracious",
        "phone_country_code": "1",
        "phone_area_code": "343",
        "phone_number": "4581236",
        "mobile_country_code": "91",
        "mobile_area_code": "234",
        "mobile_number": "7849856",
        "email": "Marius.g.ra.t@test.com",
        "supplier_contact_id": 34453,
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier_contact.get_oracle_fusion_client"
    ) as mock_oracle_client:
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {
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

        response = oracle_fusion_create_supplier_contact(
            supplier_id=test_data["supplier_id"],
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
        assert response.supplier_contact_id == test_data["supplier_contact_id"]
        assert response.email == test_data["email"]

        mock_client.post_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/child/contacts",
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
