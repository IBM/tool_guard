from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.get_folder_files import get_folder_files


def test_get_folder_files() -> None:
    """Test that the folder items can be retrieved successfully."""

    # Define test data:
    test_data = {
        "folder_id": "TestFoler",
        "file_id": 291570230083,
        "file_type": "file",
        "file_name": "TestFile",
        "limit": 20,
        "offset": 0,
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.get_folder_files.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "entries": [
                {
                    "type": test_data["file_type"],
                    "id": test_data["file_id"],
                    "name": test_data["file_name"],
                }
            ],
            "total_count": 1,
            "offset": test_data["offset"],
            "limit": test_data["limit"],
        }

        # Get folder files
        response = get_folder_files(folder_id=test_data["folder_id"])

        # Ensure that get_folder_files() executed and returned proper values
        assert response
        assert response.total_count >= 1
        assert len(response.entries)
        assert response.entries[0].id == test_data["file_id"]
        assert response.entries[0].type == test_data["file_type"]
        assert response.entries[0].name == test_data["file_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"folders/{test_data['folder_id']}/items",
            params={"limit": test_data["limit"], "offset": test_data["offset"]},
        )
