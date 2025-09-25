from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_time_off import get_time_off
from agent_ready_tools.tools.hr.employee_support.workday.workday_schemas import (
    _TIME_OFF_CATEGORY_ID,
)


def test_get_time_off() -> None:
    """Verifies that the `get_time_off` tool can successfully retrieve time off entries in
    Workday."""

    # Define test data
    test_data = {
        "user_id": "de52fbe58bc84c8b90883502f9f868ed",
        "from_date": "2025-01-01",
        "to_date": "2025-01-31",
        "status": "Approved",
        "status_type_id": "0391102bd1b542538d996936c8fa2fa7",
        "time_off_type_id": "4369c324b54b10100568d824579d0000",
        "quantity": "8",
        "unit": "Hours",
        "time_off_type": "Vacation (Hours)",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_time_off.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "status": {
                        "descriptor": test_data["status"],
                        "id": test_data["status_type_id"],
                    },
                    "timeOffType": {
                        "descriptor": test_data["time_off_type"],
                        "id": test_data["time_off_type_id"],
                    },
                    "quantity": test_data["quantity"],
                    "unit": {"descriptor": test_data["unit"]},
                    "date": test_data["from_date"],
                }
            ],
        }

        # Call the `get_time_off` function
        response = get_time_off(
            user_id=test_data["user_id"],
            from_date=test_data["from_date"],
            to_date=test_data["to_date"],
            status_type_id=test_data["status_type_id"],
            time_off_type_id=test_data["time_off_type_id"],
        )

        assert response
        assert len(response.time_off_entries)
        assert response.time_off_entries[0].status == test_data["status"]
        assert response.time_off_entries[0].time_off_type == test_data["time_off_type"]
        assert response.time_off_entries[0].quantity == test_data["quantity"]
        assert response.time_off_entries[0].unit == test_data["unit"]
        assert response.time_off_entries[0].date == test_data["from_date"]

        # Ensure the API call was made with expected parameters
        params = {
            "fromDate": test_data["from_date"],
            "toDate": test_data["to_date"],
            "status": test_data["status_type_id"],
            "timeOffType": test_data["time_off_type_id"],
            "category": _TIME_OFF_CATEGORY_ID,
        }
        url = (
            f"api/absenceManagement/v1/{mock_client.tenant_name}/workers/{test_data['user_id']}"
            "/timeOffDetails"
        )
        mock_client.get_request.assert_called_once_with(
            url=url,
            params=params,
        )
