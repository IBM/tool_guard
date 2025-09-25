from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_business_title_oracle import (
    get_business_title_oracle,
)


def test_get_business_title() -> None:
    """Test that the `get_business_title` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445295F0000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001975C49580078",
        "service_id": "300000047606125",
        "assignment_id": "300000047606131",
        "business_title": "Senior Architect",
        "url": "https://test.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_business_title_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AssignmentId": test_data["assignment_id"],
                    "AssignmentName": test_data["business_title"],
                }
            ]
        }

        # Update business title
        response = get_business_title_oracle(
            worker_id=test_data["worker_id"],
            service_id=test_data["service_id"],
            assignment_id=test_data["assignment_id"],
        )

        # Ensure that get_business_title() executed and returned proper values
        assert response
        assert response.business_title == test_data["business_title"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/workRelationships/{test_data['service_id']}/child/assignments",
        )
