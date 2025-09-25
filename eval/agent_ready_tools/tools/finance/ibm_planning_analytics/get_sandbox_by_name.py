from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from requests import Response

from agent_ready_tools.clients.ibm_planning_analytics_client import (
    IBMPlanningAnalyticsClient,
    get_ibm_pa_client,
)
from agent_ready_tools.tools.finance.ibm_planning_analytics.common import Entity
from agent_ready_tools.utils.tool_credentials import IBM_PA_CONNECTIONS


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def get_sandbox_by_name(sandbox_name: str) -> bool:
    """
    Gets the sandbox identified by sandbox_name.

    Args:
        sandbox_name: The name of the sandbox to be retrieved by the tool.

    Returns:
        True if the sandbox exists, False otherwise.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()

    response: Response = client.get_request(entity=Entity.SANDBOX.value, entity_id=sandbox_name)
    return response.ok
