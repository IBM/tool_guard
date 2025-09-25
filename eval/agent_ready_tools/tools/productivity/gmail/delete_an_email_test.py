from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.gmail.delete_an_email import delete_an_email


def test_delete_an_email() -> None:
    """Verify that the email was deleted successfully through the delete_an_email tool."""

    test_data = {"message_id": "196c57b58c8a6387", "status_code": 204}

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.gmail.delete_an_email.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["status_code"]

        # delete an email
        response = delete_an_email(
            message_id=test_data["message_id"],
        )

        # Ensure that delete_an_email() executed and returned proper values
        assert response
        assert response.http_code == test_data["status_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"users/me/messages/{test_data['message_id']}", service="gmail", version="v1"
        )
