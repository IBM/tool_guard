from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.withdraw_learning import (
    withdraw_learning,
)


def test_withdraw_learning() -> None:
    """Test that a learning withdrawal can be initiated successfully by the `withdraw_learning`
    tool."""

    # Define test data:
    test_data = {
        "assignmentStatus": "ORA_ASSN_REC_WITHDRAWN",
        "reasonCode": "ORA_SS_WITHD_OTHER",
        "statusChangeComment": "blabla",
        "learning_record_id": "00030000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B597419030000787077080000019612B25800780000000EACED00057708000110D94239D5DF0000000B4F52415F4C4541524E4552",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.withdraw_learning.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "assignmentRecordId": 300000281744863,
            "assignmentStatus": test_data.get("assignmentStatus", ""),
        }

        response = withdraw_learning(
            learning_record_id=test_data.get("learning_record_id", ""),
            comment=test_data.get("statusChangeComment", ""),
        )

        assert response

        # Ensure the API call was made with expected parameters
        mock_client.update_request(
            payload={
                "assignmentStatus": test_data.get("assignmentStatus", ""),
                "reasonCode": test_data.get("reasonCode", ""),
                "statusChangeComment": test_data.get("statusChangeComment", ""),
            },
            entity=f'learnerLearningRecords/{test_data.get("learning_record_id", "")}',
        )
