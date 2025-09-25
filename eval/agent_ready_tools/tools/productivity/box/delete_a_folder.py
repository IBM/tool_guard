from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class DeleteFolderResponse:
    """Represents the response of deleting the folder in Box."""

    http_code: int


@tool(expected_credentials=BOX_CONNECTIONS)
def delete_a_folder(folder_id: str) -> DeleteFolderResponse:
    """
    Deletes a folder in Box.

    Args:
        folder_id: str: The id of the folder returned by the `get_folder_details_by_name` tool.

    Returns:
        Confirmation of the folder deletion.
    """

    client = get_box_client()
    params = {"recursive": True}
    entity = f"folders/{folder_id}"
    response = client.delete_request(entity=entity, params=params)
    return DeleteFolderResponse(http_code=response)
