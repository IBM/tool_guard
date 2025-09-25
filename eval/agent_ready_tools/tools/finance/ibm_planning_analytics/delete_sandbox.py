from http import HTTPStatus

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.ibm_planning_analytics_client import (
    IBMPlanningAnalyticsClient,
    get_ibm_pa_client,
)
from agent_ready_tools.tools.finance.ibm_planning_analytics.common import Entity
from agent_ready_tools.utils.tool_credentials import IBM_PA_CONNECTIONS


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def delete_sandbox(sandbox_name: str) -> bool:
    """
    Deletes a sandbox identified by sandbox_name on the model.

    Args:
        sandbox_name: An optional string that refers to the name of sandbox.

    Returns:
        No content if the sandbox is deleted successfully.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()
    response_status_code: int = client.delete_request(
        entity=Entity.SANDBOX.value, entity_id=sandbox_name
    )
    return response_status_code == HTTPStatus.NO_CONTENT.value
