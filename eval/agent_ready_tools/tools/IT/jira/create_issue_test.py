from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.create_issue import create_an_issue


def test_create_issue() -> None:
    """Verifies that the `create_issue` tool can successfully create an issue in Jira."""

    # Define test data
    test_data = {
        "project_id": "10001",
        "issuetype_id": "10007",
        "summary": "Creating an issue",
        "description": "creating an issue in jira",
        "label": "Jira",
        "priority": "High",
        "issue_number": "IWAP-32",
    }

    # Patch `get_jira_client` to return a mock client
    with patch("agent_ready_tools.tools.IT.jira.create_issue.get_jira_client") as mock_jira_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_jira_client.return_value = mock_client
        mock_client.post_request.return_value = {"key": test_data["issue_number"]}

        # Create an issue
        response = create_an_issue(
            project_id=test_data["project_id"],
            issuetype_id=test_data["issuetype_id"],
            summary=test_data["summary"],
            description=test_data["description"],
            label=test_data["label"],
            priority=test_data["priority"],
        )

        # Ensure that create_issue() has executed and returned proper values
        assert response
        assert response.issue_number == test_data["issue_number"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="issue",
            payload={
                "fields": {
                    "project": {"id": test_data["project_id"]},
                    "issuetype": {"id": test_data["issuetype_id"]},
                    "summary": test_data["summary"],
                    "description": {
                        "content": [
                            {
                                "content": [{"text": test_data["description"], "type": "text"}],
                                "type": "paragraph",
                            }
                        ],
                        "type": "doc",
                        "version": 1,
                    },
                    "labels": [test_data["label"]],
                    "priority": {"name": test_data["priority"]},
                }
            },
        )
