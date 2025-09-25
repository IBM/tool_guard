from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class UserLoginName:
    """A user login name for a user in Coupa deployment."""

    login_name: str


@dataclass
class UserLoginNameResponse:
    """A list of user login names for users in Coupa deployment."""

    login_names: list[UserLoginName]


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_user_login_names(
    limit: Optional[int] = 10, offset: Optional[int] = 0
) -> UserLoginNameResponse:
    """
    Gets the list of user login names that are active in the Coupa system.

    Args:
        limit: number of users to be shown at a time
        offset: value for pagination

    Returns:
        A list of user login names.
    """
    client = get_coupa_client(scope=["core.user.read"])

    params = {
        "status": "active",  # only show active users; can't create a requisition with an inactive user
        "limit": limit,
        "offset": offset,
    }

    response = client.get_request(resource_name="users", params=params)

    login_names = UserLoginNameResponse(
        login_names=[UserLoginName(login_name=user["login"]) for user in response]  # type: ignore[index]
    )
    return login_names
