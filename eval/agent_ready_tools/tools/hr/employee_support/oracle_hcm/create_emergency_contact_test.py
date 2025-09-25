from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_emergency_contact import (
    create_emergency_contact,
)


def test_create_emergency_contact() -> None:
    """Test that the `create_emergency_contact` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": 999999999999999,
        "person_number": "6561",
        "country": "US",
        "first_name": "John",
        "last_name": "Smith",
        "contact_type_code": "A",
        "email_address": "the.dino@gmail.com",
        "phone_number": "90001112345",
        "phone_type": "HM",
        "email_type": "H1",
        "contact_relationship_id": 300000307338133,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_emergency_contact.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "PersonId": test_data["person_id"],
            "PersonNumber": test_data["person_number"],
            "contactRelationships": {
                "items": [{"ContactRelationshipId": test_data["contact_relationship_id"]}]
            },
        }

        # Create emergency contact
        response = create_emergency_contact(
            person_id=test_data["person_id"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            contact_type=test_data["contact_type_code"],
            country=test_data["country"],
            email_address=test_data["email_address"],
            phone_number=test_data["phone_number"],
        )

        # Ensure that create_emergency_contact() executed and returned proper values
        assert response
        assert response.person_id == test_data["person_id"]
        assert response.person_number == test_data["person_number"]
        assert response.contact_relationship_id == [test_data["contact_relationship_id"]]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="hcmContacts",
            payload={
                "names": [
                    {
                        "FirstName": test_data["first_name"],
                        "LastName": test_data["last_name"],
                        "LegislationCode": test_data["country"],
                    }
                ],
                "contactRelationships": [
                    {
                        "RelatedPersonId": test_data["person_id"],
                        "ContactType": test_data["contact_type_code"],
                        "EmergencyContactFlag": True,
                    }
                ],
                "emails": [
                    {
                        "EmailAddress": test_data["email_address"],
                        "EmailType": test_data["email_type"],
                    }
                ],
                "phones": [
                    {
                        "PhoneNumber": test_data["phone_number"],
                        "PhoneType": test_data["phone_type"],
                    }
                ],
            },
        )
