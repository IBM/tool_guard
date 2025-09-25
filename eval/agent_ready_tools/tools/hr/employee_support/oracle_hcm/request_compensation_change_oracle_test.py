from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_compensation_change_oracle import (
    request_compensation_change_oracle,
)


def test_request_compensation_change_oracle() -> None:
    """Tests that the `request_compensation_change_oracle` tool functions as expected."""

    # Define test data:
    test_data = {
        "effective_date_from": "2025-03-22",
        "salary_amount": 98200,
        "assignment_id": 300000047340518,
        "salary_basis_id": 300000048365126,
        "action_id": 300000000122012,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_compensation_change_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "status_code": 201,
            "DateFrom": test_data["effective_date_from"],
            "SalaryAmount": test_data["salary_amount"],
        }

        # Update salary
        response = request_compensation_change_oracle(
            assignment_id=test_data["assignment_id"],
            salary_basis_id=test_data["salary_basis_id"],
            action_id=test_data["action_id"],
            effective_date_from=test_data["effective_date_from"],
            salary_amount=test_data["salary_amount"],
        )

        # Ensure that update_salary_amount() returned proper list of address types
        assert response
        assert response.effective_date_from == test_data["effective_date_from"]
        assert response.salary_amount == test_data["salary_amount"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="salaries",
            payload={
                "AssignmentId": test_data["assignment_id"],
                "SalaryBasisId": test_data["salary_basis_id"],
                "DateFrom": test_data["effective_date_from"],
                "SalaryAmount": test_data["salary_amount"],
                "ActionId": test_data["action_id"],
            },
        )
