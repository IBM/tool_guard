from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Solution
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def create_solution(
    name: str,
    status: str,
    description: str,
) -> Solution:
    """
    Create a new solution in Salesforce.

    Args:
        name: The name of the solution.
        status: The status of the solution.
        description: The description of the solution.

    Returns:
        The created solution object.
    """
    client = get_salesforce_client()

    data = {
        "SolutionName": name,
        "Status": status,
        "SolutionNote": description,
    }

    o = client.salesforce_object.Solution.create(data)  # type: ignore[operator]

    return Solution(id=o.get("id"), name=name, status=status, description=description)
