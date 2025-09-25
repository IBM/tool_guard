from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.delete_a_folder import delete_a_folder


def test_delete_a_folder() -> None:
    """Test that a folder can be deleted successfully by the `delete_a_folder` tool."""

    # Define test data:
    test_data = {
        "folder_id": "21312321",
        "http_code": 204,
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.delete_a_folder.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete a folder
        response = delete_a_folder(folder_id=test_data["folder_id"])

        # Ensure that delete_a_folder() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"folders/{test_data['folder_id']}", params={"recursive": True}
        )
