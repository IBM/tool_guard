from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_time_off_balances import (
    get_time_off_balances,
)


def test_get_time_off_balances() -> None:
    """Test that the `get_time_off_balances` function returns the expected response."""
    # Define test data:
    test_data = {
        "date": "2025-02-17",
        "user_id": "100052",
        "time_off_type": "Comp Time",
        "time_off_balance": "00:00 hours",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_time_off_balances.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_time_management_request.return_value = {
            "value": [
                {
                    "timeAccount": {
                        "timeAccountType": {"externalName": test_data["time_off_type"]}
                    },
                    "balances": {
                        "available": {"formattedWithUnitRoundedDown": test_data["time_off_balance"]}
                    },
                }
            ]
        }

        # Get time off balances
        response = get_time_off_balances(date=test_data["date"], user_id=test_data["user_id"])

        # Ensure that get_time_off_balances() executed and returned proper values
        assert response
        assert len(response.balances)
        assert response.balances[0].time_off_type == test_data["time_off_type"]
        assert response.balances[0].time_off_balance == test_data["time_off_balance"]

        # Ensure the API call was made with expected parameters
        mock_client.get_time_management_request.assert_called_once_with(
            endpoint="timeAccountBalances",
            params={"$at": test_data["date"], "assignmentId": test_data["user_id"]},
        )
