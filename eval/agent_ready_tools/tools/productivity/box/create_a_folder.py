import http
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class Folder:
    """Represents a folder in Box."""

    type: str
    id: str
    name: str


@dataclass
class CreateFolderResponse:
    """Response object for folder creation."""

    message: str
    folder: Optional[Folder] = None


@tool(expected_credentials=BOX_CONNECTIONS)
def create_a_folder(folder_name: str, parent_folder_id: str = "0") -> CreateFolderResponse:
    """
    Creates a new folder in Box.

    Args:
        folder_name: The name of the folder to be created.
        parent_folder_id: The ID of the parent folder returned by the `get_folder_details_by_name`
            tool in which the new folder will be created. Default is "0" (root folder).

    Returns:
        The response containing details of the created folder.
    """

    client = get_box_client()

    data = {"name": folder_name, "parent": {"id": parent_folder_id}}  # change payload to data

    response = client.post_request(entity="folders", data=data)  # change payload to data

    if (
        "status" in response and response.get("status") == http.HTTPStatus.CONFLICT.value
    ):  # If the folder with the given name is already exist, it will return the message.
        message = response.get("message", "")
        return CreateFolderResponse(message=message)

    folder = Folder(
        type=response.get("type", ""), id=response.get("id", ""), name=response.get("name", "")
    )

    return CreateFolderResponse(folder=folder, message="Folder created successfully.")
