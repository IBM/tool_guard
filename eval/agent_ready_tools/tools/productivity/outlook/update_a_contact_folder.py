from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class UpdateContactFolderResponse:
    """Represents the result of updating a contact folder in MS outlook."""

    new_contact_folder_name: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def update_a_contact_folder(
    original_contact_folder_id: str, new_contact_folder_name: str
) -> UpdateContactFolderResponse:
    """
    Update a contact folder in Microsoft outlook.

    Args:
        original_contact_folder_id: The id of the contact folder, returned by the
            `get_contact_folders` tool.
        new_contact_folder_name: The new name of the contact folder

    Returns:
        Confirmation of the contact folder update.
    """
    client = get_microsoft_client()

    payload = {"displayName": new_contact_folder_name}
    entity = f"{client.get_user_resource_path()}/contactFolders/{original_contact_folder_id}"
    response = client.update_request(endpoint=entity, data=payload)
    return UpdateContactFolderResponse(new_contact_folder_name=response.get("displayName", ""))
