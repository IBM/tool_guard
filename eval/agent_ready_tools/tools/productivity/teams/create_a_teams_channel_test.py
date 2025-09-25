from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.create_a_teams_channel import create_a_teams_channel


def test_create_a_teams_channel() -> None:
    """Verifies that the `create_a_team_channel` tool can successfully create a teams channel."""

    # Define test data
    test_data = {
        "team_id": "61838cd9-751d-4b56-a24c-4f904f4aa7d3",
        "channel_name": "Test channel11",
        "description": "Testing a channel creation",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.create_a_teams_channel.get_microsoft_client"
    ) as mock_teams_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_teams_client.return_value = mock_client
        mock_client.post_request.return_value = {"displayName": test_data["channel_name"]}

        # Create a team channel
        response = create_a_teams_channel(
            team_id=test_data["team_id"],
            channel_name=test_data["channel_name"],
            description=test_data["description"],
        )

        # Ensure that create_a_teams_channel() executed and returned proper values
        assert response
        assert response.channel_name == test_data["channel_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"teams/{test_data["team_id"]}/channels",
            data={
                "displayName": test_data["channel_name"],
                "description": test_data["description"],
            },
        )
