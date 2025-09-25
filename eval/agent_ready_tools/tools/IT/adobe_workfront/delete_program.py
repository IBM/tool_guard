from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class DeleteProgramResponse:
    """Represents the result of delete operation performed on an program in Adobe Workfront."""

    http_code: int


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def delete_program(program_id: str) -> DeleteProgramResponse:
    """
    Deletes a program in Adobe Workfront.

    Args:
        program_id: The id of the program, returned by the `list_programs` tool.

    Returns:
        The status of the delete operation.
    """

    client = get_adobe_workfront_client()

    response = client.delete_request(entity=f"prgm/{program_id}")
    return DeleteProgramResponse(http_code=response)
