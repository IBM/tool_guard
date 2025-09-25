from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_end_employment_date import (
    update_end_employment_date,
)


def test_update_end_employment_date() -> None:
    """Test that the end employment date can be updated successfully by the
    `update_end_employment_date` tool."""
    # Define test data:
    test_data = {
        "person_id": "109031",
        "user_id": "109031",
        "end_date": "2026-01-01",
        "event_reason": "TERITWPY",
        "response_http_code": 200,
        "response_message": "success",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_end_employment_date.get_sap_successfactors_client"
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

        # Update end employment_date
        response = update_end_employment_date(
            person_id_external=test_data["person_id"],
            user_id=test_data["user_id"],
            end_date=test_data["end_date"],
            event_reason=test_data["event_reason"],
        )

        # Ensure that update_end_employment_date() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

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
                "eventReason": test_data["event_reason"],
            }
        )
