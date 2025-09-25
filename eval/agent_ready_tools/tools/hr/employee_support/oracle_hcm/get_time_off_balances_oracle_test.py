from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_time_off_balances_oracle import (
    get_time_off_balances_oracle,
)


def test_get_time_off_balances_oracle() -> None:
    """Test that the `get_time_off_balances` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": 999999999999999,
        "date": "2025-12-26",
        "plan_name": "Personal/Sick Leave AU",
        "formatted_balance": "9.17 Days",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_time_off_balances_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "planName": test_data["plan_name"],
                    "formattedBalance": test_data["formatted_balance"],
                }
            ]
        }

        # Get TimeOff balance
        response = get_time_off_balances_oracle(person_id=test_data["person_id"], date="2025-12-26")

        # Ensure that get_time_off_balances_oracle() got executed properly and returned proper values
        assert response
        assert len(response.balances)
        assert response.balances[0].time_off_balance == test_data["formatted_balance"]
        assert response.balances[0].time_off_type == test_data["plan_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "planBalances",
            finder_expr=f"findByPersonIdPlanIdLevelDate;personId={test_data['person_id']},balanceAsOfDate={test_data['date']}",
        )
