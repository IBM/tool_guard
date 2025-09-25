from unittest.mock import MagicMock, patch

from requests import Response
from requests.exceptions import HTTPError

from agent_ready_tools.tools.productivity.outlook.email_search_results import (
    EmailSearchResponse,
    email_search_results,
)


def test_email_search_results_success() -> None:
    """Verify that the `email_search_results` tool handles successful API calls."""

    # Define test data:
    test_data = {
        "search_term": "contoso",
        "user_name": "user@example.com",
        "subject": "Test Subject",
        "body": "Test Body",
        "recipient_name": "Recipient Name",
        "created_date_time": "2024-01-01T00:00:00Z",
        "sender_email_address": "sender@example.com",
        "next_link": "https://graph.microsoft.com/v1.0/me/messages?$search=contoso&$top=5&$skiptoken=sometoken",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.email_search_results.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"
        mock_client.get_request.return_value = {
            "value": [
                {
                    "subject": test_data["subject"],
                    "bodyPreview": test_data["body"],
                    "toRecipients": [{"emailAddress": {"name": test_data["recipient_name"]}}],
                    "createdDateTime": test_data["created_date_time"],
                    "sender": {"emailAddress": {"address": test_data["sender_email_address"]}},
                }
            ],
            "@odata.nextLink": test_data["next_link"],
        }

        # Search for emails
        response = email_search_results(search_term=test_data["search_term"])

        # Ensure that email_search_results() executed and returned proper values
        assert response
        assert isinstance(response, EmailSearchResponse)
        assert response.http_code is None
        assert response.searchemail is not None
        assert len(response.searchemail) == 1
        assert response.searchemail[0].subject == test_data["subject"]
        assert response.limit == 5
        assert response.skip_token == "sometoken"
        assert response.error_message is None

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/messages",
            params={"$search": test_data["search_term"], "$top": 10},
        )


def test_email_search_results_http_error_json() -> None:
    """Verify that the tool handles HTTP errors with JSON responses."""

    test_data = {
        "search_term": "contoso",
        "user_name": "user@example.com",
        "error_http_code": 400,
        "error_message": "The search term is invalid.",
    }

    with patch(
        "agent_ready_tools.tools.productivity.outlook.email_search_results.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = test_data["error_http_code"]
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": {"message": test_data["error_message"]}}

        http_error = HTTPError(response=mock_response)
        mock_client.get_request.side_effect = http_error

        response = email_search_results(search_term=test_data["search_term"])

        assert response
        assert response.http_code == test_data["error_http_code"]
        assert response.error_message == test_data["error_message"]
        assert response.searchemail is None
