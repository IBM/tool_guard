from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_team_members import get_team_members


def test_get_team_members() -> None:
    """Tests that the team members can be retrieved successfully using `get_team_members` tool."""

    # Define test data:
    test_data = {
        "team_id": "032f4d85-b7fe-4d6a-9ff2-502ea7b0c535",
        "display_name": "cstest",
        "email": "abc@teams.com",
        "user_id": "6112ac05-0cb5-4233-8d0a-9afaec456e1e",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_team_members.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "displayName": test_data["display_name"],
                    "userId": test_data["user_id"],
                    "email": test_data["email"],
                }
            ]
        }

        # Get Team Members
        response = get_team_members(team_id=test_data["team_id"])

        # Ensure that get_team_members() executed and returned proper values
        assert response
        assert len(response.team_members)
        assert response.team_members[0].display_name == test_data["display_name"]
        assert response.team_members[0].email == test_data["email"]
        assert response.team_members[0].user_id == test_data["user_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"teams/{test_data["team_id"]}/members",
        )
