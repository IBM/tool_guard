from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.add_supplier_contact import (
    sap_s4_hana_add_supplier_contact,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    Department,
    FunctionOfPartner,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_sap_s4_hana_add_supplier_contact() -> None:
    """Verify that the `test_sap_s4_hana_add_supplier_contact` tool successfully adds a contact to a
    supplier in SAP S4 HANA."""

    # Define test data
    test_data: Dict[str, Any] = {
        "supplier_id": "10100001",
        "start_date": "2025-05-13",
        "person_function": "SALES_MANAGER",
        "person_department": "SALES",
        "phone_number": "0987012342",
        "phone_country_code": "91",
        "first_name": "Test",
        "last_name": "Person",
        "house_number": "1-A1",
        "street": "S1",
        "city": "Buffalo",
        "country": "US",
        "postal_code": "523456",
        "email_address": "charan@test.com",
        "person_id": "1212",
        "relationship_category": "BUR001",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.add_supplier_contact.get_sap_s4_hana_client"
    ) as mock_get_client, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.add_supplier_contact.sap_s4_hana_get_persons"
    ) as mock_get_persons, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.add_supplier_contact.sap_s4_hana_create_person"
    ) as mock_create_person:

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.post_request.return_value = {
            "d": {
                "BusinessPartnerCompany": test_data["supplier_id"],
                "BusinessPartnerPerson": test_data["person_id"],
            }
        }

        mock_get_persons.return_value = MagicMock(person_id=test_data["person_id"])
        mock_create_person_instance = MagicMock()
        mock_create_person_instance.content = MagicMock()
        mock_create_person_instance.content.person_id = test_data["person_id"]
        mock_create_person_instance.content.supplier_id = test_data["supplier_id"]
        mock_create_person.return_value = mock_create_person_instance

        response = sap_s4_hana_add_supplier_contact(
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            house_number=test_data["house_number"],
            street=test_data["street"],
            city=test_data["city"],
            country=test_data["country"],
            postal_code=test_data["postal_code"],
            email_address=test_data["email_address"],
            supplier_id=test_data["supplier_id"],
            start_date=test_data["start_date"],
            person_function=test_data["person_function"],
            person_department=test_data["person_department"],
            phone_number=test_data["phone_number"],
            phone_country_code=test_data["phone_country_code"],
        ).content

        # Ensure that sap_s4_hana_add_supplier_contact() executed and returned proper values
        assert response
        assert response.person_id == test_data["person_id"]
        assert response.supplier_id == test_data["supplier_id"]

        expected_payload = {
            "BusinessPartnerCompany": test_data["supplier_id"],
            "BusinessPartnerPerson": test_data["person_id"],
            "RelationshipCategory": test_data["relationship_category"],
            "to_ContactRelationship": {
                "BusinessPartnerCompany": test_data["supplier_id"],
                "ContactPersonFunction": FunctionOfPartner[test_data["person_function"]].value,
                "ContactPersonDepartment": Department[test_data["person_department"]].value,
                "PhoneNumber": test_data["phone_number"],
                "PhoneNumberExtension": test_data["phone_country_code"],
                "EmailAddress": test_data["email_address"],
            },
            "ValidityStartDate": iso_8601_to_sap_date(test_data["start_date"]),
        }

        mock_client.post_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_BusinessPartnerContact",
            payload=expected_payload,
        )
