from typing import List, Optional, Tuple

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.slack_client import SlackClient, get_slack_client
from agent_ready_tools.utils.tool_credentials import SLACK_CONNECTIONS


@dataclass
class SlackUser:
    """Represents a Slack user."""

    id: str
    name: str
    team_id: Optional[str]
    email: Optional[str]


@dataclass
class GetAllSlackUsersResponse:
    """Represents the response from fetching all Slack users."""

    users: List[SlackUser]
    http_code: int


def _fetch_users(
    client: SlackClient, users: List[SlackUser], cursor: str = ""
) -> Tuple[List[SlackUser], int]:
    """
    Helper function to recursively fetch all users from Slack.

    Args:
        client: The Slack client
        users: List of users accumulated so far
        cursor: Pagination cursor

    Returns:
        Tuple of (list of users, http code)
    """
    params = {}
    if cursor:
        params["cursor"] = cursor

    response = client.get_request(entity="users.list", params=params)

    if not response.get("ok", False):
        return users, 400

    for user in response.get("members", []):
        profile = user.get("profile", {})
        users.append(
            SlackUser(
                id=user.get("id", ""),
                name=user.get("name", ""),
                team_id=user.get("team_id", ""),
                email=profile.get("email"),
            )
        )

    response_metadata = response.get("response_metadata", {})
    next_cursor = response_metadata.get("next_cursor", "")

    if next_cursor:
        return _fetch_users(client, users, next_cursor)

    return users, 200


@tool(expected_credentials=SLACK_CONNECTIONS)
def get_all_slack_users() -> GetAllSlackUsersResponse:
    """
    Retrieves all users from a Slack workspace.

    The function handles pagination automatically and fetches all users across multiple API calls.

    Returns:
        A complete list of all users in the Slack workspace.
    """
    client = get_slack_client()

    all_users, http_code = _fetch_users(client, [], "")

    return GetAllSlackUsersResponse(
        users=all_users,
        http_code=http_code,
    )
