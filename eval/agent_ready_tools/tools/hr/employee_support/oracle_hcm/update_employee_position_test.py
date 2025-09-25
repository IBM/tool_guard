from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_employee_position import (
    update_employee_position,
)


def test_update_employee_position() -> None:
    """Verifies that `update_employee_position` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "assignment_uniq_id": 999999999999990,
        "period_of_service_id": "300000047640662",
        "position_id": 999999999999999,
        "action_code": "TRANSFER",
        "http_code": 200,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_employee_position.get_worker_work_relationship"
    ) as mock_get_worker_work_relationship, patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_employee_position.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {"status_code": test_data["http_code"]}

        # Mock the work relationship structure
        mock_workrelation = MagicMock()
        mock_workrelation.period_of_service_id = test_data["period_of_service_id"]

        mock_all_workrelation = MagicMock()
        mock_all_workrelation.worker_work_relationship = [mock_workrelation]

        mock_get_worker_work_relationship.return_value = mock_all_workrelation

        # Update employee position
        response = update_employee_position(
            worker_id=test_data["worker_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
            position_id=test_data["position_id"],
        )

        # Ensure that update_employee_position() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments/{test_data['assignment_uniq_id']}",
            payload={
                "ActionCode": test_data["action_code"],
                "PositionId": test_data["position_id"],
            },
        )
