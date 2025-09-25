from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_all_managers import get_all_managers


def test_get_all_managers() -> None:
    """Test that the `get_all_managers` function returns the expected response."""

    # Define test data:
    test_data = {
        "number": "48",
        "display_name": "Test user",
        "email_address": "test@example.com",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_all_managers.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AssignmentNumber": f'E{test_data["number"]}',
                    "DisplayName": f'E{test_data["display_name"]}',
                    "EmailAddress": f'E{test_data["email_address"]}',
                }
            ]
        }

        # Get all managers
        response = get_all_managers(test_data["number"])

        # Ensure that get_all_managers() executed and returned proper values
        assert response
        assert len(response.managers)
        assert response.managers[0].manager_assignment_number == f'E{test_data["number"]}'
        assert response.managers[0].manager_display_name == f'E{test_data["display_name"]}'
        assert response.managers[0].manager_email_address == f'E{test_data["email_address"]}'

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "talentReviewManagersLOV", q_expr=f"PersonNumber={test_data['number']}"
        )
