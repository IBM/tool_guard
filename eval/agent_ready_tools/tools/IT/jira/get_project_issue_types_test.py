from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.get_project_issue_types import get_project_issue_types


def test_get_project_issue_types() -> None:
    """Verifies that the `get_project_issue_types` tool can successfully retrieve project issue
    types from Jira."""

    # Define test data
    test_data = {"project_id": "10001", "issuetype_id": "10007", "issuetype": "Bug"}

    # Patch `get_jira_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.jira.get_project_issue_types.get_jira_client"
    ) as mock_jira_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_jira_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "issueTypes": [
                {
                    "id": test_data["issuetype_id"],
                    "name": test_data["issuetype"],
                }
            ],
        }

        # Retrieve project issue types
        response = get_project_issue_types(test_data["project_id"])

        # Ensure that get_project_issue_types() has executed and returned proper values
        assert response
        assert len(response.project_issue_types)
        assert response.project_issue_types[0].issuetype_id == test_data["issuetype_id"]
        assert response.project_issue_types[0].issuetype == test_data["issuetype"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"issue/createmeta/{test_data['project_id']}/issuetypes"
        )
