from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def delete_solution(
    solution_id: str,
) -> Any | int:
    """
    Delete a solution in Salesforce.

    Args:
        solution_id: The id of the solution.

    Returns:
        The deleted solution status.
    """
    client = get_salesforce_client()

    status = client.salesforce_object.Solution.delete(solution_id)  # type: ignore[operator]

    return status
