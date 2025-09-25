from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    Department,
    FunctionOfPartner,
    S4HanaBusinessPartner,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_contacts import (
    sap_s4_hana_get_supplier_contacts,
)


def test_get_supplier_contacts() -> None:
    """Test that the `sap_s4_hana_get_supplier_contacts` function returns the expected response."""

    test_data = {
        "supplier_id": "10100001",
        "business_partner_id": "10100001",
        "contact_person": "61",
        "relationship": "BUR001",
        "validity_from": "2025-05-08",
        "validity_to": "9999-12-31",
        "contact_person_function": "0003",
        "department": "0003",
        "phone_number": "0987 1234",
        "phone_number_extension": "12",
        "email_address": "test123@10100001.com",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_contacts.get_business_partner_id_of_supplier"
    ) as mock_business_partner, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_contacts.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "BusinessPartner": test_data["business_partner_id"],
                            "BusinessPartnerPerson": test_data["contact_person"],
                            "RelationshipCategory": test_data["relationship"],
                            "ValidityStartDate": test_data["validity_from"],
                            "ValidityEndDate": test_data["validity_to"],
                            "to_ContactRelationship": {
                                "ContactPersonFunction": test_data["contact_person_function"],
                                "ContactPersonDepartment": test_data["department"],
                                "PhoneNumber": test_data["phone_number"],
                                "PhoneNumberExtension": test_data["phone_number_extension"],
                                "EmailAddress": test_data["email_address"],
                            },
                        }
                    ]
                }
            }
        }
        mock_client.get_business_partner_id_of_supplier.return_value = {
            "response": {"d": {"results": [{"BusinessPartner": test_data["business_partner_id"]}]}}
        }
        # Ensure the mock returns the correct business partner ID
        mock_business_partner.return_value = ToolResponse(
            success=True,
            message="Success",
            content=S4HanaBusinessPartner(business_partner_id=test_data["business_partner_id"]),
        )

        response = sap_s4_hana_get_supplier_contacts(supplier_id=test_data["supplier_id"]).content
        assert response
        assert response.contact_details[0].contact_person == test_data["contact_person"]
        assert response.contact_details[0].relationship == test_data["relationship"]
        assert response.contact_details[0].validity_from == test_data["validity_from"]
        assert response.contact_details[0].validity_to == test_data["validity_to"]
        assert (
            response.contact_details[0].contact_person_function
            == FunctionOfPartner(test_data["contact_person_function"]).name
        )
        assert response.contact_details[0].department == Department(test_data["department"]).name
        assert response.contact_details[0].phone_number == test_data["phone_number"]
        assert (
            response.contact_details[0].phone_number_extension
            == test_data["phone_number_extension"]
        )
        assert response.contact_details[0].email_address == test_data["email_address"]

        mock_client.get_request.assert_any_call(
            entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{test_data["business_partner_id"]}')/to_BusinessPartnerContact",
            expand_expr="to_ContactRelationship,to_ContactAddress",
            params={"$top": 20, "$skip": 0},
        )
