from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_state_id import get_state_id


def test_get_state_id() -> None:
    """Test that the `get_state_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "country_id": "bc33aa3152ec42d4995f4791a106ed09",
        "state_name": "California",
        "state_id": "ec3d210e4240442e99a28fa70419aec5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_state_id.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["state_id"],
                    "descriptor": test_data["state_name"],
                }
            ],
        }

        # Get state id
        response = get_state_id(
            country_id=test_data["country_id"], state_name=test_data["state_name"]
        )

        # Ensure that get_state_id() executed and returned proper values
        assert response == test_data["state_id"]

        # Ensure the API call was made with expected parameters
        url = f"api/person/v4/{mock_client.tenant_name}/values/countryComponents/countryRegion"
        params = {"country": test_data["country_id"]}
        mock_client.get_request.assert_called_once_with(url=url, params=params)
