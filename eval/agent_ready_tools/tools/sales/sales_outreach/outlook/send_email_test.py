from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.send_mail import send_mail


def test_send_mail() -> None:
    """Tests that an email is being sent successfully by the `send_mail` tool."""

    # Define test data:
    test_data = {
        "http_code": 202,
        "email_body": "Testing send_mail tool code",
        "email_address": "oruganti.ramayya@wipro.com",
        "cc_email_address": "oruganti.ramayya@wipro.com",
        "subject": "Test mail",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.send_mail.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Send a mail
        response = send_mail(
            email_body=test_data["email_body"],
            email_address=test_data["email_address"],
            subject=test_data["subject"],
            cc_email_address=test_data["cc_email_address"],
        )

        # Ensure that send_mail() executed and returned proper values
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/sendMail",
            data={
                "message": {
                    "subject": test_data["subject"],
                    "body": {
                        "contentType": "Text",
                        "content": test_data["email_body"],
                    },
                    "toRecipients": [{"emailAddress": {"address": test_data["email_address"]}}],
                    "ccRecipients": [{"emailAddress": {"address": test_data["cc_email_address"]}}],
                },
            },
        )


def test_send_mail_multiple_emails() -> None:
    """Tests that an email is being sent successfully by the `send_mail` tool."""

    # Define test data:
    test_data = {
        "http_code": 202,
        "email_body": "Testing send_mail tool code",
        "subject": "Test mail",
        "user_name": "user@example.com",
    }

    email_address = ["oruganti.ramayya@wipro.com", "rahul.dutta11@wipro.com"]
    cc_email_address = ["john.smith@ibm.com", "ivan.kuzmich@ibm.com"]

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.send_mail.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Send a mail
        response = send_mail(
            email_body=test_data["email_body"],
            subject=test_data["subject"],
            email_address=email_address,
            cc_email_address=cc_email_address,
        )

        # Ensure that send_mail() executed and returned proper values
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/sendMail",
            data={
                "message": {
                    "subject": test_data["subject"],
                    "body": {
                        "contentType": "Text",
                        "content": test_data["email_body"],
                    },
                    "toRecipients": [
                        {"emailAddress": {"address": email}} for email in email_address
                    ],
                    "ccRecipients": [
                        {"emailAddress": {"address": email}} for email in cc_email_address
                    ],
                },
            },
        )
