from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.slack.get_all_slack_users import get_all_slack_users


def test_get_all_slack_users() -> None:
    """Verify that the `get_all_slack_users` tool can successfully retrieve all Slack users."""

    first_page = {
        "ok": True,
        "members": [
            {
                "id": "U12345678",
                "name": "johndoe",
                "team_id": "T12345",
                "profile": {"email": "john.doe@example.com"},
            },
            {
                "id": "U87654321",
                "name": "janesmith",
                "team_id": "T12345",
                "profile": {"email": "jane.smith@example.com"},
            },
        ],
        "response_metadata": {"next_cursor": "dXNlcjpVMEMyVUMzN0Y="},
    }

    second_page = {
        "ok": True,
        "members": [
            {"id": "B12345678", "name": "slackbot", "team_id": "T12345", "profile": {"email": None}}
        ],
        "response_metadata": {"next_cursor": ""},
    }

    with patch(
        "agent_ready_tools.tools.productivity.slack.get_all_slack_users.get_slack_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.side_effect = [first_page, second_page]

        response = get_all_slack_users()

        assert response
        assert response.http_code == 200
        assert len(response.users) == 3

        assert response.users[0].id == "U12345678"
        assert response.users[0].name == "johndoe"
        assert response.users[0].team_id == "T12345"
        assert response.users[0].email == "john.doe@example.com"

        assert response.users[1].id == "U87654321"
        assert response.users[1].name == "janesmith"
        assert response.users[1].team_id == "T12345"
        assert response.users[1].email == "jane.smith@example.com"

        assert response.users[2].id == "B12345678"
        assert response.users[2].name == "slackbot"
        assert response.users[2].team_id == "T12345"
        assert response.users[2].email is None

        assert mock_client.get_request.call_count == 2
        mock_client.get_request.assert_any_call(entity="users.list", params={})
        mock_client.get_request.assert_any_call(
            entity="users.list", params={"cursor": "dXNlcjpVMEMyVUMzN0Y="}
        )


def test_get_all_slack_users_error() -> None:
    """Verify that the `get_all_slack_users` tool correctly handles an error response."""

    mock_response = {"ok": False, "error": "invalid_auth", "members": []}

    with patch(
        "agent_ready_tools.tools.productivity.slack.get_all_slack_users.get_slack_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_response

        response = get_all_slack_users()

        assert response
        assert response.http_code == 400
        assert len(response.users) == 0

        mock_client.get_request.assert_called_once_with(entity="users.list", params={})
