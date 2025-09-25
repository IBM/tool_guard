from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.initiate_promotion import (
    initiate_promotion_sap,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_initiate_promotion() -> None:
    """Verify that the `initiate_promotion` tool can successfully update a user’s promotion
    request."""
    # Define test data:
    test_data = {
        "user_id": "103074",
        "start_date": "2025-02-21",
        "job_code": "7000013",
        "pay_grade": "GR-15",
        "message": "Promotion have been initiated successfully",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.initiate_promotion.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {"d": [{"message": test_data["message"]}]}

        # Approve the request
        response = initiate_promotion_sap(
            user_id=test_data["user_id"],
            start_date=test_data["start_date"],
            job_code=test_data["job_code"],
            pay_grade=test_data["pay_grade"],
        )

        # Ensure that initiate_promotion() executed and returned proper values
        assert response
        assert response.message == test_data["message"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "EmpJob"},
                "userId": test_data["user_id"],
                "startDate": iso_8601_to_sap_date(test_data["start_date"]),
                "jobCode": test_data["job_code"],
                "payGrade": test_data["pay_grade"],
            }
        )
