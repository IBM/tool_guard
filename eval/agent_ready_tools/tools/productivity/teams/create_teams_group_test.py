from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.create_teams_group import create_teams_group


def test_create_teams_group() -> None:
    """Test that a Teams group has been created successfully using the `create_teams_group` tool."""

    # Define test data:
    test_data = {
        "display_name": "Project Alpha Team",
        "mail_nickname": "project-alpha",
        "http_code": 200,
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.create_teams_group.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create Teams group
        response = create_teams_group(
            display_name=test_data["display_name"],
            mail_nickname=test_data["mail_nickname"],
        )

        # Ensure that create_teams_group() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint="groups",
            data={
                "displayName": test_data["display_name"],
                "mailNickname": test_data["mail_nickname"],
                "mailEnabled": True,
                "securityEnabled": False,
                "groupTypes": ["Unified"],
            },
        )
