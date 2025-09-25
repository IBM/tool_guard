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

EXCLUDED_DIMENSION = "Sandboxes"


@tool(expected_credentials=IBM_PA_CONNECTIONS, permission=ToolPermission.READ_ONLY)
def get_dimensions_of_cube(cube_name: str) -> List[str]:
    """
    Gets the list of dimensions for a given cube.

    Args:
        cube_name: The name of the cube whose dimensions are to be retrieved.

    Returns:
        list of dimensions of a given cube.
    """
    client: IBMPlanningAnalyticsClient = get_ibm_pa_client()

    response: Response = client.get_request(
        entity=Entity.CUBE.value, entity_id=cube_name, embedded_entity=Entity.DIMENSION.value
    )
    dimensions: List[str] = []
    if response.status_code == HTTPStatus.OK.value:
        response_body: Dict[str, Any] = response.json()
        dimensions = [dimension.get("Name", "") for dimension in response_body.get("value", [])]
        dimensions.remove(EXCLUDED_DIMENSION)
    return dimensions
