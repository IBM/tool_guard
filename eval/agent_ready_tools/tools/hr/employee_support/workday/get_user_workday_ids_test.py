from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_user_workday_ids import (
    get_user_workday_ids,
)


def test_get_user_workday_ids() -> None:
    """Test that the `get_user_workday_ids` function returns the expected response."""

    # Define test data:
    test_data = {
        "total": 1,
        "descriptor": "Steve Morgan",  # Worker's name.
        "email": "Gopala.Divya@partner.ibm.com",
        "user_id": "6dcb8106e8b74b5aabb1fc3ab8ef2b92",
        "person_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_user_workday_ids.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "total": test_data["total"],
            "data": [
                {
                    "id": test_data["user_id"],
                    "descriptor": test_data["descriptor"],
                    "person": {
                        "id": test_data["person_id"],
                        "email": test_data["email"],
                    },
                }
            ],
        }

        # Get user's workday ids
        response = get_user_workday_ids(name=test_data["descriptor"])

        # Ensure that get_user_workday_ids() executed and returned proper values
        assert response

        worker = response.workers[0]
        assert worker.email == test_data["email"]
        assert worker.name == test_data["descriptor"]
        assert worker.person_id == test_data["person_id"]
        assert worker.user_id == test_data["user_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/staffing/v6/{mock_client.tenant_name}/workers",
            params={"search": test_data["descriptor"]},
        )
