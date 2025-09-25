from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.create_a_contact import create_a_contact


def test_create_a_contact() -> None:
    """Verifies that the `create_a_contact` tool is able to create a contact successfully in
    Microsoft Outlook."""

    # Define test data:
    test_data = {
        "first_name": "testing",
        "last_name": "k",
        "email_address": "test88@example.com",
        "phone_number": "373929988",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_a_contact.get_microsoft_client"
    ) as mock_outlook_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "emailAddresses": [{"address": test_data["email_address"]}],
            "givenName": test_data["first_name"],
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Create a contact
        response = create_a_contact(
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            email_address=test_data["email_address"],
            phone_number=test_data["phone_number"],
        )

        # Ensure that create_a_contact() executed and returned proper values
        assert response
        assert response.email_address == test_data["email_address"]
        assert response.first_name == test_data["first_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/contacts",
            data={
                "givenName": test_data["first_name"],
                "surname": test_data["last_name"],
                "emailAddresses": [{"address": test_data["email_address"]}],
                "mobilePhone": test_data["phone_number"],
            },
        )
