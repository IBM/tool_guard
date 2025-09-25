from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.send_a_chat_message import send_a_chat_message


def test_send_a_chat_message() -> None:
    """Verifies that the `send_a_chat_message` tool can successfully send a chat message."""

    # Define test data:
    test_data = {
        "chat_id": "19:cfbd412ef36d48a4ba737abcf6461c93@thread.v2",
        "message": "Welcome to teams",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.send_a_chat_message.get_microsoft_client"
    ) as mock_teams_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_teams_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "body": {
                "content": test_data["message"],
            }
        }

        # Sends a chat message
        response = send_a_chat_message(
            message=test_data["message"],
            chat_id=test_data["chat_id"],
        )

        # Ensure that send_a_chat_message() executed and returned proper values
        assert response
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"chats/{test_data["chat_id"]}/messages",
            data={"body": {"content": test_data["message"]}},
        )
