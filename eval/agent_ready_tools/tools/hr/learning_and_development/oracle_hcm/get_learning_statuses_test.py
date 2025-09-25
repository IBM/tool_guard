from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_learning_statuses import (
    get_learning_statuses,
)


def test_get_learning_statuses() -> None:
    """Test that the `get_learning_statuses` function returns the expected response."""
    # Define test data:
    test_data = {
        "status": "Not Started",
        "person_id": 300000281382510,
        "learning_status_code": "ORA_ASSN_REC_NOTSTARTED",
        "learning_name": "00030000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001960D8BFC00780000000EACED00057708000110D942391E6D0000000B4F52415F4C4541524E4552",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_learning_statuses.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "items": [
                {
                    "LookupCode": test_data["learning_status_code"],
                    "links": [
                        {
                            "href": f"https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/learnerLearningRecords/{test_data['learning_name']}",
                        }
                    ],
                }
            ]
        }
        # Get learning statuses
        response = get_learning_statuses(
            status=test_data["status"],
            person_id=test_data["person_id"],
        )
        # Ensure that get_learning_statuses() executed and returned proper values
        assert response
        assert response.learning_status_code == test_data["learning_status_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_with(
            f"learnerLearningRecords/{test_data["learning_name"]}/lov/AssignmentStatusLOV",
            q_expr=f"Meaning='{test_data['status']}'",
        )
