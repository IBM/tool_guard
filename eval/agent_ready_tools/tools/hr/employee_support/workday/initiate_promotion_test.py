from datetime import date
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.initiate_promotion import (
    _initiate_promotion_payload,
    initiate_promotion,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_initiate_promotion() -> None:
    """Test that the `initiate_promotion` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "b7549f663f1042f7b319add5b04e5e97",
        "position_id": "94c59aabe75e4ee3ac0e2dc95991655c",
        "change_reason_id": "9a7f47f0d2d14825a2016c76af30b939",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
    }
    effective_date: date = date(2025, 2, 3)

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.initiate_promotion.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_job_change.return_value = Obj(
            {
                "body": {
                    "change_job_response": {
                        "event_reference": {
                            "id": [
                                Obj(
                                    {
                                        "value": test_data["change_id"],
                                    }
                                )
                            ]
                        }
                    },
                },
            }
        )

        # Initiate a promotion
        response = initiate_promotion(
            user_id=test_data["user_id"],
            change_reason_id=test_data["change_reason_id"],
            effective_date=effective_date,
            position_id=test_data["position_id"],
        )

        # Ensure that initiate_promotion() executed and returned proper values
        assert response
        assert response.event_id == test_data["change_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_job_change.assert_called_once_with(
            _initiate_promotion_payload(
                user_id=str(test_data["user_id"]),
                change_reason_id=str(test_data["change_reason_id"]),
                effective_date=effective_date,
                position_id=str(test_data["position_id"]),
            )
        )
