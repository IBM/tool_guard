from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_employee_location import (
    get_employee_location,
)


def test_get_employee_location() -> None:
    """Integration test for the `get_employee_location` tool."""
    # Define test data:
    test_data = {"user_id": "109031", "location_id": "9100-0001", "company": "9100"}

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_employee_location.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [{"location": test_data["location_id"], "company": test_data["company"]}]
            }
        }

        # Get employee location
        response = get_employee_location(user_id=test_data["user_id"])

        # Ensure that get_employee_location() executed and returned proper values
        assert response
        assert response.location == test_data["location_id"]
        assert response.company == test_data["company"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="EmpJob",
            filter_expr=f"userId eq '{test_data['user_id']}'",
            select_expr="location,company",
        )
