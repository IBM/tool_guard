from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
import requests

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import validate_role_enum_value
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CreateUserResponse:
    """Represents the result for user creation in Zendesk."""

    user_id: str
    name: str
    email: str
    role: Optional[str] = None
    error_message: Optional[str] = None


@tool(
    permission=ToolPermission.READ_WRITE,
    expected_credentials=ZENDESK_CONNECTIONS,
)
def zendesk_create_user(name: str, email: str, role: Optional[str] = None) -> CreateUserResponse:
    """
    Creates a new user in Zendesk with the given name, email, and optional role.

    Args:
        name: Full name of the user.
        email: Email id of the user.
        role: Role of the user (optional, defaults to empty string).

    Returns:
        An object with the created user's details or error message.
    """
    client = get_zendesk_client()

    try:
        validated_role = validate_role_enum_value(role)
    except ValueError as ve:
        return CreateUserResponse(
            user_id="", name=name, email=email, role=role, error_message=str(ve)
        )

    payload = {"user": {"name": name, "email": email, "role": validated_role}}

    try:
        response = client.post_request(entity="users", payload=payload)
        data = response.get("user", {})
        return CreateUserResponse(
            user_id=str(data.get("id", "")),
            name=data.get("name", ""),
            email=data.get("email", ""),
            role=data.get("role", ""),
            error_message=None,
        )

    except requests.exceptions.HTTPError as http_err:
        error_msg = "HTTP error occurred while creating user"
        if http_err.response is not None and http_err.response.status_code == 422:
            error_detail = http_err.response.json()
            email_errors = error_detail.get("details", {}).get("email", [])
            for err in email_errors:
                if err.get("error") == "DuplicateValue":
                    error_msg = "User creation failed: Email is already being used by another user."
                    break
        return CreateUserResponse(
            user_id="", name=name, email=email, role=role, error_message=error_msg
        )

    except Exception as e:  # pylint: disable=broad-except
        return CreateUserResponse(
            user_id="", name=name, email=email, role=role, error_message=str(e)
        )
