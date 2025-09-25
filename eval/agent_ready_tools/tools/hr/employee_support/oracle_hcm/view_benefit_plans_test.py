from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.view_benefit_plans import (
    view_benefit_plans,
)


def test_view_benefit_plans() -> None:
    """Test that the `view_benefit_plans` function returns a valid OracleBenefitPlansResponse."""

    # Define test data:
    test_data = {
        "plan_id": 300000047958114,
        "plan_name": "Holiday Purchase",
        "program_name": "UK Benefit Program",
        "option_name": "Holiday Purchase - 1 Day",
        "coverage_amount": "",
        "person_id": 300000157003563,
        "person_name": "John Patterson",
        "enrollment_coverage_start_date": "2019-01-01",
        "enrollment_coverage_end_date": "",
        "currency_code": "GBP",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.view_benefit_plans.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PlanId": test_data["plan_id"],
                    "PlanName": test_data["plan_name"],
                    "PersonName": test_data["person_name"],
                    "ProgramName": test_data["program_name"],
                    "OptionName": test_data["option_name"],
                    "CoverageAmount": test_data["coverage_amount"],
                    "EnrollmentCoverageStartDate": test_data["enrollment_coverage_start_date"],
                    "EnrollmentCoverageEndDate": test_data["enrollment_coverage_end_date"],
                    "CurrencyCode": test_data["currency_code"],
                }
            ]
        }

        # Get benefit plans
        response = view_benefit_plans(person_id=test_data["person_id"])

        # Ensure that view_benefit_plans() got executed properly and returned proper values
        assert response
        assert len(response.benefit_plans)
        assert response.benefit_plans[0].plan_id == test_data["plan_id"]
        assert response.benefit_plans[0].plan_name == test_data["plan_name"]
        assert response.benefit_plans[0].person_name == test_data["person_name"]
        assert response.benefit_plans[0].program_name == test_data["program_name"]
        assert response.benefit_plans[0].option_name == test_data["option_name"]
        assert response.benefit_plans[0].coverage_amount == test_data["coverage_amount"]
        assert (
            response.benefit_plans[0].enrollment_coverage_start_date
            == test_data["enrollment_coverage_start_date"]
        )
        assert (
            response.benefit_plans[0].enrollment_coverage_end_date
            == test_data["enrollment_coverage_end_date"]
        )
        assert response.benefit_plans[0].currency_code == test_data["currency_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "benefitEnrollments",
            q_expr=f"PersonId={test_data['person_id']}",
        )
