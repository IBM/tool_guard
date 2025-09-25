from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class User:
    """Represents a Microsoft user."""

    id: str
    display_name: str
    mail: str
    job_title: Optional[str] = None


@dataclass
class GetAllUsersResponse:
    """Represents the result of getting all users from Microsoft Graph API."""

    users: list[User]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_all_users() -> GetAllUsersResponse:
    """
    Get all users from Microsoft Graph API.

    Returns:
        List of users.
    """
    client = get_microsoft_client()

    endpoint = "users?$select=id,displayName,jobTitle,mail"
    response = client.get_request(endpoint)

    users: list[User] = []

    for result in response["value"]:
        users.append(
            User(
                id=result.get("id"),
                display_name=result.get("displayName"),
                job_title=result.get("jobTitle"),
                mail=result.get("mail"),
            )
        )

    return GetAllUsersResponse(users=users)
