from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_revisions import get_revisions


def test_get_revisions() -> None:
    """Tests that the revisions can be retrieved successfully using `get_revisions` tool."""

    # Define test data
    test_data = {
        "file_id": "032f4d85-b7fe-4d6a-9ff2-502ea7b0c535",
        "revision_id": "7",
        "mime_type": "application/vnd.google-apps.spreadsheet",
        "kind": "drive#revision",
        "modified_time": "2025-04-14T12:01:20.935Z",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_revisions.get_google_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "revisions": [
                {
                    "id": test_data["revision_id"],
                    "mimeType": test_data["mime_type"],
                    "kind": test_data["kind"],
                    "modifiedTime": test_data["modified_time"],
                }
            ]
        }

        # Get Revisions
        response = get_revisions(file_id=test_data["file_id"])

        # Ensure that get_revisions() executed and returned proper values
        assert response
        assert response.revisions[0].revision_id == test_data["revision_id"]
        assert response.revisions[0].mime_type == test_data["mime_type"]
        assert response.revisions[0].kind == test_data["kind"]
        assert response.revisions[0].modified_time == test_data["modified_time"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data["file_id"]}/revisions",
        )
