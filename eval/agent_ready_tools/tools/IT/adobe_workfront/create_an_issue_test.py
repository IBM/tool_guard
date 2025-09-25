from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
)
from agent_ready_tools.tools.IT.adobe_workfront.create_an_issue import adobe_create_an_issue


def test_adobe_create_an_issue() -> None:
    """Verifies that the `adobe_create_an_issue` tool can successfully create an issue in Adobe
    Workfront."""

    # Define test data
    test_data = {
        "project_id": "68301d4f000e8a2fa77964c2db6de65e",
        "issue_name": "Test Issue",
        "issue_description": "This is a test issue created for unit testing.",
        "issue_priority": "NORMAL",
        "issue_id": "682b3a25000ac9d6e7196c10924a8cfc",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_an_issue.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {
                "ID": test_data["issue_id"],
                "name": test_data["issue_name"],
            }
        }

        # Create an issue
        response = adobe_create_an_issue(
            project_id=test_data["project_id"],
            issue_name=test_data["issue_name"],
            issue_description=test_data["issue_description"],
            issue_priority=test_data["issue_priority"],
        )

        # Ensure that adobe_create_an_issue() has executed and returned proper values
        assert response
        assert response.issue_id == test_data["issue_id"]
        assert response.issue_name == test_data["issue_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="optask",
            payload={
                "projectID": test_data["project_id"],
                "name": test_data["issue_name"],
                "description": test_data["issue_description"],
                "priority": int(AdobeWorkfrontPriority[test_data["issue_priority"].upper()].value),
            },
        )
