from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_manager_flag import (
    update_manager_flag,
)


def test_update_manager_flag() -> None:
    """Test that the `update_manager_flag` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "period_of_service_id": "999999999999990",
        "assignment_uniq_id": 999999999999999,
        "is_manager": True,
        "action_code": "PROMOTION",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_manager_flag.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "ManagerFlag": test_data["is_manager"],
            "ActionCode": test_data["action_code"],
            "links": [
                {
                    "rel": "self",
                    "href": f'https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/workers/{test_data["worker_id"]}',
                }
            ],
        }

        # Update Manager Flag
        response = update_manager_flag(
            worker_id=test_data["worker_id"],
            period_of_service_id=test_data["period_of_service_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
            action_code=test_data["action_code"],
            is_manager=True,
        )

        # Ensure that update_manager_flag() executed and returned proper values
        assert response
        assert response.manager_flag == test_data["is_manager"]
        assert response.action_code == test_data["action_code"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments/{test_data['assignment_uniq_id']}",
            payload={
                "ManagerFlag": test_data["is_manager"],
                "ActionCode": test_data["action_code"],
            },
        )
