from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_payslips import get_payslips


def test_get_payslips() -> None:
    """Test that the `get_payslips` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "fb151c22babd4004919999c601cc55a4",
        "descriptor": "Andrew Walton: 01/15/2019 (Regular) - Complete",
        "gross": "4853.42",
        "net": "2908.05",
        "date": "2019-01-15",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_payslips.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "descriptor": test_data["descriptor"],
                    "gross": test_data["gross"],
                    "net": test_data["net"],
                    "date": test_data["date"],
                }
            ],
        }

        # Get payslips
        response = get_payslips(user_id=test_data["user_id"])

        # Ensure that get_payslips() executed and returned proper values
        assert response
        assert len(response.payslips)
        assert response.payslips[0].description == test_data["descriptor"]
        assert response.payslips[0].gross == test_data["gross"]
        assert response.payslips[0].net == test_data["net"]
        assert response.payslips[0].date == test_data["date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/v1/{mock_client.tenant_name}/workers/{test_data['user_id']}/paySlips"
        )
