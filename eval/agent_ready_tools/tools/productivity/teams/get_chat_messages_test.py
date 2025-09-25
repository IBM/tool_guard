from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_chat_messages import (
    ChatMessage,
    get_chat_messages,
)


def test_get_chat_messages() -> None:
    """Tests that the chat messages can be retrieved by the `get_chats` tool in Microsoft teams."""

    # Define test data with explicit type annotation
    test_data = {
        "chat_message_id": "1743765494479",
        "chat_id": "19:faefd53dda51455695e57a35b9d806db@thread.v2",
        "message_type": "message",
        "message": "Hi",
        "web_url": "",
        "output_limit": 10,
        "output_skip": "U291cmNlPU1lc3NhZ2luZ0Zyb250RW5kIyNUeXBlPVN5bmNTdGF0ZSMjQ29udGludWF0aW9uVG9rZW49M2UyZDAwMDAwMDMxMzkzYTY2NjE2NTY2NjQzNTMzNjQ2NDYxMzUzMTM0MzUzNTM2MzkzNTY1MzUzNzYxMzMzNTYyMzk2NDM4MzAzNjY0NjI0MDc0Njg3MjY1NjE2NDJlNzYzMjAxMDE1MTdmMDA5NjAxMDAwMGNmZGE4NTAwOTYwMTAwMDA=",
    }
    limit = 10
    skip_token = test_data["output_skip"]

    # Patch `get_microsoft_client` to return a mock  client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_chat_messages.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["chat_message_id"],
                    "chatId": test_data["chat_id"],
                    "messageType": test_data["message_type"],
                    "webUrl": test_data["web_url"],
                    "body": {"content": test_data["message"]},
                }
            ],
            "@odata.nextLink": f"https://example.com/nextLink?$top={test_data["output_limit"]}&$skiptoken={test_data["output_skip"]}",
        }

        response = get_chat_messages(
            chat_id=test_data["chat_id"], limit=limit, skip_token=skip_token
        )

        expected_chat_message = ChatMessage(
            chat_message_id=str(test_data["chat_message_id"]),
            chat_id=str(test_data["chat_id"]),
            message_type=str(test_data["message_type"]),
            web_url=str(test_data["web_url"]),
            message=str(test_data["message"]),
        )
        assert response.messages[0] == expected_chat_message
        assert response.limit == test_data["output_limit"]
        assert response.skip_token == test_data["output_skip"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"chats/{test_data["chat_id"]}/messages",
            params={"$top": limit, "$skiptoken": skip_token},
        )
