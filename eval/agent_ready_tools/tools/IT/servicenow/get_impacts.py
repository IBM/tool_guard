from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Impact:
    """Represents the details of a single impact in ServiceNow."""

    impact: str
    impact_value: str


@dataclass
class ImpactsResponse:
    """A list of impacts in a ServiceNow."""

    impacts: List[Impact]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_impacts() -> ImpactsResponse:
    """
    Retrieves a list of impacts in Servicenow.

    Returns:
        A list of all the impacts.
    """

    client = get_servicenow_client()
    response = client.get_request(entity="sys_choice", params={"name": "task", "element": "impact"})

    impact_list = [
        Impact(impact=impact.get("label"), impact_value=impact.get("value"))
        for impact in response.get("result", [])
    ]

    return ImpactsResponse(impacts=impact_list)
