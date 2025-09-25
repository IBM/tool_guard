from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.update_an_issue import update_an_issue


def test_update_an_issue() -> None:
    """Verifies that the `update_an_issue` tool updates the issue details in Jira."""

    # Define test data:
    test_data = {
        "issue_number": "IWAP-11",
        "summary": "IWAP-11 Test Issue",
        "description": "Updates description in Jira for IWAP-11",
        "due_date": "2025-04-20",
        "account_id": "712020:1e98ed0a-0b06-4d85-967d-8763739ce9c7",
        "label": "triaged",
        "priority": "High",
        "http_code": 204,
    }

    # Patch `get_jira_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.jira.update_an_issue.get_jira_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.put_request.return_value = {"status_code": test_data["http_code"]}

        # Update an issue
        response = update_an_issue(
            issue_number=test_data["issue_number"],
            summary=test_data["summary"],
            description=test_data["description"],
            due_date=test_data["due_date"],
            account_id=test_data["account_id"],
            label=test_data["label"],
            priority=test_data["priority"],
        )

        # Ensure that update_an_issue() executed and returned proper values
        assert response
        assert response.http_code == 204

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"issue/{test_data['issue_number']}",
            payload={
                "fields": {
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
                    "priority": {"name": test_data["priority"]},
                    "duedate": test_data["due_date"],
                    "assignee": {"accountId": test_data["account_id"]},
                },
                "update": {"labels": [{"add": test_data["label"]}]},
            },
        )
