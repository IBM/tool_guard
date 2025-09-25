from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_current_compensation_details_sap import (
    get_current_compensation_details_sap,
)


def test_get_current_compensation_details_sap_on_valid_user() -> None:
    """Test that the `get_current_compensation_details_sap` function returns the expected
    response."""
    # Define test data:
    test_data = {
        "user_id": "40004",
        "currency": "EUR",
        "yearly_base_salary": "80000",
        "search_key": "empCompensationCalculatedNav",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_current_compensation_details_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        f"{test_data['search_key']}": {
                            "currency": test_data["currency"],
                            "yearlyBaseSalary": test_data["yearly_base_salary"],
                        }
                    }
                ]
            }
        }

        # Get current compensation details
        response = get_current_compensation_details_sap(user_id=test_data["user_id"])

        # Ensure that get_current_compensation_details_sap() executed and returned proper values
        assert response
        assert response.currency == test_data["currency"]
        assert response.yearly_base_salary == test_data["yearly_base_salary"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "EmpCompensation",
            filter_expr=f"userId eq '{test_data['user_id']}'",
            expand_expr=test_data["search_key"],
        )
