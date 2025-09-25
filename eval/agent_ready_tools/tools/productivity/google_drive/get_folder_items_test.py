from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_folder_items import get_folder_items


def test_get_folder_items() -> None:
    """Test that the items from a Google Drive folder can be retrieved successfully."""

    # Define test data:
    test_data = {
        "folder_id": "1wSFKE1swdCm4CqKEQEuDO91ChdhnVIsX",
        "folder_item_name": "MyFolder",
        "folder_item_id": "1xDOCieVlJXJrhx6CXOBXofcmFJ4mZbxg",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_folder_items.get_google_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "files": [
                {
                    "name": test_data["folder_item_name"],
                    "id": test_data["folder_item_id"],
                }
            ]
        }

        # Get items from a folder
        response = get_folder_items(test_data["folder_id"])

        assert response

        assert response.folder_items[0].folder_item_name == test_data["folder_item_name"]
        assert response.folder_items[0].folder_item_id == test_data["folder_item_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="files",
            params={"q": f"'{test_data["folder_id"]}' in parents"},
        )
