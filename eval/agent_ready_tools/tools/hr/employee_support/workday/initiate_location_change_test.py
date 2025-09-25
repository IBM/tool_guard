from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.initiate_location_change import (
    initiate_location_change,
)


def test_initiate_location_change() -> None:
    """Tests that the `initiate_location_change` tool functions properly."""

    # Define test data:
    test_data = {
        "worker_id": "de52fbe58bc84c8b90883502f9f868ed",
        "reason_id": "9a7f47f0d2d14825a2016c76af30b939",
        "location_id": "94c59aabe75e4ee3ac0e2dc95991655c",
        "effective_date": "2026-01-01",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
        "status": "Successfully Completed",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.initiate_location_change.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.initiate_job_change.return_value = {"id": test_data["change_id"]}
        mock_client.submit_job_change.return_value = {"status": {"descriptor": test_data["status"]}}

        # Initiate a location change
        response = initiate_location_change(
            worker_id=test_data["worker_id"],
            reason_id=test_data["reason_id"],
            location_id=test_data["location_id"],
            effective_date=test_data["effective_date"],
        )

        # Ensure that initiate_location_change() executed and returned proper values
        assert response
        assert not response.error
        assert response.status == test_data["status"]

        # Ensure the API calls was made with expected parameters
        mock_client.initiate_job_change.assert_called_once_with(
            test_data["worker_id"],
            {
                "date": test_data["effective_date"],
                "reason": {"id": test_data["reason_id"]},
                "location": {"id": test_data["location_id"]},
            },
        )
        mock_client.submit_job_change.assert_called_once_with(test_data["change_id"])
