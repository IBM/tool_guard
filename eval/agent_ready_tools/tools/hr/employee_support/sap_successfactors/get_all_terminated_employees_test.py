from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_all_terminated_employees import (
    get_all_terminated_employees,
)


def test_get_all_terminated_employees() -> None:
    """Test that list of terminated employees can be retrieved successfully for the given user."""
    # Define test data:
    test_data = {
        "person_id": "40006",
        "user_id": "40004",
        "end_date": "/Date(1546214400000)/",
        "event_reason": "TEROTH",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_all_terminated_employees.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "personIdExternal": test_data["person_id"],
                        "userId": test_data["user_id"],
                        "endDate": test_data["end_date"],
                        "jobInfoNav": {"eventReason": test_data["event_reason"]},
                    },
                ]
            }
        }

        # Get all terminated employees
        response = get_all_terminated_employees(person_id_external=test_data["person_id"])

        # Ensure that get_all_terminated_employees() executed and returned proper values
        assert response
        assert len(response.terminated_employees)
        assert response.terminated_employees[0].person_id_external == test_data["person_id"]
        assert response.terminated_employees[0].user_id == test_data["user_id"]
        assert response.terminated_employees[0].end_date == test_data["end_date"]
        assert response.terminated_employees[0].event_reason == test_data["event_reason"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="EmpEmploymentTermination",
            filter_expr=f"employmentNav/empJobRelationshipNav/relUserId eq '{test_data['person_id']}'",
            expand_expr="employmentNav/empJobRelationshipNav,jobInfoNav",
        )
