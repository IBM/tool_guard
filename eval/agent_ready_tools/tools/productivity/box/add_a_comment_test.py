from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.add_a_comment import add_a_comment


def test_add_a_comment() -> None:
    """Test that adds a comment to a Box file successfully using the `add_a_comment` tool."""

    # Define test data:
    test_data = {
        "file_id": "How_to_Scrumble_Eggs",
        "comment_name": "Test comments(25/03)",
        "comment_id": "313315103035",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.add_a_comment.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["comment_id"],
            "message": test_data["comment_name"],
        }

        # Add a comment to a file
        response = add_a_comment(
            file_id=test_data["file_id"],
            comment=test_data["comment_name"],
        )

        # Ensure that add_a_comment() executed and returned proper values
        assert response
        assert response.comment_id == test_data["comment_id"]
        assert response.comment == test_data["comment_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="comments",
            data={
                "item": {"id": test_data["file_id"], "type": "file"},
                "message": test_data["comment_name"],
            },
        )
