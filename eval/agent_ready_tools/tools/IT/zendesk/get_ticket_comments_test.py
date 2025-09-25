from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_ticket_comments import Comment, get_ticket_comments


def test_get_ticket_comment_first_item() -> None:
    """Tests that the first Zendesk comment for a ticket in the response matches the expected
    data."""

    # Define test data
    test_data = {
        "comment": "Test WO",
        "created_at": "2025-06-27T12:29:00Z",
        "file_name": None,
        "content_url": None,
        "content_type": None,
    }
    ticket_id = 184924
    comment_id = 782043723434
    author_id = 382203429554

    # Inputs and expected pagination values
    per_page = 1
    page = 1
    output_page = 2
    output_per_page = 1

    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_ticket_comments.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "comments": [
                {
                    "id": comment_id,
                    "author_id": author_id,
                    "body": test_data["comment"],
                    "created_at": test_data["created_at"],
                    "attachments": [],
                }
            ],
            "users": [
                {
                    "id": author_id,
                    "name": "Agent",
                }
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/v2/tickets/184924/comments.json?include=users&page=2&per_page=1",
        }

        # Patch pagination helper if needed
        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

            # Call the function
            response = get_ticket_comments(ticket_id=ticket_id, per_page=per_page, page=page)

            # Expected first comment of ticket
            expected_first_comment = Comment(
                comment_id=str(comment_id),
                author_name="Agent",
                comment=str(test_data["comment"]),
                created_at=str(test_data["created_at"]),
                file_name=test_data["file_name"],
                content_url=test_data["content_url"],
                content_type=test_data["content_type"],
            )

            # Assertions
            assert response.comments[0] == expected_first_comment
            assert response.page == output_page
            assert response.per_page == output_per_page

            # Assert correct API call
            mock_client.get_request.assert_called_once_with(
                entity=f"tickets/{ticket_id}/comments",
                params={
                    "per_page": per_page,
                    "page": page,
                    "include": "users",
                },
            )
