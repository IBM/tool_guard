from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_country_of_employment import (
    get_country_of_employment,
)


def test_get_country_of_employment() -> None:
    """Test that the `get_country_of_employment` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "40004",
        "country": "IND",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_country_of_employment.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {"results": [{"countryOfCompany": test_data["country"]}]}
        }

        # Get country of employment
        response = get_country_of_employment(test_data["user_id"])

        # Ensure that get_country_of_employment() executed and returned proper values
        assert response
        assert len(response.countries_of_employment)
        assert response.countries_of_employment[0].country_of_employment == test_data["country"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="EmpJob", filter_expr=f"userId eq '{test_data['user_id']}'"
        )
