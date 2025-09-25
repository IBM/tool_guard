from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.delete_an_issue import delete_an_issue


def test_delete_an_issue() -> None:
    """Tests that an issue can be deleted successfully by the `delete_an_issue` tool."""
    # Define test data:
    test_data = {"issue_number": "110A-0", "http_code": 204, "delete_sub_tasks": "true"}

    # Patch `get_jira_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.jira.delete_an_issue.get_jira_client"
    ) as mock_jira_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_jira_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Call the function
        response = delete_an_issue(issue_number=test_data["issue_number"])

        # Ensure that the delete_an_issue() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"issue/{test_data["issue_number"]}?deleteSubtasks={test_data["delete_sub_tasks"]}"
        )
