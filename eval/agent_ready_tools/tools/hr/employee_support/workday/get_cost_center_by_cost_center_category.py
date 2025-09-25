from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CostCenter:
    """Represents a cost center in Workday."""

    id: str
    descriptor: str


@dataclass
class CostCenterResponse:
    """Represents the response from getting cost centers by category."""

    costcenters: List[CostCenter]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_cost_center_by_cost_center_category(cost_center_category_id: str) -> CostCenterResponse:
    """
    Gets cost centers by cost center category ID from Workday.

    Args:
        cost_center_category_id: The ID of the cost center category.

    Returns:
        The cost centers associated with the specified category.
    """
    client = get_workday_client()

    url = f"api/staffing/v6/{client.tenant_name}/values/organizationAssignmentChangesGroup/costCenters/{cost_center_category_id}"
    response = client.get_request(url=url)

    cost_centers: List[CostCenter] = []
    for item in response.get("data", []):
        cost_centers.append(
            CostCenter(descriptor=item.get("descriptor", ""), id=item.get("id", ""))
        )

    return CostCenterResponse(costcenters=cost_centers)
