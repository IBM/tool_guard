from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.create_a_team import create_a_team


def test_create_a_team() -> None:
    """Tests that the team can be created successfully by the `create_a_team` tool."""
    # Define test data:
    test_data = {
        "team_name": "Hello test",
        "description": "Hello test team is used for testing",
        "first_channel_name": "My first channel of the test team",
        "http_code": 202,
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.create_a_team.get_microsoft_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create a team
        response = create_a_team(
            team_name=test_data["team_name"],
            description=test_data["description"],
            first_channel_name=test_data["first_channel_name"],
        )

        # Ensure that create_a_team() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Since there is no API available to fetch the templates and this parameter is mandatory, it is hardcoded to 'standard' and passed within template_name.
        template_name = "https://graph.microsoft.com/v1.0/teamsTemplates('standard')"

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint="teams",
            data={
                "template@odata.bind": template_name,
                "displayName": test_data["team_name"],
                "description": test_data["description"],
                "firstChannelName": test_data["first_channel_name"],
            },
        )
