from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.initiate_manager_change import (
    initiate_manager_change,
)


def test_initiate_manager_change() -> None:
    """Test that a manager change can be initiated successfully by the `initiate_manager_change`
    tool."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D94234E9960000004AAC",
        "period_of_service_id": 300000281422248,
        "assignment_uniq_id": "00020000000EACED00057708000110D94234E9AE0000004AAC",
        "manager_uniq_id": "00020000000EACED00057708000000000009D3A00000004AAC",
        "manager_assignment_number": "E48",
        "manager_type": "PROJECT_MANAGER",
        "action_code": "MANAGER_CHANGE",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.initiate_manager_change.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "ManagerAssignmentNumber": test_data["manager_assignment_number"],
            "ManagerType": test_data["manager_type"],
            "ActionCode": test_data["action_code"],
        }

        # Initiate manager change
        response = initiate_manager_change(
            worker_id=test_data["worker_id"],
            period_of_service_id=test_data["period_of_service_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
            manager_uniq_id=test_data["manager_uniq_id"],
            manager_assignment_number=test_data["manager_assignment_number"],
            manager_type=test_data["manager_type"],
        )

        # Ensure that initiate_manager_change() returned proper list of address types
        assert response
        assert response.manager_assignment_number == test_data["manager_assignment_number"]
        assert response.manager_type == test_data["manager_type"]
        assert response.action_code == test_data["action_code"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            payload={
                "ActionCode": test_data["action_code"],
                "ManagerAssignmentNumber": test_data["manager_assignment_number"],
                "ManagerType": test_data["manager_type"],
            },
            entity=f'workers/{test_data["worker_id"]}/child/workRelationships/{test_data["period_of_service_id"]}/child/assignments/{test_data["assignment_uniq_id"]}/child/managers/{test_data["manager_uniq_id"]}',
        )
