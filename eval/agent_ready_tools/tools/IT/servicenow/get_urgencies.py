from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Urgency:
    """Represents the details of a single urgency in ServiceNow."""

    urgency: str
    urgency_value: str


@dataclass
class UrgencyResponse:
    """A list of urgencies in a ServiceNow."""

    urgencies: list[Urgency]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_urgencies() -> UrgencyResponse:
    """
    Retrieves a list of urgencies in Servicenow.

    Returns:
        A list of all the urgency.
    """

    client = get_servicenow_client()
    response = client.get_request(
        entity="sys_choice", params={"name": "task", "element": "urgency"}
    )

    urgency_list = [
        Urgency(urgency=urgency.get("label"), urgency_value=urgency.get("value"))
        for urgency in response.get("result", [])
    ]

    return UrgencyResponse(urgencies=urgency_list)
