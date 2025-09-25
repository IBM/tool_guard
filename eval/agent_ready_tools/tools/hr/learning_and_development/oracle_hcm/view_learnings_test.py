from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_learnings import (
    LearningDetails,
    view_learnings,
)


def test_view_learnings() -> None:
    """Tests that the `view_learnings` function returns the expected response."""

    # Define test data:
    test_data = {
        "learning_name": "Charan oracle",
        "learning_status": "Not Started",
        "assigned_by": "Yugandhar Sonawane",
        "assigned_date": "2025-03-28",
        "withdrawn_date": "",
        "completion_date": "",
        "assigner": 300000281382510,
        "person_id": 300000281382510,
        "learning_status_code": "",
        "learning_title": "Charan oracle",
        "learning_record_id": "00030000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B597419030000787077080000019617D8B400780000000EACED00057708000110D942391E6D0000000B4F52415F4C4541524E4552",
        "limit": 50,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_learnings.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "learningItemTitle": test_data["learning_name"],
                    "assignmentSubStatusMeaning": test_data["learning_status"],
                    "assignerDisplayName": test_data["assigned_by"],
                    "assignedDate": test_data["assigned_date"],
                    "withdrawnDate": test_data["withdrawn_date"],
                    "completedDate": test_data["completion_date"],
                    "assignerId": test_data["assigner"],
                    "links": [
                        {
                            "href": f'https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/learnerLearningRecords/{test_data["learning_record_id"]}'
                        }
                    ],
                }
            ]
        }

        # Get users assigned learnings
        response = view_learnings(
            person_id=test_data["person_id"],
            learning_title=test_data["learning_title"],
            limit=test_data["limit"],
        ).learnings[:1]

        expected_response = [
            LearningDetails(
                learning_name="Charan oracle",
                learning_status="Not Started",
                assigned_by="Yugandhar Sonawane",
                assigned_date="2025-03-28",
                withdrawn_date="",
                completion_date="",
                assigner="Self-enrolled",
                learning_record_id="00030000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B597419030000787077080000019617D8B400780000000EACED00057708000110D942391E6D0000000B4F52415F4C4541524E4552",
            ),
        ]
        # Ensure that view_learnings() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        q_expr = f"assignedToId={test_data["person_id"]}"
        if test_data["learning_status_code"]:
            q_expr += f" and assignmentSubStatus='{test_data["learning_status_code"]}'"
        elif test_data["learning_title"]:
            q_expr += f" and learningItemTitle='{test_data["learning_title"]}'"
        params = {"limit": test_data["limit"]}
        mock_client.get_request.assert_called_once_with(
            "learnerLearningRecords",
            q_expr=q_expr,
            params=params,
            headers={"REST-Framework-Version": "4"},
        )
