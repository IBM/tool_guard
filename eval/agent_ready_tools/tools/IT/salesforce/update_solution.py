from enum import StrEnum
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class SolutionStatus(StrEnum):
    """Represents the status of solution in Salesforce."""

    DRAFT = "Draft"
    REVIEWED = "Reviewed"
    DUPLICATE = "Duplicate"


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_solution(
    solution_id: str,
    solution_name: Optional[str] = None,
    status: Optional[SolutionStatus] = None,
    solution_details: Optional[str] = None,
    is_public: Optional[bool] = None,
    is_visible_in_public_knowledge_base: Optional[bool] = None,
) -> int:
    """
    Updates a solution in Salesforce.

    Args:
        solution_id: The id of the solution, returned by the `list_solutions` tool.
        solution_name: The name of the solution.
        status: The status of the solution.
        solution_details: The details of the solution.
        is_public: Whether the solution is published.
        is_visible_in_public_knowledge_base: Whether the solution is visible in public knowledge
            base.

    Returns:
        The status of the update operation performed on the solution.
    """
    client = get_salesforce_client()

    data = {
        "SolutionName": solution_name,
        "Status": status,
        "SolutionNote": solution_details,
        "IsPublished": is_public,
        "IsPublishedInPublicKb": is_visible_in_public_knowledge_base,
    }
    data = {key: value for key, value in data.items() if value}
    status_code = client.salesforce_object.Solution.update(solution_id, data)  # type: ignore[operator]
    return status_code
