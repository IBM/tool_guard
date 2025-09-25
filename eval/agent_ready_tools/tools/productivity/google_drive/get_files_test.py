from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_files import Files, get_files


def test_get_files() -> None:
    """Tests that the files can be retrieved by the `get_files` tool in Google Drive."""

    # Define test data
    test_data = {
        "file_id": "1tJrN3N3pVnCW3qxk7RjS9Yp38yGMCTQA",
        "file_name": "Test Folder1",
        "file_type": "application/vnd.google-apps.folder",
        "kind": "drive#file",
        "output_nextPageToken": "~!!~AI9FV7SoP3YlCVSM-4niqPJFUTWRMfZFPxOvLtvjXH2u8WV_be69Myn3r3DJFTCN6kREc7EwqYyWg09yTIMIpl9NvGnZyebda4CcGSDRjHmU34aj_hgmAHxOZwKwGG2bgqLJzc2MVT0mOK4L98Hz8U7tBSMhiWTiC-3RvOpK2q8Y-kZnyZ_uq3yUqc3DZYJeEXHOkY3kF8ItLF7UDuU-1yBix5Hx4jQw-7yagnV5TLCmyBYYv5Vo4QwmrPYwN2054U4WSEWeG_aECwCvIXm9MpnTUS7Tjkl8kLdODlqyFSIaqChJFLfjgCDGtmuJeONyZkyY_gA8f1pz",
    }
    limit = 20

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_files.get_google_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "files": [
                {
                    "id": test_data["file_id"],
                    "name": test_data["file_name"],
                    "mimeType": test_data["file_type"],
                    "kind": test_data["kind"],
                }
            ],
            "nextPageToken": test_data["output_nextPageToken"],
        }

        # Call the function
        response = get_files(
            file_name=test_data["file_name"],
            limit=limit,
            next_page_token=test_data["output_nextPageToken"],
        )

        expected_files = Files(
            file_id=str(test_data["file_id"]),
            file_name=str(test_data["file_name"]),
            file_type=str(test_data["file_type"]),
            kind=str(test_data["kind"]),
        )

        # Verify that the file details matches the expected data

        assert response.files[0] == expected_files
        assert response.limit == limit
        assert response.next_page_token == test_data["output_nextPageToken"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="files",
            params={
                "pageSize": limit,
                "q": f"name = '{test_data["file_name"]}'",
                "pageToken": test_data["output_nextPageToken"],
            },
        )
