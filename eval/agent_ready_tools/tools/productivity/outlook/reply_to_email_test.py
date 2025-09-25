from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.reply_to_email import reply_to_email


def test_reply_to_email() -> None:
    """Tests that reply to an email is sent successfully by the `reply_to_email` tool."""

    # Define test data:
    test_data = {
        "http_code": 202,
        "message_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMTk4NgBGAAAAAACc41e7EpqATZaoltx0URUoBwD-yalyWcFZS7k3FwN9Rv9bAAAAAAEMAAD-yalyWcFZS7k3FwN9Rv9bAAbnpftiAAA=",
        "comment": "Reply to email test continues",
        "user_name": "user@example.com",
    }
    sender_email_address = ["rahul@example.com", "oruganti@example.com"]

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.reply_to_email.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Reply to an email
        response = reply_to_email(
            message_id=test_data["message_id"],
            comment=test_data["comment"],
            sender_email_address=sender_email_address,
        )
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/messages/{test_data["message_id"]}/reply",
            data={
                "message": {
                    "toRecipients": [
                        {"emailAddress": {"address": email_address}}
                        for email_address in sender_email_address
                    ]
                },
                "comment": test_data["comment"],
            },
        )
