from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.initiate_organization_transfer import (
    initiate_organization_transfer,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_initiate_organization_transfer() -> None:
    """Test that an organization transfer can be initiated successfully by the
    `initiate_organization_transfer` tool."""
    # Define test data:
    test_data = {
        "user_id": "103362",
        "business_unit": "CORP",
        "division": "CORP_SVCS",
        "department": "5000148",
        "start_date": "2025-02-20",
        "response_http_code": "200",
        "response_message": "Initiated organization transfer successfully.",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.initiate_organization_transfer.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        # Initiate organisation transfer
        response = initiate_organization_transfer(
            user_id=test_data["user_id"],
            business_unit=test_data["business_unit"],
            division=test_data["division"],
            department=test_data["department"],
            start_date=test_data["start_date"],
        )

        # Ensure that initiate_organization_transfer() executed and returned proper values
        assert response
        assert response.http_code == int(test_data["response_http_code"])
        assert response.message == test_data["response_message"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "EmpJob", "type": "SFOData.EmpJob"},
                "userId": test_data["user_id"],
                "businessUnit": test_data["business_unit"],
                "division": test_data["division"],
                "department": test_data["department"],
                "startDate": iso_8601_to_sap_date(test_data["start_date"]),
            }
        )
