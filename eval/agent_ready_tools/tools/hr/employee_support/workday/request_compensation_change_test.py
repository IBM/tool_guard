from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.request_compensation_change import (
    _request_compensation_change_payload,
    request_compensation_change,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_request_hourly_compensation_change() -> None:
    """Test that request_compensation_change gets the expected response."""

    # Define test data:
    test_data = {
        "user_id": "86fca18e30b810010acaee0763b50000",
        "reason_id": "Request_Compensation_Change_Adjustment_Ad-h",
        "effective_date": "2025-02-20",
        "new_compensation": "6.06",
        "request_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.request_compensation_change.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.request_compensation_change.return_value = Obj(
            {
                "body": {
                    "request_compensation_change_response": {
                        "request_compensation_change_event_reference": {
                            "id": [
                                Obj(
                                    {
                                        "value": test_data["request_id"],
                                    }
                                )
                            ]
                        }
                    },
                },
            }
        )

        # Request a compensation change
        response = request_compensation_change(
            test_data["user_id"],
            test_data["reason_id"],
            test_data["effective_date"],
            test_data["new_compensation"],
        )

        # Ensure that request_compensation_change() executed and returned proper values
        assert response
        assert response.request_id == test_data["request_id"]

        # Ensure the API call was made with expected parameters
        mock_client.request_compensation_change.assert_called_once_with(
            _request_compensation_change_payload(
                user_id=test_data["user_id"],
                reason_id=test_data["reason_id"],
                effective_date=test_data["effective_date"],
                new_compensation_amount=test_data["new_compensation"],
            )
        )
