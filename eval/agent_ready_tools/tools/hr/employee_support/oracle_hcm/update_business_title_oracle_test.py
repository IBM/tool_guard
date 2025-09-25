from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_business_title_oracle import (
    update_business_title_oracle,
)


def test_update_business_title_oracle() -> None:
    """Verifies that the `update_business_title_oracle` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "assignment_uniq_id": "00020000000EACED00057708000110D93445B0480000004AAC7",
        "period_of_service_id": "300000047640662",
        "assignment_id": "999999999999999",
        "action_code": "ASG_CHANGE",
        "business_title": "Senior Software developer",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_business_title_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "AssignmentId": test_data["assignment_id"],
            "AssignmentName": test_data["business_title"],
            "ActionCode": test_data["action_code"],
            "PeriodOfServiceId": test_data["period_of_service_id"],
        }

        # Update business title
        response = update_business_title_oracle(
            worker_id=test_data["worker_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
            business_title=test_data["business_title"],
            period_of_service_id=test_data["period_of_service_id"],
        )
        # Ensure that update_business_title_oracle() executed and returned proper values
        assert response
        assert response.assignment_id == test_data["assignment_id"]
        assert response.business_title == test_data["business_title"]
        assert response.action_code == test_data["action_code"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments/{test_data['assignment_uniq_id']}",
            payload={
                "ActionCode": test_data["action_code"],
                "AssignmentName": test_data["business_title"],
            },
        )
