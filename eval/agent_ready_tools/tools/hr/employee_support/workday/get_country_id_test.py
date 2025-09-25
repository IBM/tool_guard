from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_country_id import get_country_id


def test_get_country_id() -> None:
    """Test that the `get_country_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "Algeria",
        "id": "9e616caff5b1480aab04f1ce22d7e7d4",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_country_id.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "descriptor": test_data["name"],
                }
            ],
        }

        # Get country ID
        response = get_country_id(country_name=test_data["name"])

        # Ensure that get_country_id() executed and returned proper values
        assert response == test_data["id"]

        # Ensure the API call was made with expected parameters
        url = f"api/person/v4/{mock_client.tenant_name}/values/countryComponents/country/"
        mock_client.get_request.assert_called_once_with(url=url)
