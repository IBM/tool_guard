from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_compensation_history import (
    get_compensation_history,
)


def test_get_compensation_history() -> None:
    """Test that the `get_compensation_history` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": 999999999999999,
        "salary_frequency_code": "M",
        "currency_code": "USD",
        "date_from": "2025-01-01",
        "date_to": "2025-01-11",
        "salary_amount": "1000",
        "annual_salary": "12000",
        "salary_amount_float": float(1000),
        "annual_salary_float": float(12000),
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_compensation_history.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "SalaryFrequencyCode": test_data["salary_frequency_code"],
                    "CurrencyCode": test_data["currency_code"],
                    "DateFrom": test_data["date_from"],
                    "DateTo": test_data["date_to"],
                    "SalaryAmount": test_data["salary_amount"],
                    "AnnualSalary": test_data["annual_salary"],
                }
            ]
        }

        # Get compensation history
        response = get_compensation_history(test_data["person_id"])

        # Ensure that get_compensation_history() got executed properly and returned proper values
        assert response
        assert response.compensation_history
        assert response.compensation_history[0].salary_amount == test_data["salary_amount_float"]
        assert response.compensation_history[0].annual_salary == test_data["annual_salary_float"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "salaries", q_expr=f"AssignmentId={test_data['person_id']}"
        )
