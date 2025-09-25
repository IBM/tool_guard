from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.get_file_comments import (
    GetFileComment,
    get_file_comments,
)


def test_get_file_comments() -> None:
    """Verifies that the file's comments can be retrieved successfully by the tool
    `get_file_comments`."""

    # Define test data.
    test_data = {
        "comment_id": "AAABhrVvDt4",
        "comment": "Adding a comment through postman",
        "author_name": "Agent Tool",
        "created_datetime": "2025-04-14T13:50:41.756Z",
        "file_id": "1d7F2bMTDmi6XlFxPgz39ME2DB-E6KXWx",
    }

    limit = 10
    next_page_token = ""

    # Patch mock client instance.
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.get_file_comments.get_google_client"
    ) as mock_google_client:

        # Create a mock client instance.
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "comments": [
                {
                    "id": test_data["comment_id"],
                    "content": test_data["comment"],
                    "author": {"displayName": test_data["author_name"]},
                    "createdTime": test_data["created_datetime"],
                }
            ],
            "nextPageToken": next_page_token,
        }

        # Get File's Comments
        response = get_file_comments(
            file_id=test_data["file_id"], limit=limit, next_page_token=next_page_token
        )

        expected_result = GetFileComment(
            comment_id=str(test_data["comment_id"]),
            comment=str(test_data["comment"]),
            author_name=str(test_data["author_name"]),
            created_datetime=str(test_data["created_datetime"]),
        )

        # Ensure that get_file_comments() has executed and returned proper values
        assert response
        assert response.comments[0] == expected_result
        assert response.limit == limit
        assert response.next_page_token == next_page_token

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data["file_id"]}/comments?fields=*",
            params={"pageSize": limit, "pageToken": next_page_token},
        )
