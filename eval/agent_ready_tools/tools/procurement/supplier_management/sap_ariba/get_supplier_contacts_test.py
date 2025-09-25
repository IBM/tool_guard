from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_supplier_contacts import (
    ariba_get_supplier_contacts,
)


def test_ariba_get_supplier_contacts() -> None:
    """Verifies the list of supplier contacts was retrieved successfully by
    `get_supplier_contacts`"""

    # Define test data:
    test_data = {
        "sm_vendor_id": "S20042549",
        "first_name": "Test",
        "last_name": "Agent",
        "middle_name": "Watson",
        "email_address": "agent@ariba.com",
        "mobile_phone": "91\t9876543567",
        "office_phone": "91\t8765432789",
        "region": "IND",
        "contact_type": "Technical",
        "title": "Testing",
        "department": "",
        "timezone": "IST",
        "language": "en",
        "is_primary": True,
    }

    # Patch `get_ariba_client` to return a mock client

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_ariba.get_supplier_contacts.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "vendorDetails": [
                {
                    "vendorContactInfos": [
                        {
                            "firstName": test_data["first_name"],
                            "lastName": test_data["last_name"],
                            "middleName": test_data["middle_name"],
                            "email": test_data["email_address"],
                            "telephone": test_data["office_phone"],
                            "title": test_data["title"],
                            "mobilePhone": test_data["mobile_phone"],
                            "regions": test_data["region"],
                            "type": test_data["contact_type"],
                            "locale": test_data["language"],
                            "timeZoneId": test_data["timezone"],
                            "departments": test_data["department"],
                            "primary": test_data["is_primary"],
                        }
                    ]
                }
            ]
        }

        response = ariba_get_supplier_contacts(sm_vendor_id=test_data["sm_vendor_id"]).content

        # Ensure that get_supplier_contacts() executed and returned proper values

        assert response
        assert response.contact_details[0].first_name == test_data["first_name"]
        assert response.contact_details[0].last_name == test_data["last_name"]
        assert response.contact_details[0].middle_name == test_data["middle_name"]
        assert response.contact_details[0].email_address == test_data["email_address"]
        assert response.contact_details[0].mobile_phone == test_data["mobile_phone"]
        assert response.contact_details[0].office_phone == test_data["office_phone"]
        assert response.contact_details[0].region == test_data["region"]
        assert response.contact_details[0].contact_type == test_data["contact_type"]
        assert response.contact_details[0].title == test_data["title"]
        assert response.contact_details[0].department == test_data["department"]
        assert response.contact_details[0].timezone == test_data["timezone"]
        assert response.contact_details[0].language == test_data["language"]
        assert response.contact_details[0].is_primary == test_data["is_primary"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint="supplierdatapagination/v4/prod/vendorContactsRequests",
            payload={"smVendorIds": [test_data["sm_vendor_id"]]},
        )
