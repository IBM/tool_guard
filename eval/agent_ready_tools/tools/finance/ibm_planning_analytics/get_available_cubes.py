from http import HTTPStatus
from typing import Any, Dict, List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from requests import Response

from agent_ready_tools.clients.ibm_planning_analytics_client import (
    IBMPlanningAnalyticsClient,
    get_ibm_pa_client,
)
from agent_ready_tools.tools.finance.ibm_planning_analytics.common import Entity
from agent_ready_tools.utils.tool_credentials import IBM_PA_CONNECTIONS


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def get_available_cubes() -> List[str]:
    """
    Gets a list of available cube names against the configured database (model).

    Returns:
        the list of cube names available in the database.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()

    response: Response = client.get_request(entity=Entity.CUBE.value)
    cube_names: List[str] = []
    if response.status_code == HTTPStatus.OK.value:
        response_body: Dict[str, Any] = response.json()
        cubes_list: List[Any] = response_body.get("value", [])
        cube_names = [cube.get("Name", "") for cube in cubes_list]
    return cube_names
