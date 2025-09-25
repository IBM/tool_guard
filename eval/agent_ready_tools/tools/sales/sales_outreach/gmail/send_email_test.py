import base64
from email.message import EmailMessage
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_outreach.gmail.send_email import gmail_send_email


def test_gmail_send_email() -> None:
    """Test that the email was send successfully using send_an_email tool."""

    # Define test data
    test_data = {
        "email_address": "rangisettiganesh2000@gmail.com,kavyagoudthabeti01@gmail.com",
        "body": "Testing the python code",
        "subject": "Tool testing",
        "cc_email_address": "",
        "bcc_email_address": "",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_outreach.gmail.send_email.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.post_request.return_value = {"labelIds": ["SENT"]}

        # Send an email
        response = gmail_send_email(
            email_address=test_data["email_address"],
            body=test_data["body"],
            subject=test_data["subject"],
            cc_email_address=test_data["cc_email_address"],
            bcc_email_address=test_data["bcc_email_address"],
        )

        # Ensure that send_an_email() executed and returned proper values
        assert response
        assert response.label == "SENT"

        content = EmailMessage()
        content.set_content(test_data["body"])

        content["To"] = test_data["email_address"]
        content["Subject"] = test_data["subject"]
        if test_data["cc_email_address"]:
            content["Cc"] = test_data["cc_email_address"]
        if test_data["bcc_email_address"]:
            content["Bcc"] = test_data["bcc_email_address"]

        # encoded message
        encoded_message = base64.urlsafe_b64encode(content.as_bytes()).decode()

        payload = {"raw": encoded_message}

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="users/me/messages/send", service="gmail", version="v1", payload=payload
        )
