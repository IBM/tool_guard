from datetime import datetime
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_current_compensation_details_oracle import (
    get_current_compensation_details_oracle,
)


def test_get_current_compensation_details() -> None:
    """Tests that the `get_current_compensation_details_oracle` tool functions as expected."""

    # Define test data:
    test_data = {
        "assignment_id": "999999999999999",
        "annual_salary": "39527.24",
        "currency": "SGD",
        "comparative_ratio": "131.76",
        "adjustment_amount": "1.72",
        "adjustment_percentage": "4.99",
        "effective_period": "2024-07-01",
        "action_name": "Allocate Workforce Compensation",
        "salary_basis_name": "US1 Hourly Rate",
        "legal_employer_name": "US1 Legal Entity",
        "grade_name": "Admin03",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_current_compensation_details_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AnnualSalary": test_data["annual_salary"],
                    "CurrencyCode": test_data["currency"],
                    "CompaRatio": test_data["comparative_ratio"],
                    "AdjustmentAmount": test_data["adjustment_amount"],
                    "AdjustmentPercentage": test_data["adjustment_percentage"],
                    "DateFrom": test_data["effective_period"],
                    "ActionName": test_data["action_name"],
                    "SalaryBasisName": test_data["salary_basis_name"],
                    "LegalEmployerName": test_data["legal_employer_name"],
                    "GradeName": test_data["grade_name"],
                }
            ]
        }

        # Get current compensation details
        response = get_current_compensation_details_oracle(assignment_id=test_data["assignment_id"])

        # Ensure that get_current_compensation_details_oracle() got executed properly and returned proper values
        assert response
        assert response.annual_salary == test_data["annual_salary"]
        assert response.currency == test_data["currency"]
        assert response.comparative_ratio == test_data["comparative_ratio"]
        assert response.adjustment_amount == test_data["adjustment_amount"]
        assert response.adjustment_percentage == test_data["adjustment_percentage"]
        assert response.effective_period == test_data["effective_period"]
        assert response.action_name == test_data["action_name"]
        assert response.salary_basis_name == test_data["salary_basis_name"]
        assert response.legal_employer_name == test_data["legal_employer_name"]
        assert response.grade_name == test_data["grade_name"]

        # Ensure the API call was made with expected parameters
        current_date = datetime.today().date()
        mock_client.get_request.assert_called_once_with(
            entity="salaries",
            finder_expr=f'findByAssignmentIdAndDate;AssignmentId={test_data["assignment_id"]},EffectiveDate="{current_date}"',
        )
