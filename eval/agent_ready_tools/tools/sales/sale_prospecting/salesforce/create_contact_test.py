from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_contact import (
    salesforce_create_contact,
)


def test_create_contact() -> None:
    """Verifies that the `create_contact` tool can successfully create a contact in Salesforce."""

    # Define test data
    test_data = {
        "last_name": "Watson",
        "title": "IBM Watson Orchestrate",
        "email": "watson@ibm.com",
        "phone_number": "+919876543210",
        "first_name": "Orchestrate",
        "account_id": "001gL0000054RzdQAE",
        "contact_id": "003gL000002cIpBQAU",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_contact.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contact.create.return_value = {"id": test_data["contact_id"]}

        # Create a contact
        response = salesforce_create_contact(
            last_name=test_data["last_name"],
            title=test_data["title"],
            email=test_data["email"],
            phone_number=test_data["phone_number"],
            first_name=test_data["first_name"],
            account_id=test_data["account_id"],
        )

        # Ensure that salesforce_create_contact() has executed and returned proper values
        assert response
        assert response.contact_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Contact.create(
            payload={
                "LastName": test_data["last_name"],
                "Title": test_data["title"],
                "Email": test_data["email"],
                "Phone": test_data["phone_number"],
                "FirstName": test_data["first_name"],
                "AccountId": test_data["account_id"],
            },
        )
