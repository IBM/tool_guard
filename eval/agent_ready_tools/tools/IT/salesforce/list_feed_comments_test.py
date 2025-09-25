from typing import Any
from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.IT.salesforce.list_feed_comments import list_feed_comments
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import FeedComment


def test_list_feed_comments() -> None:
    """Tests that the `list_feed_comments` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "feed_comment_id": "0D7gL0000000W9ZSAU",
        "comment": "<p>test comment</p>",
        "feed_item_id": "0D5gL0000019IQASA2",
        "parent_id": "500gL000002mk6nQAA",
        "is_rich_text": False,
        "status": "Published",
        "created_by_id": "005gL000001qXQjQAM",
        "created_date": "2025-05-09T14:04:33.000+0000",
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_feed_comments.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["feed_comment_id"],
                "CommentBody": test_data["comment"],
                "FeedItemId": test_data["feed_item_id"],
                "ParentId": test_data["parent_id"],
                "IsRichText": test_data["is_rich_text"],
                "Status": test_data["status"],
                "CreatedById": test_data["created_by_id"],
                "CreatedDate": test_data["created_date"],
            }
        ]

        # Call the function
        response = list_feed_comments("IsDeleted = false")

        # Construct expected object
        expected_value = [
            FeedComment(
                feed_comment_id=test_data["feed_comment_id"],
                comment=test_data["comment"],
                feed_item_id=test_data["feed_item_id"],
                parent_id=test_data["parent_id"],
                is_rich_text=test_data["is_rich_text"],
                status=test_data["status"],
                created_by_id=test_data["created_by_id"],
                created_date=test_data["created_date"],
            )
        ]

        # Assertions
        assert response == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, CommentBody, FeedItemId, ParentId, IsRichText, Status, CreatedById, CreatedDate FROM FeedComment WHERE IsDeleted = false"
            )
        )


def test_list_feed_comments_without_filter() -> None:
    """Tests that the `list_feed_comments` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "feed_comment_id": "0D7gL0000000W9ZSAU",
        "comment": "<p>test comment</p>",
        "feed_item_id": "0D5gL0000019IQASA2",
        "parent_id": "500gL000002mk6nQAA",
        "is_rich_text": False,
        "status": "Published",
        "created_by_id": "005gL000001qXQjQAM",
        "created_date": "2025-05-09T14:04:33.000+0000",
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_feed_comments.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["feed_comment_id"],
                "CommentBody": test_data["comment"],
                "FeedItemId": test_data["feed_item_id"],
                "ParentId": test_data["parent_id"],
                "IsRichText": test_data["is_rich_text"],
                "Status": test_data["status"],
                "CreatedById": test_data["created_by_id"],
                "CreatedDate": test_data["created_date"],
            }
        ]

        # Call the function
        response = list_feed_comments()

        # Construct expected object
        expected_value = [
            FeedComment(
                feed_comment_id=test_data["feed_comment_id"],
                comment=test_data["comment"],
                feed_item_id=test_data["feed_item_id"],
                parent_id=test_data["parent_id"],
                is_rich_text=test_data["is_rich_text"],
                status=test_data["status"],
                created_by_id=test_data["created_by_id"],
                created_date=test_data["created_date"],
            )
        ]

        # Assertions
        assert response == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, CommentBody, FeedItemId, ParentId, IsRichText, Status, CreatedById, CreatedDate FROM FeedComment "
            )
        )
