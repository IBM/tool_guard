from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_folders import (
    FolderGoogleDrive,
    get_folders,
)


def test_get_all_folders() -> None:
    """Tests that folders can be retrieved by the `get_folders` tool in Google Drive."""

    # Define test data
    test_data = {
        "folder_name": "Saisharan1",
        "folder_id": "1QuLI06Oxw-i30Xmu4lq7nIJ7IPuL76gB",
        "limit": 100,
    }
    # Patch mock client instance.
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_folders.get_google_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock return value from Google Drive API
        mock_client.get_request.return_value = {
            "files": [{"name": test_data["folder_name"], "id": test_data["folder_id"]}],
        }

        # Run get_folders function
        response = get_folders(limit=100)

        # Expected output
        expected_folder = FolderGoogleDrive(
            folder_name=str(test_data["folder_name"]),
            folder_id=str(test_data["folder_id"]),
        )

        # Ensure that get_file_comments() has executed and returned proper values
        assert response.folders[0] == expected_folder
        assert response.limit == test_data["limit"]
        # Updated call expectation to match actual implementation
        mock_client.get_request.assert_called_once_with(
            entity="files",
            params={
                "q": "mimeType='application/vnd.google-apps.folder' and trashed = false",
                "pageSize": 100,
            },
        )
