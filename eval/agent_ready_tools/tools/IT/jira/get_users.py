from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS

_ACCOUNT_TYPE: str = "app"


@dataclass
class JiraUser:
    """Represents a Jira user."""

    account_id: str
    account_type: str
    user_name: str
    user_active: bool
    email_address: str


@dataclass
class GetUsersResponse:
    """Represents the result of getting all users from Jira."""

    users: List[JiraUser]


@tool(expected_credentials=JIRA_CONNECTIONS)
def get_users(
    limit: Optional[int] = 40,
    skip: Optional[int] = 0,
) -> GetUsersResponse:
    """
    Gets all users from Jira.

    Args:
        limit: The maximum number of users to retrieve in a single API call. Defaults to 10. Use
            this to control the size of the result set.
        skip: The number of users to skip for pagination purposes. Use this to retrieve subsequent
            pages of results when handling large datasets.

    Returns:
        List of users.
    """
    client = get_jira_client()

    params = {"maxResults": limit, "startAt": skip}

    # Filter out the parameters that are None/Blank.
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="users/search", params=params)

    users: List[JiraUser] = []

    for result in response:
        if isinstance(result, dict):
            if result.get("accountType", "") != _ACCOUNT_TYPE:
                users.append(
                    JiraUser(
                        account_id=result.get("accountId", ""),
                        account_type=result.get("accountType", ""),
                        user_name=result.get("displayName", ""),
                        user_active=result.get("active", False),
                        email_address=result.get("emailAddress", ""),
                    )
                )

    return GetUsersResponse(users=users)
