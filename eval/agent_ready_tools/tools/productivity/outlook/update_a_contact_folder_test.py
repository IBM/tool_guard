from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.update_a_contact_folder import (
    update_a_contact_folder,
)


def test_update_a_contact_folder() -> None:
    """Verify that the `update_a_contact_folder` tool can successfully update an Outlook contact
    folder."""

    # Define test data:
    test_data = {
        "folder_id": 312321312,
        "name": "Test contact folder",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.update_a_contact_folder.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.update_request.return_value = {"displayName": test_data["name"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Update a contact folder
        response = update_a_contact_folder(
            original_contact_folder_id=test_data["folder_id"],
            new_contact_folder_name=test_data["name"],
        )

        # Ensure that update_a_contact_folder() executed and returned proper values
        assert response
        assert response.new_contact_folder_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/contactFolders/{test_data['folder_id']}",
            data={"displayName": test_data["name"]},
        )
