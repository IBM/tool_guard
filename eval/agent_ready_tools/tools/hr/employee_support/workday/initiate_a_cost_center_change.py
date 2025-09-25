from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class InitiateCostCenterResult:
    """Represents the result of an InitiateCostCenterChange operation in Workday HCM."""

    cost_center_id: str
    descriptor: str
    status: str


def cost_center_error(response: dict[str, Any], cost_center_id: str) -> InitiateCostCenterResult:
    """
    Builds an error response for the Workday response.

    Args:
        response: The failed response, contains information about the error.
        cost_center_id: The ID of the cost center to be updated, as specified by the
            `get_cost_center_by_cost_center_category` and `get_cost_center_categories.py` tools.

    Returns:
        InitiateCostCenterResult with Failed status.
    """
    return InitiateCostCenterResult(
        status="Failed",
        cost_center_id=cost_center_id,
        descriptor=response["errors"][0]["error"],
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def initiate_a_cost_center_change(
    cost_center_id: str, effective_date: str, user_id: str
) -> InitiateCostCenterResult:
    """
    Initiates a cost center change in Workday.

    Args:
        cost_center_id: The ID of the cost center to be updated, as specified by the
            `get_cost_center_by_cost_center_category` and `get_cost_center_categories.py` tools.
        effective_date: The effective date of the organization assignment change event in ISO 8601.
        user_id: The ID of the worker for whom the organization assignment change is being created.

    Returns:
        The result from performing the update to the user's cost center.
    """
    client = get_workday_client()

    post_payload = {"date": effective_date}
    post_response = client.post_create_organization_assignment_change(post_payload, user_id)
    if "id" in post_response:
        organization_assignment_change_id = post_response["id"]

        patch_payload = {"costCenter": {"id": cost_center_id}}
        patch_response = client.patch_initiate_a_cost_center_change(
            patch_payload, organization_assignment_change_id
        )

        submit_response = client.post_submit_organization_assignment_change_id(
            payload={}, organization_assignment_change_id=organization_assignment_change_id
        )
        if submit_response["error"]:
            return cost_center_error(submit_response, cost_center_id)
    else:
        return cost_center_error(post_response, cost_center_id)

    return InitiateCostCenterResult(
        status=submit_response["businessProcessParameters"]["overallStatus"],
        cost_center_id=patch_response["costCenter"]["id"],
        descriptor=patch_response["costCenter"]["descriptor"],
    )
