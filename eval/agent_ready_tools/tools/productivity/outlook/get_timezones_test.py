from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_timezones import get_timezones


def test_get_timezones() -> None:
    """Verify that the `get_timezones` tool can successfully return a list of timezones from
    Microsoft Outlook."""

    # Define test data:
    test_date = {
        "timezone_value": "India Standard Time",
        "display_name": "(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi",
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_timezones.get_microsoft_client"
    ) as mock_outlook_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {"alias": test_date["timezone_value"], "displayName": test_date["display_name"]}
            ],
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_date["user_name"]}"

        response = get_timezones().timezones[0]
        # Ensure that get_timezones() executed and returned proper values
        assert response
        assert response.timezone_value == test_date["timezone_value"]
        assert response.display_name == test_date["display_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_date["user_name"]}/outlook/supportedTimeZones"
        )
