from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.delete_a_comment import delete_a_comment


def test_delete_a_comment() -> None:
    """Test that a file comment can be deleted successfully by the `delete_a_comment` tool."""

    # Define test data:
    test_data = {
        "http_code": 204,
        "comment_id": "653207693",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.delete_a_comment.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete a comment
        response = delete_a_comment(comment_id=test_data["comment_id"])

    # Ensure that delete_a_comment() executed and returned proper values
    assert response
    assert response.http_code == test_data["http_code"]

    # Ensure the API call was made with expected parameters
    mock_client.delete_request.assert_called_once_with(entity=f"comments/{test_data['comment_id']}")
