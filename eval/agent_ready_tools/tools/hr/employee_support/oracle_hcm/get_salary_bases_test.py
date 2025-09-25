from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.common_classes import Currency
from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_salary_bases import get_salary_bases


def test_get_salary_bases() -> None:
    """Tests that the `get_salary_bases` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "AR Annual Salary Basis",
        "id": 300000124167471,
        "payment_frequency": "Annually",
        "currency_symbol": "ARS",
        "currency_symbol_output": Currency(code="ARS"),
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_salary_bases.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "SalaryBasisName": test_data["name"],
                    "SalaryBasisId": test_data["id"],
                    "FrequencyName": test_data["payment_frequency"],
                    "InputCurrencyCode": test_data["currency_symbol"],
                }
            ]
        }

        # Get salary bases.
        response = get_salary_bases(test_data["currency_symbol"])

        # Ensure that get_salary_bases returned the expected list of salary bases.
        assert response
        assert len(response.salary_bases) == 1

        salary_basis = response.salary_bases[0]
        assert salary_basis.salary_basis_name == test_data["name"]
        assert salary_basis.salary_basis_id == test_data["id"]
        assert salary_basis.payment_frequency == test_data["payment_frequency"]
        assert salary_basis.currency == test_data["currency_symbol_output"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "salaryBasisLov",
            q_expr=f"InputCurrencyCode='{test_data['currency_symbol']}'",
        )
