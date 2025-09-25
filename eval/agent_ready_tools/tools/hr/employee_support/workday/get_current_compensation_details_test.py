from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_current_compensation_details import (
    _get_current_compensation_details_payload,
    get_current_compensation_details,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_current_compensation_details() -> None:
    """Test that the `get_current_compensation_details` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "0e44c92412d34b01ace61e80a47aaf6d",
        "user_id": "smorgan",
        "compensation_effective_date": "2019-04-01",
        "total_base_pay": "353562",
        "total_salary_and_allowances": "421362",
        "primary_compensation_basis": "562786.8",
        "currency": "USD",
        "frequency": "Annual",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_current_compensation_details.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_current_compensation_details.return_value = Obj(
            {
                "body": {
                    "get_workers_response": {
                        "response_data": {
                            "worker": [
                                Obj(
                                    {
                                        "worker_data": {
                                            "user_id": test_data["user_id"],
                                            "compensation_data": {
                                                "compensation_effective_date": test_data[
                                                    "compensation_effective_date"
                                                ],
                                                "employee_compensation_summary_data": {
                                                    "annualized_summary_data": {
                                                        "total_base_pay": test_data[
                                                            "compensation_effective_date"
                                                        ],
                                                        "total_salary_and_allowances": test_data[
                                                            "total_salary_and_allowances"
                                                        ],
                                                        "primary_compensation_basis": test_data[
                                                            "primary_compensation_basis"
                                                        ],
                                                        "currency_reference": {
                                                            "id": [
                                                                Obj(
                                                                    {
                                                                        "type_value": "Currency_ID",
                                                                        "value": test_data[
                                                                            "currency"
                                                                        ],
                                                                    }
                                                                )
                                                            ]
                                                        },
                                                        "frequency_reference": {
                                                            "id": [
                                                                Obj(
                                                                    {
                                                                        "type_value": "Frequency_ID",
                                                                        "value": test_data[
                                                                            "frequency"
                                                                        ],
                                                                    }
                                                                )
                                                            ]
                                                        },
                                                    }
                                                },
                                            },
                                        }
                                    }
                                )
                            ],
                        }
                    },
                },
            }
        )

        # Get current compensation details
        response = get_current_compensation_details(test_data["id"])

        # Ensure that get_current_compensation_details() executed and returned proper values
        assert response
        assert response.user_id == test_data["user_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_current_compensation_details.assert_called_once_with(
            _get_current_compensation_details_payload(user_id=test_data["id"])
        )
