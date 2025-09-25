from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_countries import get_countries


def test_get_countries() -> None:
    """Test that the country can be fetched suceessfully by the `get_country` tool."""

    # Define test data:
    test_data = {
        "country_code": "JP",
        "country_name": "Japan",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_countries.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "label": test_data["country_name"],
                    "value": test_data["country_code"],
                },
            ],
        }

        # Get countries
        response = get_countries(country_code=test_data["country_code"])

        # Ensure that get_assignment_groups() executed and returned proper values
        assert response
        assert len(response.countries_list)
        assert response.countries_list[0].country_code == test_data["country_code"]
        assert response.countries_list[0].country_name == test_data["country_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice",
            params={
                "name": "sys_user",
                "element": "country",
                "value": test_data["country_code"],
            },
        )
