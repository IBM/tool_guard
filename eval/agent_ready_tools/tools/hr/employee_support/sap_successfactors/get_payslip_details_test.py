from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_payslip_details import (
    get_payslip_details,
)


def test_get_payslip_details() -> None:
    """Test that the `get_payslip_details` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "82094",
        "start_date": "2018-01-01",
        "end_date": "2018-01-15",
        "currency": "USD",
        "wage_type_1": "GROSS",
        "wage_type_1_amount": 2466.66,
        "wage_type_2": "TAXES",
        "wage_type_2_amount": 556.58,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_payslip_details.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "startDateWhenPaid": test_data["start_date"],
                        "endDateWhenPaid": test_data["end_date"],
                        "currency": test_data["currency"],
                        "employeePayrollRunResultsItems": {
                            "results": [
                                {
                                    "wageType": test_data["wage_type_1"],
                                    "amount": str(test_data["wage_type_1_amount"]),
                                },
                                {
                                    "wageType": test_data["wage_type_2"],
                                    "amount": str(test_data["wage_type_2_amount"]),
                                },
                            ]
                        },
                    }
                ]
            }
        }

        # Get location ID
        response = get_payslip_details(
            test_data["user_id"], test_data["start_date"], str(test_data["end_date"])
        )

        # Ensure that get_payslip_details() executed and returned proper values
        assert response
        assert len(response.payslips)
        assert response.payslips[0].start_date == test_data["start_date"]
        assert response.payslips[0].end_date == test_data["end_date"]
        assert len(response.payslips[0].wages)
        assert response.payslips[0].wages[0].wage_type == test_data["wage_type_1"]
        assert response.payslips[0].wages[0].amount == str(test_data["wage_type_1_amount"])
        assert response.payslips[0].wages[1].wage_type == test_data["wage_type_2"]
        assert response.payslips[0].wages[1].amount == str(test_data["wage_type_2_amount"])

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "EmployeePayrollRunResults",
            filter_expr=f"userId eq '{test_data['user_id']}' and startDateWhenPaid ge '{test_data['start_date']}' and endDateWhenPaid le '{test_data['end_date']}'",
            expand_expr="employeePayrollRunResultsItems",
        )
