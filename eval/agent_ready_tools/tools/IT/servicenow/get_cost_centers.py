from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CostCenters:
    """Represents a single cost center object in ServiceNow."""

    system_id: str
    cost_center_name: str


@dataclass
class CostCentersResponse:
    """A list of cost centers configured in a ServiceNow deployment."""

    cost_centers: list[CostCenters]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_cost_centers(
    system_id: Optional[str] = None, cost_center_name: Optional[str] = None
) -> CostCentersResponse:
    """
    Gets a list of cost centers configured in this ServiceNow deployment.

    Args:
        system_id: The unique system identifier of a cost center within the ServiceNow API for
            retrieving any department.
        cost_center_name: The name of the cost center within the ServiceNow API.

    Returns:
        A list of cost centers.
    """

    client = get_servicenow_client()

    params = {
        "sys_id": system_id,
        "name": cost_center_name,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="cmn_cost_center", params=params)
    cost_centers_list = [
        CostCenters(system_id=item.get("sys_id", ""), cost_center_name=item.get("name", ""))
        for item in response["result"]
    ]

    return CostCentersResponse(cost_centers=cost_centers_list)
