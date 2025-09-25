from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.delete_a_file import delete_a_file


def test_delete_a_file() -> None:
    """Tests that a file can be successfully deleted by the `delete_a_file` tool."""

    # Define test data:
    test_data = {
        "file_id": "1809734598969",
        "http_code": 204,
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.delete_a_file.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete a file
        response = delete_a_file(file_id=test_data["file_id"])

        # Ensure that delete_a_file() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"files/{test_data['file_id']}")
