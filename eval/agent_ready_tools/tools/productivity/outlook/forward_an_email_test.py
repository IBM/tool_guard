from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.forward_an_email import forward_an_email


def test_forward_an_email() -> None:
    """Verifies that an email is forwarded to the intended recipient in Microsoft Outlook."""

    # Define test data.
    test_data = {
        "message_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMTk4NgBGAAAAAACc41e7EpqATZaoltx0URUoBwD-yalyWcFZS7k3FwN9Rv9bAAAAAAEJAAD-yalyWcFZS7k3FwN9Rv9bAAblxUC8AAA=",
        "comment": "Hello Comment 001",
        "recipient_email_address": "hello@ochre.com",
        "http_code": 202,
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client.

    with patch(
        "agent_ready_tools.tools.productivity.outlook.forward_an_email.get_microsoft_client"
    ) as mock_outlook_client:
        # Create a mock client instance.
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Forward an email
        response = forward_an_email(
            message_id=test_data["message_id"],
            recipient_email_address=test_data["recipient_email_address"],
            comment=test_data["comment"],
        )

        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/messages/{test_data["message_id"]}/forward",
            data={
                "comment": test_data["comment"],
                "toRecipients": [
                    {"emailAddress": {"address": test_data["recipient_email_address"]}},
                ],
            },
        )


def test_multiple_forward_email() -> None:
    """Verifies that an email is forwarded to multiple intended recipients in Microsoft Outlook."""

    # Define Test Data
    test_data = {
        "http_code": 202,
        "message_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMTk4NgBGAAAAAACc41e7EpqATZaoltx0URUoBwD-yalyWcFZS7k3FwN9Rv9bAAAAAAEJAAD-yalyWcFZS7k3FwN9Rv9bAAblxUC8AAA=",
        "comment": "Hello Comment 202",
        "user_name": "user@example.com",
    }
    # List of recipient email address
    recipient_email_address = [
        "abc@ochre.com",
        "xyz@ochre.com",
    ]

    # Patch `get_microsoft_client` to return a mock client.

    with patch(
        "agent_ready_tools.tools.productivity.outlook.forward_an_email.get_microsoft_client"
    ) as mock_outlook_client:
        # Create a mock client instance.
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Forward multiple email
        response = forward_an_email(
            message_id=test_data["message_id"],
            comment=test_data["comment"],
            recipient_email_address=recipient_email_address,
        )

        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/messages/{test_data["message_id"]}/forward",
            data={
                "comment": test_data["comment"],
                "toRecipients": [
                    {"emailAddress": {"address": item}} for item in recipient_email_address
                ],
            },
        )
