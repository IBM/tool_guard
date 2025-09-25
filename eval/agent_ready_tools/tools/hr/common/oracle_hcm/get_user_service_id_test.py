from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.oracle_hcm.get_user_service_id import get_user_service_id


def test_get_user_service_id() -> None:
    """Tests that the `get_user_service_id` tool functions as expected."""

    # Define test data:
    test_data = {
        "email": "ALAN.COOK_etaj-dev23@oraclepdemos.com",
        "person_id": "300000047606111",
        "worker_id": "00020000000EACED00057708000110D93445295F0000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001975C49580078",
        "service_id": "300000047606125",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.oracle_hcm.get_user_service_id.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PeriodOfServiceId": test_data["service_id"],
                }
            ]
        }

        # Get User IDs.
        response = get_user_service_id(worker_id=test_data["worker_id"])
        # Ensure that get_user_service_id() got executed properly and returned proper values
        assert response
        assert response.service_id == int(test_data["service_id"])

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"workers/{test_data["worker_id"]}/child/workRelationships"
        )
