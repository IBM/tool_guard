from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.create_a_folder import create_a_folder


def test_create_box_folder() -> None:
    """Test that a folder and subfolder can be created successfully, and then deletes them."""

    # Define test data:
    test_data = {
        "parent_folder_id": "0",
        "folder_name": "test_folder_creation_test",
        "folder_type": "folder",
        "folder_id": "31232131232",
        "http_code": 201,
        "message": "Folder created successfully.",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.create_a_folder.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["folder_id"],
            "type": test_data["folder_type"],
            "name": test_data["folder_name"],
        }

        # Copy a folder into a different folder
        response = create_a_folder(
            folder_name=test_data["folder_name"], parent_folder_id=test_data["parent_folder_id"]
        )

        # Ensure that create_a_folder() executed and returned proper values
        assert response
        assert response.folder
        assert response.folder.id == test_data["folder_id"]
        assert response.folder.name == test_data["folder_name"]
        assert response.folder.type == test_data["folder_type"]
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"folders",
            data={
                "name": test_data["folder_name"],
                "parent": {"id": test_data["parent_folder_id"]},
            },
        )
