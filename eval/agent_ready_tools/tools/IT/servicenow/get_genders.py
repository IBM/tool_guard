from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GendersList:
    """Represents a gender record in ServiceNow."""

    gender_label: str


@dataclass
class GendersListResponse:
    """Reprersents the response containing the gender records."""

    gender: List[GendersList]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_genders(gender_label: Optional[str] = None) -> GendersListResponse:
    """
    Retrieves a list of gender records.

    Args:
        gender_label: The label of the gender record.

    Returns:
        A list of gender records.
    """
    params = {"name": "sys_user", "element": "gender"}
    if gender_label:
        params["label"] = gender_label

    client = get_servicenow_client()
    response = client.get_request(
        entity="sys_choice",
        params=params,
    )

    gender_list = [
        GendersList(gender_label=item.get("label", "")) for item in response.get("result", [])
    ]

    return GendersListResponse(gender=gender_list)
