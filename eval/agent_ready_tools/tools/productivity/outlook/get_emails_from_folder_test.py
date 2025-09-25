from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_emails_from_folder import (
    Emails,
    get_emails_from_folder,
)


def test_get_emails_from_folder() -> None:
    """Tests that the emails can be retrieved by the `get_emails_from_folder` tool in Microsoft
    Outlook."""

    # Define test data
    test_data: dict[str, str] = {
        "folder_id": "AQMkADYyODVkMjM5LTFlZQA3LTRmMWYtYThjOC1hYmY2Mjc5ZDE5ODYALgAAA5zjV7sSmoBNlqiW3HRRFSgBAP-JqXJZwVlLuTcXA31G-1sAAAIBDAAAAA==",
        "message_id": "AAMkAGVmMDEzMTM4LTZmYWUtNDdkNC1hMDZiLTU1OGY5OTZhYmY4OABGAAAAAAAiQ8W967B7TKBjgx9rVEURBwAiIsqMbYjsT5e-T7KzowPTAAAAAAEMAAAiIsqMbYjsT5e-T7KzowPTAAYdkniWAAA=",
        "recipient_email_address": "MeganB@M365x214355.onmicrosoft.com",
        "sender_email_address": "viva-noreply@microsoft.com",
        "sender_name": "Microsoft Viva",
        "subject": "Your digest email",
        "body": "This is a test email body.",
        "user_name": "user@example.com",
    }
    limit = 100
    skip = 0
    output_limit = None
    output_skip = None

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_emails_from_folder.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["message_id"],
                    "toRecipients": [
                        {"emailAddress": {"address": test_data["recipient_email_address"]}}
                    ],
                    "subject": test_data["subject"],
                    "bodyPreview": test_data["body"],
                    "sender": {
                        "emailAddress": {
                            "address": test_data["sender_email_address"],
                            "name": test_data["sender_name"],
                        }
                    },
                }
            ],
            "limit": limit,
            "skip": skip,
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_emails_from_folder(
            folder_id=test_data["folder_id"],
            sender_name=test_data["sender_name"],
            sender_email_address=test_data["sender_email_address"],
            limit=limit,
            skip=skip,
        )

        # Verify that the email details match the expected data
        expected_response = Emails(
            message_id=test_data["message_id"],
            recipient_email_address=test_data["recipient_email_address"],
            sender_email_address=test_data["sender_email_address"],
            sender_name=test_data["sender_name"],
            subject=test_data["subject"],
            body=test_data["body"],
        )

        assert response.emails[0] == expected_response
        assert response.limit == output_limit
        assert response.skip == output_skip

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/mailFolders/{test_data['folder_id']}/messages",
            params={
                "$filter": f"sender/emailAddress/address eq '{test_data['sender_email_address']}'",
                "$top": limit,
            },
        )
