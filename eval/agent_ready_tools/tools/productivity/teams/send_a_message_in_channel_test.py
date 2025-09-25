from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.send_a_message_in_channel import (
    send_a_message_in_channel,
)


def test_send_a_message_in_channel() -> None:
    """Verifies that the send_a_message_in_channel tool can successfully send a message in a
    channel."""

    # Define test data
    test_data = {
        "team_id": "0579fca9-73f9-4325-b474-11e6ee31bd67",
        "channel_id": "19:f074f4a188b54e96ab13b6065ffa0749@thread.tacv2",
        "message": "Sending a message in channel",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.send_a_message_in_channel.get_microsoft_client"
    ) as mock_teams_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_teams_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "body": {
                "content": test_data["message"],
            }
        }

        # Send a message in channel
        response = send_a_message_in_channel(
            team_id=test_data["team_id"],
            channel_id=test_data["channel_id"],
            message=test_data["message"],
        )

        # Ensure that send_a_message_in_channel() executed and returned proper values
        assert response
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"teams/{test_data["team_id"]}/channels/{test_data["channel_id"]}/messages",
            data={
                "body": {
                    "content": test_data["message"],
                }
            },
        )
