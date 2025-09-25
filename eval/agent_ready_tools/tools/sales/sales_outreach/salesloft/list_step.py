from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.salesloft_client import get_salesloft_client
from agent_ready_tools.tools.sales.sales_outreach.salesloft.dataclasses import (
    SalesloftErrorResponse,
    StepResponse,
)
from agent_ready_tools.tools.sales.sales_outreach.salesloft.utils import format_datetime
from agent_ready_tools.utils.tool_credentials import SALESLOFT_CONNECTIONS


def parse_step_item(
    item: dict,
) -> (
    StepResponse
):  # TODO: Make this function for dynamic to handle various formats. Need to confirm the needs and use cases with PM.
    """Extracts the required fields from a step fields dictionary and handle None values
    gracefully."""
    step_fields = {
        "id": item.get("id"),
        "name": item.get("name"),
        "display_name": item.get("display_name"),
        "type": item.get("type"),
        "day": item.get("day"),
        "step_number": item.get("step_number"),
        "created_at": (format_datetime(item.get("created_at")) if item.get("created_at") else None),
        "updated_at": (format_datetime(item.get("updated_at")) if item.get("updated_at") else None),
        "details": item.get("details", {}).get("_href"),
        "cadence_id": item.get("cadence", {}).get("id"),
    }

    return StepResponse(**step_fields)


@tool(
    expected_credentials=SALESLOFT_CONNECTIONS,
    description="Lists steps from Salesloft. If an ID is provided, returns a single step. Otherwise, returns all steps.",
)
def salesloft_list_step(
    step_id: Optional[str] = None,
) -> Optional[List[StepResponse]] | SalesloftErrorResponse:
    """
    Retrieves one or more steps from Salesloft. A step is a specific action—such as sending an
    email, making a call, or performing another engagement activity—within a sales cadence. A
    cadence is a structured sequence of these steps, designed to guide salespeople through a
    consistent and systematic outreach process.

    Args:
        step_id (Optional[str | int]): The ID of the step to retrieve. If not provided, all steps will be returned.

    Returns:
        A list of one of multiple dict following keys:
            - id (str | int): The ID of the step.
            - name (str): The name of the step.
            - display_name (str): The display_name of the step.
            - type (str): The type of the action scheduled by this step. Valid types are: email, phone, integration, other. #TODO make this into enum
            - day (int): Day this step is associated with up.
            - step_number (int): The number of the step for this day.
            - created_at (str): The datetime when the step was created.
            - updated_at (str): The datetime when the step was last updated.
            - details (str): The URL link to the details of the step.
            - cadence_id (str | int): The ID of the cadence the step is associated with
    """
    client = get_salesloft_client()

    response = client.get_request(
        version="v2",
        endpoint="steps",
        path_parameter=step_id,
    )

    if "error" in response:
        return SalesloftErrorResponse(message=response.get("error"))

    steps = []
    if "data" in response:
        raw = response["data"]
        if isinstance(raw, dict):  # for a single cadence ID
            steps.append(parse_step_item(raw))
        elif isinstance(raw, list):
            steps.extend(parse_step_item(item) for item in raw)

    return steps
