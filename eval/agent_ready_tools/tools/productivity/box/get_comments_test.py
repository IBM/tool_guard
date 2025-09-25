from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.get_comments import get_comments


def test_get_comments() -> None:
    """Test that all the comments can be retrieved successfully."""

    # Define test data:
    test_data = {
        "comment": "Hello world",
        "comment_id": "651643221",
        "created_by": "csprod2",
        "created_date": "2025-03-19T23:28:22-07:00",
        "file_id": "1808636123058",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.get_comments.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "entries": [
                {
                    "id": test_data["comment_id"],
                    "message": test_data["comment"],
                    "created_by": {"name": test_data["created_by"]},
                    "created_at": test_data["created_date"],
                }
            ],
        }

        # Get comments for file
        response = get_comments(file_id=test_data["file_id"])

        # Ensure that get_comments() executed and returned proper values
        assert response
        assert response.comments_list[0].comment == test_data["comment"]
        assert response.comments_list[0].comment_id == test_data["comment_id"]
        assert response.comments_list[0].created_by == test_data["created_by"]
        assert response.comments_list[0].created_date == test_data["created_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}/comments"
        )
