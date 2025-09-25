from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.get_issues import Issue, IssuesResponse, get_issues


def test_get_issues_first() -> None:
    """Tests that the issues can be retrieved by the `get_issues` tool."""

    # Define test data
    test_data: dict[str, Any] = {
        "issue_number": "WO-6",
        "summary": "testing postman",
        "description": "nothing",
        "author_name": "Agent tool",
        "created_date": "2025-05-30T16:34:23.241+0530",
        "file_name": "testing file",
        "progress_percent": 0,
        "status": "Open",
        "output_nextPageToken": "ChkjU3RyaW5nJlUwTlNWVTA9JUludCZNelU9EAEY8dLjm-QyIhpwcm9qZWN0PSJNeSBTY3J1bSBQcm9qZWN0Ig==",
        "labels": ["Jira"],
        "due_date": "2025-06-07",
        "priority": "Medium",
        "project_name": "Watson Orchestrate",
    }
    limit = 3

    # Patch `get_jira_client` to return a mock client
    with patch("agent_ready_tools.tools.IT.jira.get_issues.get_jira_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "issues": [
                {
                    "key": test_data["issue_number"],
                    "versionedRepresentations": {
                        "summary": {"1": test_data["summary"]},
                        "description": {
                            "1": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": test_data["description"]}
                                        ],
                                    }
                                ],
                            }
                        },
                        "attachment": {"1": [{"filename": test_data["file_name"]}]},
                        "assignee": {"1": {"displayName": test_data["author_name"]}},
                        "created": {"1": test_data["created_date"]},
                        "progress": {"1": {"progress": test_data["progress_percent"], "total": 0}},
                        "status": {"1": {"name": test_data["status"]}},
                        "labels": {"1": test_data["labels"]},
                        "duedate": {"1": test_data["due_date"]},
                        "priority": {"1": {"name": test_data["priority"]}},
                    },
                }
            ],
            "nextPageToken": test_data["output_nextPageToken"],
        }

        # Call the function
        response = get_issues(
            project_name=test_data["project_name"],
            limit=limit,
            next_page_token=test_data["output_nextPageToken"],
        )

        # Expected output
        expected_output = IssuesResponse(
            issues=[
                Issue(
                    summary=test_data["summary"],
                    issue_number=test_data["issue_number"],
                    description=test_data["description"],
                    author_name=test_data["author_name"],
                    created_date=test_data["created_date"],
                    file_name=test_data["file_name"],
                    progress_percent=test_data["progress_percent"],
                    status=test_data["status"],
                    labels=test_data["labels"],
                    due_date=test_data["due_date"],
                    priority=test_data["priority"],
                )
            ],
            next_page_token=test_data["output_nextPageToken"],
        )

        # Verify that the issue details matches the expected data
        assert response.issues[0] == expected_output.issues[0]
        assert response.next_page_token == test_data["output_nextPageToken"]

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            "search/jql",
            params={
                "jql": f"project='{test_data["project_name"]}'",
                "maxResults": limit,
                "nextPageToken": test_data["output_nextPageToken"],
                "expand": "versionedRepresentations",
                "fields": "summary,description,attachment,progress,labels,duedate,status,assignee,created,priority",
            },
        )


def test_get_issues_second() -> None:
    """Tests that the issues can be retrieved by the `get_issues` tool."""

    # Define test data
    test_data: dict[str, Any] = {
        "issue_number": "WO-5",
        "summary": "Test1 Task",
        "description": "Test1 Task",
        "author_name": "Agent tool",
        "created_date": "2025-05-30T15:26:28.575+0530",
        "file_name": "",
        "progress_percent": 0,
        "status": "Work in progress",
        "output_nextPageToken": "ChkjU3RyaW5nJlUwTlNWVTA9JUludCZNelU9EAEY8dLjm-QyIhpwcm9qZWN0PSJNeSBTY3J1bSBQcm9qZWN0Ig==",
        "labels": ["Story", "urgent"],
        "due_date": "2025-06-04",
        "priority": "Medium",
        "project_name": "Watson Orchestrate",
    }
    limit = 3

    # Patch `get_jira_client` to return a mock client
    with patch("agent_ready_tools.tools.IT.jira.get_issues.get_jira_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "issues": [
                {
                    "key": test_data["issue_number"],
                    "versionedRepresentations": {
                        "summary": {"1": test_data["summary"]},
                        "description": {
                            "1": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": test_data["description"]}
                                        ],
                                    }
                                ],
                            }
                        },
                        "attachment": {"1": []},
                        "assignee": {"1": {"displayName": test_data["author_name"]}},
                        "created": {"1": test_data["created_date"]},
                        "progress": {"1": {"progress": test_data["progress_percent"], "total": 0}},
                        "status": {"1": {"name": test_data["status"]}},
                        "labels": {"1": test_data["labels"]},
                        "duedate": {"1": test_data["due_date"]},
                        "priority": {"1": {"name": test_data["priority"]}},
                    },
                }
            ],
            "nextPageToken": test_data["output_nextPageToken"],
        }

        # Call the function
        response = get_issues(
            project_name=test_data["project_name"],
            limit=limit,
            next_page_token=test_data["output_nextPageToken"],
        )

        # Expected output
        expected_output = IssuesResponse(
            issues=[
                Issue(
                    summary=test_data["summary"],
                    issue_number=test_data["issue_number"],
                    description=test_data["description"],
                    author_name=test_data["author_name"],
                    created_date=test_data["created_date"],
                    file_name=test_data["file_name"],
                    progress_percent=test_data["progress_percent"],
                    status=test_data["status"],
                    labels=test_data["labels"],
                    due_date=test_data["due_date"],
                    priority=test_data["priority"],
                )
            ],
            next_page_token=test_data["output_nextPageToken"],
        )

        # Verify that the issue details matches the expected data
        assert response.issues[0] == expected_output.issues[0]
        assert response.next_page_token == test_data["output_nextPageToken"]

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            "search/jql",
            params={
                "jql": f"project='{test_data["project_name"]}'",
                "maxResults": limit,
                "nextPageToken": test_data["output_nextPageToken"],
                "expand": "versionedRepresentations",
                "fields": "summary,description,attachment,progress,labels,duedate,status,assignee,created,priority",
            },
        )
