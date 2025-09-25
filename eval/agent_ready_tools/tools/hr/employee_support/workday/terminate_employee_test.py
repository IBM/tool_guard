from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.terminate_employee import (
    _terminate_employee_payload,
    workday_terminate_employee,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_workday_terminate_employee() -> None:
    """Testing the `terminate_employee` tool that terminates employee successufully."""

    # Define test data:
    test_data = {
        "id": "cf9f717959444023b9bc9226a2556661",
        "termination_date": "2025-04-30",
        "primary_reason": "Terminate_Employee_Voluntary_Moved",
        "terminate_value": "49d9a1c0574910013e7db0fba7a10000",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.terminate_employee.get_workday_soap_client"
    ) as mock_workday_client:

        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.terminate_event.return_value = Obj(
            {
                "body": {
                    "terminate_employee_event_response": {
                        "event_reference": {"id": [Obj({"value": test_data["terminate_value"]})]}
                    }
                }
            }
        )

        # Terminate Employee

        response = workday_terminate_employee(
            user_id=test_data["id"],
            termination_date=test_data["termination_date"],
            primary_reason=test_data["primary_reason"],
        )

        # Ensure that terminate_employee() executed and returned proper values
        assert response
        assert response.terminate_event_id == test_data["terminate_value"]

        # Ensure the API call was made with expected parameters

        mock_client.terminate_event.assert_called_once_with(
            _terminate_employee_payload(
                user_id=test_data["id"],
                termination_date=test_data["termination_date"],
                primary_reason=test_data["primary_reason"],
            )
        )
