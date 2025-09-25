from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.create_mail_folder import create_mail_folder


def test_create_mail_folder() -> None:
    """Test that a mail folder has been created successfully in Microsoft Outlook using the
    `create_mail_folder` tool."""

    # Define test data:
    test_data = {
        "display_name": "05 File Folder New",
        "http_code": 200,
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_mail_folder.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Create mail folder
        response = create_mail_folder(display_name=test_data["display_name"])

        # Ensure that create_mail_folder() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/mailFolders",
            data={"displayName": test_data["display_name"], "isHidden": False},
        )
