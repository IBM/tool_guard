from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.copy_a_file_into_another_box_folder import (
    copy_a_file_into_another_box_folder,
)


def test_copy_a_file_into_another_box_folder() -> None:
    """Verifies that the `copy_a_file_into_another_box_folder` tool can successfully copy a file
    into another folder in Box."""

    # Define test data:
    test_data = {
        "file_id": "1813043288424",
        "source_folder_name": "SK_source",
        "source_folder_id": "313315103035",
        "target_folder_id": "313314381597",
        "http_code": 201,
        "message": "File copied successfully.",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.copy_a_file_into_another_box_folder.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # copy a file into another box folder
        response = copy_a_file_into_another_box_folder(
            file_id=test_data["file_id"], target_folder_id=test_data["target_folder_id"]
        )

        # Ensure that copy_a_file_into_another_box_folder() executed and returned proper values
        assert response
        assert response.file.http_code == test_data["http_code"]
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}/copy",
            data={"parent": {"id": test_data["target_folder_id"]}},
        )
