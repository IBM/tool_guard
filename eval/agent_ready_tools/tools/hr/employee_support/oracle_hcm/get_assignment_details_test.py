from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_assignment_details import (
    get_assignment_details,
)


def test_get_assignment_details() -> None:
    """Test that the `get_assignment_details` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "period_of_service_id": "999999999999990",
        "legal_employer_name": "Australia Legal Entity",
        "assignment_id": "999999999999999",
        "assignment_id_int": 999999999999999,
        "assignment_name": "Analyst",
        "assignment_number": "E192",
        "primary_flag": True,
        "action_code": "HIRE",
        "child_id": "00020000000EACED00057708000110D9344C684F0000004AAC",
        "url": "https://example.dev.oraclepdemos.com:443/hcmRestApi/resources/11.12.13.14",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_assignment_details.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PeriodOfServiceId": test_data["period_of_service_id"],
                    "LegalEmployerName": test_data["legal_employer_name"],
                    "AssignmentId": test_data["assignment_id"],
                    "AssignmentName": test_data["assignment_name"],
                    "AssignmentNumber": test_data["assignment_number"],
                    "PrimaryFlag": test_data["primary_flag"],
                    "ActionCode": test_data["action_code"],
                    "links": [
                        {
                            "href": f"{test_data['url']}/workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments/{test_data['child_id']}",
                        }
                    ],
                }
            ]
        }

        # Get assignment details
        response = get_assignment_details(test_data["worker_id"])

        # Ensure that get_assignment_details() executed and returned proper values
        assert response
        assert response.user_assignment_details
        assert response.user_assignment_details[0].assignment_id == test_data["assignment_id_int"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_with(
            f"workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments",
            q_expr=f"PrimaryFlag=true",
        )
