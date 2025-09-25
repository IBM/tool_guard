from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_emergency_contact import (
    update_emergency_contact_oracle,
)


def test_update_emergency_contact_oracle() -> None:
    """Test the functionality of the `update_emergency_contact_oracle` function."""

    # Define test data:
    test_data = {
        "contact_uniq_id": "00020000000EACED00057708000110D94234EA290000004AAC",
        "contact_relationship_id": 300000281422381,
        "contact_type": "P",
        "email_address_id": 300000281422384,
        "email_address": "the.dragon@gmail.com",
        "phone_id": 300000281422383,
        "phone_number": "90001112345",
        "address_line1": "Church street",
        "person_address_usage_id": 300000281422386,
        "http_code": 200,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_emergency_contact.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "status_code": test_data["http_code"],
        }

        # Update emergency_contact
        response = update_emergency_contact_oracle(
            contact_uniq_id=test_data["contact_uniq_id"],
            contact_relationship_id=test_data["contact_relationship_id"],
            contact_type=test_data["contact_type"],
            email_address_id=test_data["email_address_id"],
            email_address=test_data["email_address"],
            phone_id=test_data["phone_id"],
            phone_number=test_data["phone_number"],
            address_line1=test_data["address_line1"],
            person_address_usage_id=test_data["person_address_usage_id"],
        )

        # Ensure that update_emergency_contact_oracle() returned proper list of address types
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            payload={
                "contactRelationships": [
                    {
                        "ContactRelationshipId": test_data["contact_relationship_id"],
                        "ContactType": test_data["contact_type"],
                    }
                ],
                "emails": [
                    {
                        "EmailAddressId": test_data["email_address_id"],
                        "EmailAddress": test_data["email_address"],
                    }
                ],
                "phones": [
                    {"PhoneId": test_data["phone_id"], "PhoneNumber": test_data["phone_number"]}
                ],
                "addresses": [
                    {
                        "AddressLine1": test_data["address_line1"],
                        "PersonAddrUsageId": test_data["person_address_usage_id"],
                    }
                ],
            },
            entity=f'hcmContacts/{test_data["contact_uniq_id"]}',
        )
