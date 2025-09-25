from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.oracle_hcm.get_user_ids_based_on_person_number import (
    get_user_ids_based_on_person_number,
)


def test_get_user_oracle_ids_based_on_person_number() -> None:
    """Tests that the `get_user_ids_based_on_person_number` function returns the expected
    response."""

    # Define test data:
    test_data = {
        "person_number": "6522",
        "person_id": "999999999999999",
        "worker_id": "00020000000EACED00057708000110D9344C61220000004AAC",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.oracle_hcm.get_user_ids_based_on_person_number.get_oracle_hcm_client"
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
                            "href": f"example.com/{test_data['person_id']}/child/{test_data['worker_id']}",
                        }
                    ],
                }
            ]
        }

        # Get users ids based on person number
        response = get_user_ids_based_on_person_number(person_number=test_data["person_number"])

        # Ensure that get_user_ids_based_on_person_number() executed and returned proper values
        assert response
        assert response.worker_id == test_data["worker_id"]
        assert response.person_id == int(test_data["person_id"])

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "workers",
            q_expr=f"PersonNumber='{test_data['person_number']}'",
            headers={"REST-Framework-Version": "4"},
        )
