from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateMailFolderResponse:
    """Represents the HTTP status code result of creating a mail folder in Microsoft Outlook."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_mail_folder(
    display_name: str,
    is_hidden: Optional[bool] = False,
) -> CreateMailFolderResponse:
    """
    Creates a new mail folder in Microsoft Outlook.

    Args:
        display_name: The display name of the new mail folder.
        is_hidden: Boolean flag indicating if the folder should be hidden.

    Returns:
        HTTP status code of the create mail folder operation.
    """
    client = get_microsoft_client()

    payload = {"displayName": display_name, "isHidden": is_hidden}

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/mailFolders", data=payload
    )

    return CreateMailFolderResponse(http_code=response.get("status_code", ""))
