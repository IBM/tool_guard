from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_chats import Chats, get_chats


def test_get_chats() -> None:
    """Tests that the chats can be retrieved by the `get_chats` tool in Microsoft Teams."""

    # Define test data
    test_data: Dict[str, Any] = {
        "chat_id": "19:faefd53dda51455695e57a35b9d806db@thread.v2",
        "chat_name": "Group chat title update",
        "chat_type": "group",
        "output_limit": 50,
        "output_skiptoken": "1.kscDYs0BEcYAAAEU8P8DgapQcm9wZXJ0aWVzgqlTeW5jU3RhdGXZ6GV5SmtaV3hwZG1WeVpXUlRaV2R0Wlc1MGN5STZXM3NpYzNSaGNuUWlPaUl5TURJMUxUQTBMVEF5VkRFeU9qVTNPakF6TGpreE5pc3dNRG93TUNJc0ltVnVaQ0k2SWpJd01qVXRNRFF0TURoVU1URTZNRFU2TVRZdU16QXpLekF3T2pBd0luMWRMQ0o2WlhKdlRFMVRWRVJsYkdsMlpYSmxaRk5sWjIxbGJuUnpJanBiWFN3aWMyOXlkRTl5WkdWeUlqb3dMQ0pwYm1Oc2RXUmxXbVZ5YjB4TlUxUWlPbVpoYkhObGZRPT2sTGFzdFBhZ2VTaXplojUw",
        "user_name": "user@example.com",
    }
    limit = 50
    member_details = [
        ("Test User 1", "testuser1@example.com"),
        ("Test User 2", "testuser2@example.com"),
    ]

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_chats.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["chat_id"],
                    "topic": test_data["chat_name"],
                    "chatType": test_data["chat_type"],
                    "members": [
                        {"displayName": member_details[0][0], "email": member_details[0][1]},
                        {"displayName": member_details[1][0], "email": member_details[1][1]},
                    ],
                }
            ],
            "@odata.nextLink": f"https://example.com/nextLink?$filter=startswith(topic,'{test_data["chat_name"]}')&$top={test_data["output_limit"]}&$skiptoken={test_data["output_skiptoken"]}",
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_chats(chat_name=test_data["chat_name"], limit=limit)

        # Verify that the chat details matches the expected data
        expected_chats = Chats(
            chat_id=str(test_data["chat_id"]),
            chat_name=str(test_data["chat_name"]),
            chat_type=str(test_data["chat_type"]),
            member_details=member_details,
        )

        assert response.chats[0] == expected_chats
        assert response.limit == test_data["output_limit"]
        assert response.skip_token == test_data["output_skiptoken"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/chats",
            params={
                "$top": limit,
                "$expand": "members",
                "$filter": f"startswith(topic,'{test_data['chat_name']}')",
            },
        )
