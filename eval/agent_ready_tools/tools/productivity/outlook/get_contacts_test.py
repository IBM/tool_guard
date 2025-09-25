from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_contacts import Contacts, get_contacts


def test_get_contacts() -> None:
    """Tests that the contacts can be retrieved by the `get_contacts` tool in Microsoft Outlook."""

    # Define test data
    test_data: dict[str, str] = {
        "contact_name": "Super Man",
        "email_address": "s.man1@gmail.com",
        "folder_name": "EmptyFolderTest",
        "phone_number": "3344343434",
        "user_name": "user@example.com",
    }
    limit = 100
    skip = 0
    output_limit = None
    output_skip = None

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_contacts.get_microsoft_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "displayName": test_data["contact_name"],
                    "emailAddresses": [{"address": test_data["email_address"]}],
                    "categories": [test_data["folder_name"]],
                    "mobilePhone": test_data["phone_number"],
                }
            ],
            "limit": limit,
            "skip": skip,
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_contacts(email_address=test_data["email_address"], limit=limit, skip=skip)
        # Verify that the contact details matches the expected data
        expected_contact = Contacts(
            contact_name=test_data["contact_name"],
            email_address=test_data["email_address"],
            folder_name=test_data["folder_name"],
            phone_number=test_data["phone_number"],
        )

        assert response.contacts_list[0] == expected_contact
        assert response.limit == output_limit
        assert response.skip == output_skip

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/contacts",
            params={
                "$top": limit,
                "$filter": f"emailAddresses/any(a:a/address eq '{test_data['email_address']}')",
            },
        )
