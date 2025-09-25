from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeUser:
    """Represents a User in Adobe Workfront."""

    user_id: str
    user_name: str
    email: str
    title: Optional[str]
    phone_number: Optional[str]
    access_level_id: Optional[str]
    access_level_name: Optional[str]


@dataclass
class ListUsersResponse:
    """Represents list of users in Adobe Workfront."""

    users: List[AdobeUser]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def adobe_list_users(
    user_name: Optional[str] = None,
    email: Optional[str] = None,
    limit: Optional[int] = 50,
    skip: Optional[int] = 0,
) -> ListUsersResponse:
    """
    Retrieves a list of users from Adobe Workfront.

    Args:
        user_name: The name of the user in Adobe Workfront.
        email: The email address of the user in Adobe Workfront.
        limit: The maximum number of users to return. Default is 50.
        skip: The number of users to skip (for pagination). Default is 0.

    Returns:
        List of users in Adobe Workfront.
    """

    client = get_adobe_workfront_client()

    fields = "title,emailAddr,phoneNumber,accessLevel"

    params = {
        "name": user_name,
        "emailAddr": email,
        "fields": fields,
        "$$LIMIT": limit,
        "$$FIRST": skip,
    }
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="user/search", params=params)

    users: List[AdobeUser] = [
        AdobeUser(
            user_id=result.get("ID", ""),
            user_name=result.get("name", ""),
            title=result.get("title", ""),
            email=result.get("emailAddr", ""),
            phone_number=result.get("phoneNumber", ""),
            access_level_id=(
                result.get("accessLevel", {}).get("ID", "") if result.get("accessLevel") else None
            ),
            access_level_name=(
                result.get("accessLevel", {}).get("name", "") if result.get("accessLevel") else None
            ),
        )
        for result in response.get("data", [])
    ]

    return ListUsersResponse(users=users)
