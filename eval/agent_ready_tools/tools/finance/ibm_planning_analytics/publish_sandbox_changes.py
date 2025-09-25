from http import HTTPStatus
from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.ibm_planning_analytics_client import (
    IBMPlanningAnalyticsClient,
    get_ibm_pa_client,
)
from agent_ready_tools.tools.finance.ibm_planning_analytics.common import Entity
from agent_ready_tools.utils.tool_credentials import IBM_PA_CONNECTIONS


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def publish_sandbox(sandbox_name: str) -> bool:
    """
    Publishes the sandbox changes back to the base.

    Args:
        sandbox_name: A string that refers to the name of sandbox.

    Returns:
        True if the sandbox changes were published, False otherwise.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()
    response: Dict[str, Any] = client.post_request(
        entity=Entity.SANDBOX.value, entity_id=sandbox_name, action="tm1.Publish", payload={}
    )
    return response["status_code"] == HTTPStatus.NO_CONTENT.value
