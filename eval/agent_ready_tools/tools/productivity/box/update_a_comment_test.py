from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.update_a_comment import update_a_comment


def test_update_a_comment() -> None:
    """Tests that the comment can be updated successfully by the `update_a_comment` tool."""

    # Define test data:
    test_data = {
        "comment": "This is a new test comment to update.",
        "comment_id": "651642941",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.update_a_comment.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.put_request.return_value = {"message": test_data["comment"]}

        # Update comment for a file
        response = update_a_comment(
            original_comment_id=test_data["comment_id"], new_comment=test_data["comment"]
        )

        # Ensure that update_a_comment() executed and returned proper values
        assert response
        assert response.message == test_data["comment"]

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"comments/{test_data['comment_id']}", data={"message": test_data["comment"]}
        )
