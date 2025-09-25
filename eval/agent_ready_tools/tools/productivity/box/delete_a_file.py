from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class DeleteAFileResponse:
    """Represents the response of deleting a file in Box."""

    http_code: int


@tool(expected_credentials=BOX_CONNECTIONS)
def delete_a_file(file_id: str) -> DeleteAFileResponse:
    """
    Deletes a file in Box.

    Args:
        file_id: The id of the file returned by the `get_file_details_by_name` tool.

    Returns:
        Confirmation of the file deletion.
    """

    client = get_box_client()

    entity = f"files/{file_id}"

    response_status_code = client.delete_request(entity=entity)

    return DeleteAFileResponse(http_code=response_status_code)
