import http
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class CopyFolder:
    """Represents the copying a folder into another folder in Box."""

    folder_name: str
    folder_id: str
    http_code: int


@dataclass
class CopyFolderResponse:
    """Represents the result of copying a folder into another folder in Box."""

    message: str
    folder: Optional[CopyFolder] = None


@tool(expected_credentials=BOX_CONNECTIONS)
def copy_folder(
    source_folder_id: str,
    target_folder_id: str,
) -> CopyFolderResponse:
    """
    Copies a folder into another folder in Box.

    Args:
        source_folder_id: The id of the folder to be copied, as returned by the
            `get_folder_details_by_name` tool.
        target_folder_id: The id of the target folder where the copied folder will be pasted, as
            returned by the `get_folder_details_by_name` tool.

    Returns:
        The result from performing the copy operation.
    """
    client = get_box_client()

    payload = {"parent": {"id": target_folder_id}}
    entity = f"folders/{source_folder_id}/copy"
    response = client.post_request(entity=entity, data=payload)

    if (
        "status" in response and response.get("status") == http.HTTPStatus.CONFLICT.value
    ):  # If the folder with the given name is already exist, it will return the message.
        message = response.get("message", "")
        return CopyFolderResponse(message=message)

    folder = CopyFolder(
        folder_name=response.get("name", ""),
        folder_id=response.get("id", ""),
        http_code=response.get("status_code", ""),
    )
    return CopyFolderResponse(folder=folder, message="Folder copied successfully.")
