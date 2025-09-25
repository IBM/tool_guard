from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_pay_grades import (
    get_pay_grades,
)


def test_get_pay_grades() -> None:
    """Verifies that the `get_pay_grades` tool is retrieving data successfully."""
    # Define test data:
    test_data = {
        "external_code": "GR-01",
        "name": "Salary Grade 01",
        "level": "1",
        "status": "A",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_pay_grades.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalCode": test_data["external_code"],
                        "name": test_data["name"],
                        "paygradeLevel": test_data["level"],
                        "status": test_data["status"],
                    }
                ]
            }
        }

        # Get pay grades
        response = get_pay_grades()

        # Ensure that get_pay_grades() executed and returned proper values
        assert response
        assert len(response.pay_grades)
        assert response.pay_grades[0].code == test_data["external_code"]
        assert response.pay_grades[0].name == test_data["name"]
        assert response.pay_grades[0].level == test_data["level"]
        assert response.pay_grades[0].status == test_data["status"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="FOPayGrade", select_expr="externalCode,paygradeLevel,name,internalCode,status"
        )
