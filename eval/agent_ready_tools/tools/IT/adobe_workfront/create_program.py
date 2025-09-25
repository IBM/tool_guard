from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class CreateProgramResponse:
    """Represents the result of creating a program in Adobe Workfront."""

    program_id: str
    program_name: str
    program_description: Optional[str]
    active_status: Optional[bool]
    object_code: Optional[str]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def create_program(
    portfolio_id: str,
    program_name: str,
    active_status: Optional[bool] = True,
    object_code: Optional[str] = None,
    program_manager: Optional[str] = None,
    group: Optional[str] = None,
    program_description: Optional[str] = None,
) -> CreateProgramResponse:
    """
    Creates a program in Adobe Workfront.

    Args:
        portfolio_id: The id of the portfolio from the Adobe Workfront returned by `list_portfolios`
            tool.
        program_name: The name of the program in the Adobe Workfront.
        active_status: The active status of the program in the Adobe Workfront.
        object_code: The object code for the program in the Adobe Workfront.
        program_manager: The owner of the program in the Adobe Workfront.
        group: The group of the program in the Adobe Workfront.
        program_description: The description of the program in the Adobe Workfront.

    Returns:
        The result of performing the creation of program in Adobe Workfront.
    """

    client = get_adobe_workfront_client()

    if active_status is None:
        active_status = True

    payload: dict[str, Any] = {
        "name": program_name,
        "description": program_description,
        "portfolioID": portfolio_id,
        "objCode": object_code,
        "isActive": active_status,
        "ownerID": program_manager,
        "groupID": group,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="prgm", payload=payload)

    result = response.get("data", {})

    return CreateProgramResponse(
        program_id=result.get("ID", ""),
        program_name=result.get("name", ""),
        object_code=result.get("objCode", ""),
        program_description=result.get("description", ""),
        active_status=result.get("isActive", ""),
    )
