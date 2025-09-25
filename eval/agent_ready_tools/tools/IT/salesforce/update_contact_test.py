from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_contact import update_contact


def test_update_contact() -> None:
    """Tests that the `update_contact` function returns the expected response."""

    # Define test data:
    test_data = {
        "contact_id": "003gL000002VI16QAG",
        "last_name": "Kodali",
        "first_name": "Sivasri",
        "email": "sivasri@gmail.com",
        "phone_number": "1234567890",
        "title": "testing contact",
        "account_id": "001gL000005jzsVQAQ",
        "mailing_country": "India",
        "mailing_state": "Telangana",
        "mailing_city": "Hyderabad",
        "mailing_street": "Gachibowli, Hyderabad.",
        "mailing_postal_code": "500075",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_contact.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contact.update.return_value = test_response

        # Update contact
        response = update_contact(**test_data)

        # Ensure that update_contact() has executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Contact.update(test_data, test_data["contact_id"])
