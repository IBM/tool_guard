from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_time_zones import get_time_zones


def test_get_time_zones() -> None:
    """Tests that the `get_time_zones` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "US/Hawaii",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_time_zones.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "label": test_data["name"],
                },
            ],
        }

        # Get timezones
        response = get_time_zones(time_zone_label=test_data["name"])

        # Ensure that get_time_zones() executed and returned proper values
        assert response
        assert len(response.timezones)
        assert response.timezones[0].time_zone_label == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice",
            params={
                "name": "sys_user",
                "element": "time_zone",
                "inactive": "false",
                "label": test_data["name"],
            },
        )
