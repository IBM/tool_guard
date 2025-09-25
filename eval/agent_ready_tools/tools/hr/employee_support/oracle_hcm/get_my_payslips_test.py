from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_my_payslips import get_my_payslips


def test_get_my_payslips() -> None:
    """Test that the `get_my_payslips` function returns a valid OraclePayslipResponse."""

    # Define test data:
    test_data = {
        "person_id": 999999999999999,
        "start_date": "2015-12-26",
        "end_date": "2016-01-08",
        "currency": "USD",
        "amount": float(1511.64),
        "payment_date": "2016-01-08",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_my_payslips.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "Amount": test_data["amount"],
                    "PeriodStartDate": test_data["start_date"],
                    "PeriodEndDate": test_data["end_date"],
                    "CurrencyCode": test_data["currency"],
                    "PaymentDate": test_data["payment_date"],
                }
            ]
        }

        # Get user payslips
        response = get_my_payslips(
            test_data["person_id"], test_data["start_date"], test_data["end_date"]
        )

        # Ensure that get_my_payslips() got executed properly and returned proper values
        assert response
        assert len(response.payslips)
        assert response.payslips[0].amount == test_data["amount"]
        assert response.payslips[0].payment_date == test_data["payment_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "payslips",
            q_expr=f"PersonId={test_data['person_id']};PeriodStartDate>='{test_data['start_date']}';PeriodEndDate<='{test_data['end_date']}'",
        )
