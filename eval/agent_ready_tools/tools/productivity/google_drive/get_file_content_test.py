from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_file_content_google_drive import (
    get_file_content_google_drive,
)


def test_get_file_content_google_drive() -> None:
    """Tests that the contents of the file are retrieved successfully by the
    `get_file_content_google_drive` tool."""

    # Define test data
    test_data = {
        "file_content": "Mock file content",
        "file_id": "1GoN6dLYBiMUKl6FUDFW9nAv3BoLDW8Ob",
        "file_type": None,
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_file_content_google_drive.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.get_request.return_value = (
            test_data["file_content"],
            {},  # Mock response to return a tuple with content and headers
        )

        # Get File content
        response = get_file_content_google_drive(
            file_id=test_data["file_id"], file_type=test_data["file_type"]
        )

        # Ensure that get_file_content_google_drive() executed and returned proper values
        assert response
        assert response.content == test_data["file_content"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}", params={"alt": "media"}, content=True
        )
