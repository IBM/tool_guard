from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.add_a_comment_google_drive import (
    add_a_comment_google_drive,
)


def test_add_a_comment() -> None:
    """Verifies that the `add_a_comment` tool can successfully add a comment to a file in Google
    Drive."""

    # Define test data
    test_data = {
        "file_id": "1C08stJWPu-OuKxf9nkwxiujOLKhEwREiOxZIq28T0eY",
        "content": "New Comment 16/5",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.add_a_comment_google_drive.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.post_request.return_value = {"content": test_data["content"]}

        # Add a comment to the file
        response = add_a_comment_google_drive(
            file_id=test_data["file_id"],
            content=test_data["content"],
        )

        # Ensure that add_a_comment() executed and returned proper values
        assert response
        assert response.content == test_data["content"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}/comments",
            payload={
                "name": test_data["file_id"],
                "content": test_data["content"],
            },
            params={"fields": "*"},
        )
