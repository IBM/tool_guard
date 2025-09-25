from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_messages import get_messages


def test_get_messages() -> None:
    """Verify that the `get_messages` tool can successfully retrieve messages for given channel fom
    Teams."""

    test_message_data1 = {
        "id": "123",
        "subject": "subject 1",
        "web_url": "https://teams.microsoft.com/l/message/1%40thread.tacv2/123?groupId=94c30026-bd4&tenantId=01-18&createdTime=1742389865468&parentMessageId=122",
        "content_type": "html",
        "content": "<systemEventMessage/>",
    }

    test_message_data2 = {
        "id": "124",
        "subject": "subject 2",
        "web_url": "https://teams.microsoft.com/l/message/1%40thread.tacv2/124?groupId=94c30026-bd4&tenantId=01-18&createdTime=1742389865469&parentMessageId=123",
        "content_type": "html",
        "content": "<systemEventMessage/>",
    }

    with patch(
        "agent_ready_tools.tools.productivity.teams.get_messages.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": "123",
                    "subject": "subject 1",
                    "webUrl": "https://teams.microsoft.com/l/message/1%40thread.tacv2/123?groupId=94c30026-bd4&tenantId=01-18&createdTime=1742389865468&parentMessageId=122",
                    "body": {"contentType": "html", "content": "<systemEventMessage/>"},
                },
                {
                    "id": "124",
                    "subject": "subject 2",
                    "webUrl": "https://teams.microsoft.com/l/message/1%40thread.tacv2/124?groupId=94c30026-bd4&tenantId=01-18&createdTime=1742389865469&parentMessageId=123",
                    "body": {"contentType": "html", "content": "<systemEventMessage/>"},
                },
            ]
        }

        response = get_messages("94c30026-bd4", "1%40thread.tacv2")

        assert response and response.messages[0].id == test_message_data1["id"]
        assert response and response.messages[0].subject == test_message_data1["subject"]
        assert response and response.messages[0].web_url == test_message_data1["web_url"]
        assert (
            response
            and response.messages[0].body.content_type == test_message_data1["content_type"]
        )
        assert response and response.messages[0].body.content == test_message_data1["content"]
        assert response and response.messages[1].id == test_message_data2["id"]
        assert response and response.messages[1].subject == test_message_data2["subject"]
        assert response and response.messages[1].web_url == test_message_data2["web_url"]
        assert (
            response
            and response.messages[1].body.content_type == test_message_data2["content_type"]
        )
        assert response and response.messages[1].body.content == test_message_data2["content"]

        mock_client.get_request.assert_called_once_with(
            "/teams/94c30026-bd4/channels/1%40thread.tacv2/messages"
        )
