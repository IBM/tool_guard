from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_job_change_locations import (
    get_job_change_locations,
)


def test_get_job_change_locations() -> None:
    """Tests that the `get_job_change_locations` tool returns the expected response."""

    # Define test data:
    test_data = {
        "category_id": "ce3de224b11a100013610893adec0148",
        "location_id": "edde84f38de1494b9c7911dcc5c40bc6",
        "location_descriptor": "Krakow",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_change_locations.get_workday_client"
    ) as mock_get_workday_client, patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_change_locations.get_job_change_locations_categories"
    ) as mock_get_categories:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["location_id"],
                    "descriptor": test_data["location_descriptor"],
                }
            ],
        }

        mock_get_workday_client.return_value = mock_client
        mock_get_categories.return_value = test_data["category_id"]

        # Get job change locations
        response = get_job_change_locations(category_id=test_data["category_id"])

        # Ensure that get_job_change_locations() executed and returned proper values
        assert response
        assert len(response.locations)
        assert response.locations[0].location_id == test_data["location_id"]
        assert response.locations[0].descriptor == test_data["location_descriptor"]

        # Ensure the API call was made with expected parameters
        expected_url = f"api/staffing/v6/{mock_client.tenant_name}/values/jobChangesGroup/locations/{test_data['category_id']}"
        mock_client.get_request.assert_called_once_with(url=expected_url)
