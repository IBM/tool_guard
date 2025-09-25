from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_worker_assignment import (
    CreateWorkerAssignmentResponse,
    create_worker_assignment,
)


def test_create_worker_assignment() -> None:
    """Test that the tool `create_worker_assignment` can create an assignment for the worker in
    Oracle HCM."""

    # Define test data:
    test_data = {
        "worker_unique_id": "00020000000EACED00057708000110D934458B0C0000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196F023CC0078",
        "period_of_service_id": "300000047631130",
        "action_code": "ADD_ASSIGN",
        "business_unit_id": "300000093962136",
        "assignment_id": "140306745645424",
        "assignment_name": "Test Assign 002",
        "assignment_status": "ACTIVE",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_worker_assignment.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "AssignmentId": test_data["assignment_id"],
            "AssignmentName": test_data["assignment_name"],
            "AssignmentStatusType": test_data["assignment_status"],
        }

        # Create worker assignment
        response = create_worker_assignment(
            worker_unique_id=test_data["worker_unique_id"],
            period_of_service_id=test_data["period_of_service_id"],
            action_code=test_data["action_code"],
            business_unit_id=test_data["business_unit_id"],
        )

        expected_data = CreateWorkerAssignmentResponse(
            assignment_id=test_data["assignment_id"],
            assignment_name=test_data["assignment_name"],
            assignment_status=test_data["assignment_status"],
        )

        # Ensure that create_worker_assignment() has executed and returned proper values
        assert response
        assert response.assignment_id == expected_data.assignment_id
        assert response.assignment_name == expected_data.assignment_name
        assert response.assignment_status == expected_data.assignment_status

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"workers/{test_data["worker_unique_id"]}/child/workRelationships/{test_data["period_of_service_id"]}/child/assignments",
            payload={
                "ActionCode": test_data["action_code"],
                "BusinessUnitId": test_data["business_unit_id"],
            },
        )
