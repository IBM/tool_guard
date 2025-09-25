from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_disability_status import (
    _update_disability_status_payload,
    update_disability_status,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_update_disability_status() -> None:
    """Test that the `update_disability_status` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "3bcc416214054db6911612ef25d51e9f",
        "id": "85883bbbf7a644b3b67dcda864b52c91",
        "reference_id": "85883bbbf7a644b3b67dcda864b52c91",
        "status_date": "2025-02-20",
        "date_known": "2025-02-21",
        "end_date": "2025-02-22",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_disability_status.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.update_disability_status.return_value = Obj(
            {
                "body": {
                    "change_personal_information_response": {
                        "personal_information_data": {
                            "disability_information_data": {
                                "disability_status_information_data": [
                                    Obj(
                                        {
                                            "disability_status_data": {
                                                "disability_reference": {
                                                    "id": [
                                                        Obj({"value": test_data["reference_id"]}),
                                                        Obj({"value": test_data["id"]}),
                                                    ]
                                                },
                                                "disability_status_date": test_data["status_date"],
                                                "disability_date_known": test_data["date_known"],
                                                "disability_end_date": test_data["end_date"],
                                            },
                                        }
                                    )
                                ]
                            }
                        }
                    },
                },
            }
        )

        # Update disability status
        response = update_disability_status(
            test_data["user_id"],
            test_data["reference_id"],
            test_data["status_date"],
            test_data["date_known"],
            test_data["end_date"],
        )

        # Ensure that update_disability_status() executed and returned proper values
        assert response
        assert response.disability_reference_id == test_data["reference_id"]
        assert response.disability_id == test_data["id"]
        assert response.status_date == test_data["status_date"]
        assert response.date_known == test_data["date_known"]
        assert response.end_date == test_data["end_date"]

        # Ensure the API call was made with expected parameters
        mock_client.update_disability_status.assert_called_once_with(
            _update_disability_status_payload(
                user_id=test_data["user_id"],
                disability_reference_id=test_data["reference_id"],
                disability_status_date=test_data["status_date"],
                disability_date_known=test_data["date_known"],
                disability_end_date=test_data["end_date"],
            )
        )
