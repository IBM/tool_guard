from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.get_folder_details_by_name import (
    get_folder_details_by_name,
)


def test_get_folder_details_by_name() -> None:
    """Test that file or folder details can be retrieved successfully."""

    # Define test data:
    test_data = {
        "folder_name": "Wxo_Presentations",
        "folder_type": "public",
        "file_id": "9999",
        "file_name": "Notebook On HowTo",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.get_folder_details_by_name.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "entries": [
                {
                    "id": test_data["file_id"],
                    "name": test_data["file_name"],
                    "type": "file",
                    "created_by": {"name": "John Smith"},
                    "modified_by": {"name": "Rachel Smith"},
                    "owned_by": {"name": "Micah Smith"},
                    "parent": {"name": "Presentations"},
                    "path_collection": {"entries": [{"name": "wxo"}]},
                }
            ],
        }

        # Get comments for file
        response = get_folder_details_by_name(name=test_data["folder_name"]).details[0]

        # Ensure that get_folder_details_by_name() executed and returned proper values
        assert response
        assert response.id == test_data["file_id"]
        assert response.name == test_data["file_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="search",
            params={"query": f"{test_data['folder_name']}", "type": "folder"},
        )
