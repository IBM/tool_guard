from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.get_users import JiraUser, get_users


def test_get_projects_first_item() -> None:
    """Verifies that the `get_users` tool can successfully retrieve users in Jira."""

    # Define test data
    test_data: dict[str, Any] = {
        "account_id": "5dd64082af96bc0efbe55103",
        "account_type": "atlassian",
        "user_name": "System",
        "user_active": True,
        "email_address": "",
    }

    # Inputs and expected pagination values
    limit = 50
    skip = 1

    with patch("agent_ready_tools.tools.IT.jira.get_users.get_jira_client") as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = [
            {
                "accountId": test_data["account_id"],
                "accountType": test_data["account_type"],
                "displayName": test_data["user_name"],
                "active": test_data["user_active"],
                "emailAddress": test_data["email_address"],
            }
        ]
        # Call the function
        response = get_users(limit=limit, skip=skip)

        # Expected response
        expected_response = JiraUser(
            account_id=test_data["account_id"],
            account_type=test_data["account_type"],
            user_name=test_data["user_name"],
            user_active=test_data["user_active"],
            email_address=test_data["email_address"],
        )

        # Assert the expected and actual response
        assert response.users[0] == expected_response

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            entity="users/search", params={"maxResults": limit, "startAt": skip}
        )
