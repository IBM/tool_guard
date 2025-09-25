from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontIssueStatus,
    AdobeWorkfrontPriority,
)
from agent_ready_tools.tools.IT.adobe_workfront.update_an_issue import (
    UpdateIssueResponse,
    adobe_update_an_issue,
)


def test_adobe_update_an_issue() -> None:
    """Verifies that the `adobe_update_an_issue` tool updates the issue details in Adobe
    Workfront."""

    # Define test data:
    test_data = {
        "issue_id": "68258e6000010187da59c9ea22e73de0",
        "issue_name": "Update an issue",
        "description": "Testing",
        "status": "NEW",
        "priority": "NORMAL",
        "planned_start_date": "2025-05-15",
        "planned_completion_date": "2025-06-01",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_an_issue.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["issue_id"],
                "name": test_data["issue_name"],
                "status": test_data["status"],
            }
        }

        # Update an issue
        response = adobe_update_an_issue(
            issue_id=test_data["issue_id"],
            issue_name=test_data["issue_name"],
            description=test_data["description"],
            status=test_data["status"],
            priority=test_data["priority"],
            planned_start_date=test_data["planned_start_date"],
            planned_completion_date=test_data["planned_completion_date"],
        )

        expected_response = UpdateIssueResponse(
            issue_id=str(test_data["issue_id"]),
            issue_name=str(test_data["issue_name"]),
            status=AdobeWorkfrontIssueStatus(test_data["status"]).name,
        )

        # Ensure that adobe_update_an_issue() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"optask/{test_data['issue_id']}",
            payload={
                "name": test_data["issue_name"],
                "description": test_data["description"],
                "status": test_data["status"],
                "priority": int(AdobeWorkfrontPriority[test_data["priority"].upper()].value),
                "plannedStartDate": test_data["planned_start_date"],
                "plannedCompletionDate": test_data["planned_completion_date"],
            },
        )
