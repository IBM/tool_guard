from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.slack.get_all_slack_channels import (
    Channel,
    GetallchannelsResponse,
    get_all_slack_channels,
)


def test_get_all_slack_channels() -> None:
    """Tests that the list of channels is retrieved by the 'get_all_slack_channels' tool."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "types": ["public_channel", "private_channel"],
        "limit": 2,
        "cursor": "dGVhbTpDMDhOV0xIUkVUWA==",
        "exclude_archived": False,
        "channels": [
            {
                "id": "C08NWLHRETX",
                "name": "test_private_channel",
                "is_channel": True,
                "is_im": False,
                "is_mpim": False,
                "is_private": True,
                "is_member": True,
            },
        ],
        "next_cursor": "dGVhbTpDMDhQMzNYN0dEUQ==",
    }

    # Patch get_slack_client to get a mock client
    with patch(
        "agent_ready_tools.tools.productivity.slack.get_all_slack_channels.get_slack_client"
    ) as mock_box_client:

        # Create a mock client instance:
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "channels": test_data["channels"],
            "response_metadata": {"next_cursor": test_data["next_cursor"]},
        }

        # Call the function
        response = get_all_slack_channels(
            types=test_data["types"],
            limit=test_data["limit"],
            cursor=test_data["cursor"],
            exclude_archived=test_data["exclude_archived"],
        )

        # Verify that the channel details match with the expected data
        expected_response = GetallchannelsResponse(
            channels=[
                Channel(
                    channel_id="C08NWLHRETX",
                    channel_name="test_private_channel",
                    is_channel=True,
                    is_im=False,
                    is_mpim=False,
                    is_private=True,
                    is_member=True,
                )
            ],
            next_cursor=test_data["next_cursor"],
        )

        assert response.channels[0] == expected_response.channels[0]
        assert response.next_cursor == expected_response.next_cursor

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="conversations.list",
            params={
                "types": "public_channel,private_channel",
                "limit": 2,
                "exclude_archived": False,
                "cursor": test_data["cursor"],
            },
        )
