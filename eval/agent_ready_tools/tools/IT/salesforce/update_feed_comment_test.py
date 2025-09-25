from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_feed_comment import update_feed_comment


def test_update_feed_comment() -> None:
    """Test that the `update_feed_comment` function returns the expected response."""
    # Define test data
    test_data = {
        "comment": "updating feed comment.",
        "feed_comment_id": "0D7gL0000000Y05SAE",
        "status": "Published",
        "is_rich_text": False,
    }
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_feed_comment.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.FeedComment.update.return_value = test_response

        # Update feed comment
        response = update_feed_comment(
            feed_comment_id=test_data["feed_comment_id"],
            comment=test_data["comment"],
            status=test_data["status"],
            is_rich_text=test_data["is_rich_text"],
        )

        # Ensure that update_feed_comment() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.FeedComment.update(test_data, test_data["feed_comment_id"])
