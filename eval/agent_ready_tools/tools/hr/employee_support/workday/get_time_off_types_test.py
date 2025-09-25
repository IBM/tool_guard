from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_time_off_types import (
    get_time_off_types,
)
from agent_ready_tools.tools.hr.employee_support.workday.workday_schemas import (
    _TIME_OFF_CATEGORY_ID,
)


def test_get_time_off_types() -> None:
    """Test that the `get_time_off_types` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "86fca18e30b810010acaee0763b50000",
        "id": "17bd6531c90c100016d74f8dfae007d0",
        "name": "Time Off Type",
        "unit": "Days",
        "quantity": "20",
        "effective_date": "2026-01-01",
        "timeoffs": "Paid Time Off",
        "daily_default_quantity": 8,
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_time_off_types.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "descriptor": test_data["name"],
                    "dailyDefaultQuantity": test_data["daily_default_quantity"],
                    "unitOfTime": {"descriptor": test_data["unit"]},
                }
            ],
        }
        # Get time off status types
        response = get_time_off_types(user_id=test_data["user_id"])

        # Ensure that get_time_off_status_types() executed and returned proper values
        assert response
        assert len(response.time_off_types)

        time_off_type = response.time_off_types[0]
        assert time_off_type.name == test_data["name"]
        assert time_off_type.type_id == test_data["id"]
        assert time_off_type.daily_default_quantity == test_data["daily_default_quantity"]
        assert time_off_type.unit_of_time == test_data["unit"]

        # Ensure the API call was made with expected parameters
        params = {
            "limit": "100",
            "offset": "0",
            "category": _TIME_OFF_CATEGORY_ID,
        }
        url = f"api/absenceManagement/v1/{mock_client.tenant_name}/workers/{test_data['user_id']}/eligibleAbsenceTypes"
        mock_client.get_request.assert_called_once_with(
            url=url,
            params=params,
        )
