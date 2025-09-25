from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.ibm_planning_analytics_client import (
    IBMPlanningAnalyticsClient,
    get_ibm_pa_client,
)
from agent_ready_tools.tools.finance.ibm_planning_analytics.common import Entity
from agent_ready_tools.utils.tool_credentials import IBM_PA_CONNECTIONS


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def create_sandbox(sandbox_name: Optional[str] = None) -> bool:
    """
    Creates a sandbox identified by sandbox_name on the model.

    Args:
        sandbox_name: An optional string that refers to the name of sandbox.

    Returns:
        True if the sandbox is created, False otherwise.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()
    if not sandbox_name:
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        sandbox_name = f"ai-sandbox-{timestamp}"
    payload: Dict[str, Any] = {"Name": sandbox_name, "IncludeInSandboxDimension": True}
    response: Dict[str, Any] = client.post_request(entity=Entity.SANDBOX.value, payload=payload)
    return response["status_code"] == HTTPStatus.CREATED.value
