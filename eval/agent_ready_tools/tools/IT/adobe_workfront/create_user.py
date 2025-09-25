from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class CreateUserResponse:
    """Represents the result for user creation in Adobe Workfront."""

    user_id: str
    name: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def create_user(
    first_name: str,
    last_name: str,
    email_address: str,
    access_level_id: str,
    phone_number: Optional[str] = None,
    title: Optional[str] = None,
    my_info: Optional[str] = None,
) -> CreateUserResponse:
    """
    Creates a user in Adobe Workfront.

    Args:
        first_name: The first name of the user.
        last_name: The last name of the user.
        email_address: The email_address of the user.
        access_level_id: The id of the access_level, returned by the `list_access_levels` tool.
        phone_number: The phone number of the user.
        title: The title of the user.
        my_info: The info of the user.

    Returns:
        The result of creating a user.
    """

    client = get_adobe_workfront_client()

    payload: dict[str, Any] = {
        "firstName": first_name,
        "lastName": last_name,
        "emailAddr": email_address,
        "accessLevelID": access_level_id,
        "phoneNumber": phone_number,
        "title": title,
        "myInfo": my_info,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="user", payload=payload)
    data = response.get("data", {})
    return CreateUserResponse(user_id=data.get("ID", ""), name=data.get("name", ""))
