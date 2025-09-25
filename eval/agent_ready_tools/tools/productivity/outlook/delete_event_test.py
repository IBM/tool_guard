from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.delete_event import delete_event


def test_delete_event() -> None:
    """Verify that the `delete_event` tool can successfully delete an Outlook event."""

    # Define test data:
    test_data = {"event_id": "987654321", "http_code": 204, "user_name": "user@example.com"}

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.delete_event.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Delete Microsoft Outlook Event
        delete_response = delete_event(test_data["event_id"])

        # Ensure that delete_event() executed and returned proper values
        assert delete_response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            f"users/{test_data["user_name"]}/events/{test_data['event_id']}"
        )
