from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_mail_folders import get_mail_folders


def test_get_mail_folders() -> None:
    """Tests that the mail folders can be retrieved successfully."""

    # Define test data:
    test_data = {
        "folder_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMTk4NgAuAAAAAACc41e7EpqATZaoltx0URUoAQD-yalyWcFZS7k3FwN9Rv9bAAblxQxkAAA=",
        "display_name": "Archival 01",
        "total_item_count": 3,
        "is_hidden": False,
        "include_hidden_folders": True,
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_mail_folders.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["folder_id"],
                    "displayName": test_data["display_name"],
                    "totalItemCount": test_data["total_item_count"],
                    "isHidden": test_data["is_hidden"],
                }
            ]
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Get Mail Folders
        response = get_mail_folders(include_hidden_folders=test_data["include_hidden_folders"])

        # Ensure that get_mail_folders() executed and returned proper values
        assert response
        assert len(response.mail_folders)
        assert response.mail_folders[0].folder_id == test_data["folder_id"]
        assert response.mail_folders[0].display_name == test_data["display_name"]
        assert response.mail_folders[0].total_item_count == test_data["total_item_count"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/mailFolders",
            params={"includeHiddenFolders": test_data["include_hidden_folders"], "$top": 10},
        )
