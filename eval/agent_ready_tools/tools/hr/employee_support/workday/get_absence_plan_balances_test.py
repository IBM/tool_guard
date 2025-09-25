from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_absence_plan_balances import (
    get_absence_plan_balances,
)


def test_get_absence_plan_balances() -> None:
    """Test that the `get_absence_plan_balances` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "0e44c92412d34b01ace61e80a47aaf6d",
        "plan_name": "Anniversary Vacation",
        "unit": "Days",
        "quantity": "0",
        "effective_date": "2026-01-01",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_absence_plan_balances.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "absencePlan": {"descriptor": test_data["plan_name"]},
                    "unit": {"descriptor": test_data["unit"]},
                    "quantity": test_data["quantity"],
                    "effectiveDate": test_data["effective_date"],
                }
            ],
        }

        # Get Absence plan balances
        response = get_absence_plan_balances(user_id=test_data["user_id"])

        # Ensure that get_absence_plan_balances() executed and returned proper values
        assert response
        assert len(response.absence_plans) == 1
        assert response.absence_plans[0].plan_name == test_data["plan_name"]
        assert response.absence_plans[0].unit == test_data["unit"]
        assert response.absence_plans[0].quantity == test_data["quantity"]
        assert response.absence_plans[0].effective_date == test_data["effective_date"]

        # Ensure the API call was made with expected parameters
        url = f"api/absenceManagement/v1/{mock_client.tenant_name}/balances"
        params = {"worker": test_data["user_id"]}
        mock_client.get_request.assert_called_once_with(url=url, params=params)
