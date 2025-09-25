from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Programs:
    """Represents a program in Adobe Workfront."""

    program_id: str
    program_name: str
    is_active: bool
    description: Optional[str]


@dataclass
class ListProgramsResponse:
    """Represents the response for retrieving programs in Adobe Workfront."""

    programs: List[Programs]


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def list_programs(
    program_name: Optional[str] = None,
    limit: Optional[int] = 50,
    skip: Optional[int] = 0,
    is_active: Optional[bool] = True,
    portfolio_id: Optional[str] = None,
    creation_date: Optional[str] = None,
    user_id: Optional[str] = None,
) -> ListProgramsResponse:
    """
    Gets a list of programs from Adobe Workfront.

    Args:
        program_name: The name of the program in Adobe Workfront.
        limit: The maximum number of programs to retrieve in a single API call. Defaults to 50. Use
            this to control the size of the result set.
        skip: The number of programs to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.
        is_active: The status of the program. If True, only active programs are retrieved. If False,
            only inactive programs are retrieved.
        portfolio_id: The unique identifier of the portfolio in Adobe Workfront, returned by the `list_portfolios` tool.
        creation_date: The creation date of program in ISO 8601 format (e.g., YYYY-MM-DD).
        user_id: The unique identifier of the users in Adobe Workfront, returned by the `list_users` tool.

    Returns:
        List of programs with their program_id, program_name, description, and isActive status.
    """

    client = get_adobe_workfront_client()

    params = {
        "name": program_name,
        "$$LIMIT": limit,
        "$$FIRST": skip,
        "isActive": is_active,
        "portfolioID": portfolio_id,
        "entryDate": creation_date,
        "ownerID": user_id,
    }
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="prgm/search", params=params)

    programs: List[Programs] = [
        Programs(
            program_id=result.get("ID", ""),
            program_name=result.get("name", ""),
            description=result.get("description", ""),
            is_active=result.get("isActive", True),
        )
        for result in response.get("data", [])
    ]

    return ListProgramsResponse(programs=programs)
