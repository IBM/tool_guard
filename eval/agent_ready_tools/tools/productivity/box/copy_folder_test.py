from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.copy_folder import copy_folder


def test_copy_folder() -> None:
    """Verify that the `copy_folder` tool can successfully copy a folder into another folder in
    Box."""

    # Define test data:
    test_data = {
        "source_folder_id": "216911298723",
        "target_folder_id": "170631251991",
        "http_code": 201,
        "message": "Folder copied successfully.",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.copy_folder.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Copy a folder to a different folder
        response = copy_folder(
            source_folder_id=test_data["source_folder_id"],
            target_folder_id=test_data["target_folder_id"],
        )

        # Ensure that copy_folder() executed and returned proper values
        assert response
        assert response.folder.http_code == test_data["http_code"]
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"folders/{test_data['source_folder_id']}/copy",
            data={"parent": {"id": test_data["target_folder_id"]}},
        )
