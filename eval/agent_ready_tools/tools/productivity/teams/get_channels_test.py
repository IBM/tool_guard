from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_channels import GetChannels, get_channels


def test_get_channels() -> None:
    """Tests that channels can be retrieved by the `get_channels` tool in Microsoft Teams."""

    # Define test data
    test_data = {
        "channel_id": "19:hj0_bpSOkTHipm-FPuygCugIp3DxDS0FiMjAY1sdRcM1@thread.tacv2",
        "display_name": "Get Channels Test Channel",
        "description": "To test get channels",
        "email": "GetChannelsTestTeam@ibmappcon.onmicrosoft.com",
        "web_url": "https://teams.microsoft.com/l/channel/19%3Ahj0_bpSOkTHipm-FPuygCugIp3DxDS0FiMjAY1sdRcM1%40thread.tacv2/Get%20Channels%20Test%20Team?groupId=76a59c8a-ad50-4493-bbe3-e5828d5942da&tenantId=0195ea87-1839-4df0-9739-bf7eec6de925&allowXTenantAccess=True&ngc=True",
        "team_id": "76a59c8a-ad50-4493-bbe3-e5828d5942da",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_channels.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["channel_id"],
                    "displayName": test_data["display_name"],
                    "description": test_data["description"],
                    "email": test_data["email"],
                    "webUrl": test_data["web_url"],
                }
            ]
        }

        # Call the function
        response = get_channels(team_id=test_data["team_id"])

        # Verify that the team details matches the expected data
        expected_channels = GetChannels(
            channel_id=test_data["channel_id"],
            display_name=test_data["display_name"],
            description=test_data["description"],
            email=test_data["email"],
            web_url=test_data["web_url"],
        )

        assert response.channels[0] == expected_channels

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"teams/{test_data['team_id']}/allChannels",
        )
