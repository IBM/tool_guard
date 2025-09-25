from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.gmail.list_emails import (
    Email,
    EmailsResponse,
    list_emails,
)


def test_list_emails() -> None:
    """Tests that email messages can be retrieved using the `list_emails` tool from Gmail."""

    # Define test data
    test_data: dict[str, Any] = {
        "id": "197b1968cf36a78c",
        "body": "testing from postman",
        "subject": "testing123",
        "from_address": "agenttool8@gmail.com",
        "to_address": "arulsri.k@gmail.com",
        "date": "Mon, 01 Jul 2024 10:00:00 +0000",
        "output_nextPageToken": None,
    }
    limit = 5

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.gmail.list_emails.get_google_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock response for listing messages
        mock_client.get_request.side_effect = [
            {
                "messages": [{"id": test_data["id"]}],
                "nextPageToken": test_data["output_nextPageToken"],
            },
            {
                "id": test_data["id"],
                "snippet": test_data["body"],
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": test_data["subject"]},
                        {"name": "From", "value": test_data["from_address"]},
                        {"name": "To", "value": test_data["to_address"]},
                        {"name": "Date", "value": test_data["date"]},
                    ]
                },
            },
        ]

        # Call the tool
        response = list_emails(
            to_address=test_data["to_address"],
            subject=test_data["subject"],
            limit=limit,
        )

        expected_email = Email(
            id=test_data["id"],
            body=test_data["body"],
            subject=test_data["subject"],
            from_address=test_data["from_address"],
            to_address=test_data["to_address"],
            date=test_data["date"],
        )

        expected_response = EmailsResponse(
            emails=[expected_email],
            limit=limit,
            next_page_token=test_data["output_nextPageToken"],
        )

        # Assertions
        assert response.emails[0] == expected_response.emails[0]

        # Verify the API calls
        mock_client.get_request.assert_any_call(
            entity="users/me/messages",
            service="gmail",
            version="v1",
            params={
                "maxResults": limit,
                "pageToken": test_data["output_nextPageToken"],
                "q": f"to:{test_data['to_address']} subject:{test_data['subject']}",
            },
        )
        mock_client.get_request.assert_any_call(
            entity=f"users/me/messages/{test_data['id']}", service="gmail", version="v1"
        )
