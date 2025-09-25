from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.terminate_employee import (
    terminate_employee,
)


def test_terminate_employee() -> None:
    """Test the termination of an employee."""
    # Define test data:
    test_data = {
        "user_id": "103074",
        "person_id": "103002",
        "end_date": "2025-11-11",
        "event_reason_external_code": "TERRTMNT",
        "response_http_code": 200,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.terminate_employee.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"]}]
        }

        # Create the time off request
        response = terminate_employee(
            person_id_external=test_data["person_id"],
            user_id=test_data["user_id"],
            end_date=test_data["end_date"],
            event_reason_external_code=test_data["event_reason_external_code"],
        )

        # Ensure that terminate_employee() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        dt = datetime.strptime(str(test_data["end_date"]), "%Y-%m-%d")
        dt.replace(tzinfo=timezone.utc)
        end_date_milliseconds = int(dt.timestamp() * 1000)
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "EmpEmploymentTermination",
                    "type": "SFOData.EmpEmploymentTermination",
                },
                "personIdExternal": test_data["person_id"],
                "userId": test_data["user_id"],
                "endDate": f"/Date({end_date_milliseconds})/",
                "eventReason": test_data["event_reason_external_code"],
            }
        )
