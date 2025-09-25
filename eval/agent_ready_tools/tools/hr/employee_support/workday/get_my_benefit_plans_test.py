from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_my_benefit_plans import (
    _get_my_benefit_plans_payload,
    get_my_benefit_plans,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_my_benefit_plans() -> None:
    """Test that the `get_my_benefit_plans` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "0e44c92412d34b01ace61e80a47aaf6d",
        "benefit_plan_name": "Charles Schwab",
        "coverage_begin_date": "2008-01-01",
        "deduction_begin_date": "2008-01-01",
        "coverage": "8",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_my_benefit_plans.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_my_benefit_plans.return_value = Obj(
            {
                "body": {
                    "get_workers_response": {
                        "response_data": {
                            "worker": [
                                Obj(
                                    {
                                        "worker_data": {
                                            "benefit_enrollment_data": {
                                                "retirement_savings_data": {
                                                    "retirement_savings_period_data": [
                                                        Obj(
                                                            {
                                                                "retirement_savings_coverage_data": [
                                                                    Obj(
                                                                        {
                                                                            "benefit_election_data": {
                                                                                "benefit_plan_summary_data": {
                                                                                    "benefit_provider_summary_data": {
                                                                                        "benefit_provider_name": test_data[
                                                                                            "benefit_plan_name"
                                                                                        ]
                                                                                    }
                                                                                },
                                                                                "coverage_begin_date": test_data[
                                                                                    "coverage_begin_date"
                                                                                ],
                                                                                "deduction_begin_date": test_data[
                                                                                    "deduction_begin_date"
                                                                                ],
                                                                            },
                                                                            "employee_contribution_amount_data": {
                                                                                "contribution_amount_data": test_data[
                                                                                    "coverage"
                                                                                ]
                                                                            },
                                                                        }
                                                                    )
                                                                ]
                                                            }
                                                        )
                                                    ],
                                                }
                                            }
                                        }
                                    }
                                )
                            ],
                        }
                    }
                }
            }
        )

        # Get benfit plans details

        response = get_my_benefit_plans(test_data["id"])  # Steve Morgan.

        assert response
        assert response.benefit_plan_name == test_data["benefit_plan_name"]
        assert response.coverage == test_data["coverage"]

        # Ensure the API call was made with expected parameters

        mock_client.get_my_benefit_plans.assert_called_once_with(
            _get_my_benefit_plans_payload(user_id=test_data["id"])
        )
