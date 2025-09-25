from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.get_issue_priorities import get_issue_priorities


def test_get_issue_priorities() -> None:
    """Test that the priorities can be retrieved successfully by the `get_issue_priorities` tool."""

    # Define test data for the first record:
    test_data = {
        "name": "Highest",
    }

    # Patch `get_jira_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.jira.get_issue_priorities.get_jira_client"
    ) as mock_jira_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_jira_client.return_value = mock_client
        mock_client.get_request.return_value = [test_data]

        # Get priorities list
        response = get_issue_priorities()

        # Ensure that get_issue_priorities() executed and returned proper values
        assert response
        print(response)
        assert len(response.priorities) == 1
        priority = response.priorities[0]
        assert priority.name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="priority")
