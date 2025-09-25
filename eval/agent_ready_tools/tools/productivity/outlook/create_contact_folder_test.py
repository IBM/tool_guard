from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.create_contact_folder import create_contact_folder


def test_create_contact_folder() -> None:
    """Verifies that the `create_contact_folder` tool is able to create a contact successfully in
    Microsoft Outlook."""

    # Define test data:
    test_data = {
        "folder_id": "1jhjwheuddfaf",
        "name": "Important contacts HS1231s",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_contact_folder.get_microsoft_client"
    ) as mock_outlook_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.post_request.return_value = {"id": test_data["folder_id"], "status_code": 201}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Create a contact
        response = create_contact_folder(display_name=test_data["name"])

        # Ensure that create_a_contact() executed and returned proper values
        assert response
        assert response.folder_id == test_data["folder_id"]
        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data['user_name']}/contactFolders",
            data={
                "displayName": test_data["name"],
            },
        )
