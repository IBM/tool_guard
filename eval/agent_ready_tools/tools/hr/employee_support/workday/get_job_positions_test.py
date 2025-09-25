from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_job_positions import get_job_positions


def test_get_job_positions() -> None:
    """Tests that the `get_job_positions` tool returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "d3fd6c7cdbf1101b037a55f03aea0c20",
        "effective_date": "2025-09-01",
        "id": "9e616caff5b1480aab04f1ce22d7e7d4",
        "descriptor": "Software Engineer",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_positions.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "descriptor": test_data["descriptor"],
                }
            ],
            "total": 1,
        }

        # Get job change reasons categories
        response = get_job_positions(
            user_id=test_data["user_id"], effective_date=test_data["effective_date"]
        )

        # Ensure that get_job_positions() executed and returned proper values
        assert response
        assert len(response.job_positions)
        assert response.job_positions[0].id == test_data["id"]
        assert response.job_positions[0].descriptor == test_data["descriptor"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/staffing/v5/{mock_client.tenant_name}/values/jobChangesGroup/jobs",
            params={"worker": "d3fd6c7cdbf1101b037a55f03aea0c20", "effectiveDate": "2025-09-01"},
        )
