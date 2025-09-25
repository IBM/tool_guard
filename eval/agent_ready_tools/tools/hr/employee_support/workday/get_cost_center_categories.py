from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CostCenterCategory:
    """Represents a cost center category in Workday."""

    cost_center_categories_id: str
    cost_center_category_name: str


@dataclass
class CostCenterCategoriesResponse:
    """Represents the response from getting cost center categories in Workday."""

    categories: List[CostCenterCategory]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_cost_center_categories() -> CostCenterCategoriesResponse:
    """
    Gets cost center categories from Workday.

    Returns:
        The cost center categories.
    """
    client = get_workday_client()

    url = f"api/staffing/v6/{client.tenant_name}/values/organizationAssignmentChangesGroup/costCenters/"
    response = client.get_request(url=url)

    categories: List[CostCenterCategory] = []
    for category in response["data"]:
        categories.append(
            CostCenterCategory(
                cost_center_category_name=category.get("descriptor", ""),
                cost_center_categories_id=category.get("id", ""),
            )
        )
    return CostCenterCategoriesResponse(categories=categories)
