from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_countries import (
    get_countries_oracle,
)


def test_get_countries_oracle() -> None:
    """Test that the `get_countries_oracle` function returns the expected response."""

    # Define test data:
    test_data = {
        "country_name": "United States of America",
        "country_code": "USA",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_countries.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "CountryName": test_data["country_name"],
                    "TerritoryCode": test_data["country_code"],
                }
            ]
        }

        # Get countries
        response = get_countries_oracle(country_name=" ")

        # Ensure that get_countries_oracle() executed and returned proper values
        assert response
        assert len(response.country_names)
        assert response.country_names[0].country_name == test_data["country_name"]
        assert response.country_names[0].country_code == test_data["country_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="hcmCountriesLov",
            q_expr=None,
        )
