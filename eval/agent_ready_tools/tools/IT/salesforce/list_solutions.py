from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Solution
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class SolutionsResponse:
    """Represents the response containing all the solution."""

    solutions: List[Solution]


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_solutions(
    search: Optional[str] = None,
) -> SolutionsResponse:
    """
    List all solutions from Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of solution from Salesforce.
    """
    client = get_salesforce_client()

    cleaned_clause = format_where_input_string(search or "")

    response = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, SolutionName, SolutionNumber,Status,SolutionNote FROM Solution {cleaned_clause}"
        )
    )

    solution_list = [
        Solution(
            id=obj.get("Id", ""),
            name=obj.get("SolutionName", ""),
            status=obj.get("Status", ""),
            description=obj.get("SolutionNote", ""),
            number=obj.get("SolutionNumber", ""),
        )
        for obj in response
    ]
    return SolutionsResponse(solutions=solution_list)
