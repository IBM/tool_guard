from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdateProgramResponse:
    """Represents the response for updating a program in Adobe Workfront."""

    program_name: str
    is_active: bool
    description: Optional[str]


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def update_program(
    program_id: str,
    program_name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = True,
    owner_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
) -> UpdateProgramResponse:
    """
    Updates a program in Adobe Workfront.

    Args:
        program_id: The id of the program in Adobe Workfront, returned by the `list_programs` tool.
        program_name: The name of the program in Adobe Workfront.
        description: The description of the program in Adobe Workfront.
        is_active: The status of the program in Adobe Workfront.
        owner_id: The id of the owner of the program in Adobe Workfront, returned by the
            `list_users` tool.
        portfolio_id: The id of the portfolio of the program in Adobe Workfront, returned by the
            `list_portfolios` tool.

    Returns:
        The result of performing an update operation on a program.
    """

    client = get_adobe_workfront_client()

    payload = {
        "name": program_name,
        "description": description,
        "isActive": is_active,
        "ownerID": owner_id,
        "portfolioID": portfolio_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.put_request(entity=f"prgm/{program_id}", payload=payload)

    data = response.get("data", {})

    return UpdateProgramResponse(
        program_name=data.get("name", ""),
        description=data.get("description", ""),
        is_active=data.get("isActive"),
    )
