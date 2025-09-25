from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.oracle_hcm.get_user_oracle_ids import get_user_oracle_ids


def test_get_user_oracle_ids() -> None:
    """Tests that the `get_user_oracle_ids` tool functions as expected."""

    # Define test data:
    test_data = {
        "email": "john.smith@oraclepdemos.com",
        "person_id": "999999999999999",
        "worker_id": "00020000000EACED00057708000110D9344C61220000004AAC",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.oracle_hcm.get_user_oracle_ids.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PersonId": test_data["person_id"],
                    "links": [
                        {
                            "href": f'https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/workers/{test_data["worker_id"]}'
                        }
                    ],
                }
            ]
        }

        # Get User IDs.
        response = get_user_oracle_ids(email=test_data["email"])
        # Ensure that get_user_oracle_ids() got executed properly and returned proper values
        assert response
        assert response.person_id == int(test_data["person_id"])
        assert response.worker_id == test_data["worker_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "workers",
            q_expr=f"emails.EmailAddress='{test_data['email']}'",
            headers={"REST-Framework-Version": "4"},
        )
