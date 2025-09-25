from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class DeleteProjectResponse:
    """Represents the result of delete operation performed on a project in Adobe Workfront."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def delete_project(project_id: str) -> DeleteProjectResponse:
    """
    Deletes a project in Adobe Workfront.

    Args:
        project_id: The id of the project, returned by the `list_projects` tool.

    Returns:
        The status of the delete operation.
    """

    client = get_adobe_workfront_client()

    response = client.delete_request(entity=f"proj/{project_id}")
    return DeleteProjectResponse(http_code=response)
