from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_all_assignment_managers import (
    get_all_assignment_managers,
)


def test_get_all_assignment_managers() -> None:
    """Tests that the `get_all_assignment_managers` tool functions as expected."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D94234E9960000004AAC",
        "period_of_service_id": 300000281422248,
        "assignment_uniq_id": "00020000000EACED00057708000110D94234E9AE0000004AAC",
        "manager_type": "PROJECT_MANAGER",
        "url": "https://example.dev.oraclepdemos.com:443/",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_all_assignment_managers.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "links": [
                        {
                            "href": f"{test_data['url']}/workers/{test_data['worker_id']}/child/{test_data['period_of_service_id']}/assignments/{test_data['assignment_uniq_id']}",
                        }
                    ],
                }
            ]
        }

        # Get all assignment managers
        response = get_all_assignment_managers(
            worker_id=test_data["worker_id"],
            period_of_service_id=test_data["period_of_service_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
            manager_type=test_data["manager_type"],
        )

        # Ensure that get_all_assignment_managers() executed and returned proper values
        assert response
        assert response.manager_uniq_id == test_data["assignment_uniq_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f'workers/{test_data["worker_id"]}/child/workRelationships/{test_data["period_of_service_id"]}/child/assignments/{test_data["assignment_uniq_id"]}/child/managers',
            q_expr=f'ManagerType={test_data["manager_type"]}',
        )
