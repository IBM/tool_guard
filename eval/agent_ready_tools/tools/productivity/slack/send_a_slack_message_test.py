from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.slack.send_a_slack_message import send_a_slack_message


def test_send_a_slack_message() -> None:
    """Tests that the message is being sent successfully in the channel in Slack using the
    `send_a_slack_message` tool."""

    # Define test data:
    test_data = {
        "channel_id": "C05EDJFBK7G",
        "send_message_status": True,
        "text": "Hi team",
        "blocks": [
            {
                "type": "section",
                "text": {"type": "plain_text", "text": "Hi team, just a test message."},
            }
        ],
        "attachments": [{"pretext": "pre-hello", "text": "text-world"}],
    }

    # Patch `get_slack_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.slack.send_a_slack_message.get_slack_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "ok": test_data["send_message_status"],
        }

        # Send message in a channel
        response = send_a_slack_message(
            channel_id=test_data["channel_id"],
            text=test_data["text"],
            blocks=test_data["blocks"],
            attachments=test_data["attachments"],
        )

        # Ensure that send_a_slack_message() executed and returned proper values
        assert response
        assert response.send_message_status == test_data["send_message_status"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="chat.postMessage",
            payload={
                "channel": test_data["channel_id"],
                "text": "Hi team",
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "plain_text", "text": "Hi team, just a test message."},
                    }
                ],
                "attachments": [{"pretext": "pre-hello", "text": "text-world"}],
            },
        )
