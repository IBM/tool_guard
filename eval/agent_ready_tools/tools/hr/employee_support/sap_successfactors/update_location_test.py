from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_location import (
    update_location,
)


def test_update_location_existing() -> None:
    """
    Attempts to update an employees location with the existing location.

    Should return a 200 even though existing location is passed into UPSERT.
    """
    # Define test data:
    test_data = {
        "user_id": "103362",
        "start_date": "2025-02-14",
        "location_id": "1232",
        "response_http_code": 200,
        "response_message": "Success",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_location.get_sap_successfactors_client"
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

        # Update user's location
        response = update_location(
            user_id=test_data["user_id"],
            location_id=test_data["location_id"],
            start_date=test_data["start_date"],
        )

        # Ensure that update_location() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        dt = datetime.strptime(str(test_data["start_date"]), "%Y-%m-%d")
        dt = dt.replace(tzinfo=timezone.utc)
        start_date_ms = dt.strftime("%Y-%m-%dT%H:%M:%S")

        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": f"EmpJob(seqNumber=1L,startDate=datetime'{start_date_ms}',userId='{test_data['user_id']}')",
                    "type": "SFOData.EmpJob",
                },
                "location": test_data["location_id"],
            }
        )
