from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_issues import AdobeIssue, list_issues


def test_list_issues() -> None:
    """Verify that the `list_issues` tool can successfully retrieve Adobe Workfront issues."""

    # Define test data:
    test_data: dict[str, Any] = {
        "issue_id": "6436c507000e5d7bdbe80ce054be17f0",
        "issue_name": "Circular task dependency",
        "percent_complete": 100,
        "planned_completion_date": "2023-04-17T10:49:00:000-0400",
        "assigned_to": "679cd07f00010fee7b8927d7dfea3321",
        "creation_date": "2025-08-13",
        "is_complete": False,
        "priority": "High",
        "project_id": "65e3932e0f14e63c1ce98215514ad0a7",
        "reference_number": "2828602",
        "issue_status": "Complete",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_issues.get_adobe_workfront_client"
    ) as mock_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workfront_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["issue_id"],
                    "name": test_data["issue_name"],
                    "percentComplete": test_data["percent_complete"],
                    "plannedCompletionDate": test_data["planned_completion_date"],
                    "status": test_data["issue_status"],
                }
            ]
        }

        # Get Adobe Workfront issues
        response = list_issues(issue_name=test_data["issue_name"]).issues[0]

        # Ensure that list_issues() has executed and returned proper values
        expected_data = AdobeIssue(
            issue_id=str(test_data["issue_id"]),
            issue_name=str(test_data["issue_name"]),
            percent_complete=int(test_data["percent_complete"]),
            planned_completion_date=str(test_data["planned_completion_date"]),
            issue_status=str(test_data["issue_status"]),
        )

        assert response
        assert response == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="optask/search",
            params={"name": test_data["issue_name"], "$$LIMIT": 50},
        )
