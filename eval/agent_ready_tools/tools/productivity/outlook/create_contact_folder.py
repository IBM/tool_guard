from typing import Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateContactFolderResponse:
    """Represents the result of creating an Outlook contact folder."""

    folder_id: Optional[Union[int, str]] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_contact_folder(
    display_name: str,
) -> CreateContactFolderResponse:
    """
    Creates an Outlook contact folder.

    Args:
        display_name: The display name of the contact folder.

    Returns:
        ID of created contact folder or error details
    """
    client = get_microsoft_client()

    payload = {
        "displayName": display_name,
    }

    try:
        response = client.post_request(
            endpoint=f"{client.get_user_resource_path()}/contactFolders", data=payload
        )
        return CreateContactFolderResponse(folder_id=response["id"])
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", {}).get("code", "")
        error_description = error_response.get("error", {}).get("message", "")
        return CreateContactFolderResponse(
            error_message=error_message,
            error_description=error_description,
        )
    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return CreateContactFolderResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
