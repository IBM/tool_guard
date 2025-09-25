from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons import (
    get_job_change_reasons,
)


def test_get_job_change_reasons() -> None:
    """Test that the `get_job_change_reasons` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "9e616caff5b1480aab04f1ce22d7e7d4",
        "descriptor": "Money $$$",
        "is_for_employee": False,
        "is_for_contingent_worker": False,
        "manager_reason": True,
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "descriptor": test_data["descriptor"],
                    "isForEmployee": test_data["is_for_employee"],
                    "isForContingentWorker": test_data["is_for_contingent_worker"],
                    "managerReason": test_data["manager_reason"],
                }
            ],
            "total": 1,
        }

        # Get job change reasons
        response = get_job_change_reasons()

        # Ensure that get_job_change_reasons() executed and returned proper values
        assert response
        assert len(response.job_change_reasons)
        assert response.job_change_reasons[0].id == test_data["id"]
        assert response.job_change_reasons[0].descriptor == test_data["descriptor"]
        assert response.job_change_reasons[0].manager_reason == test_data["manager_reason"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/v1/{mock_client.tenant_name}/jobChangeReasons"
        )
