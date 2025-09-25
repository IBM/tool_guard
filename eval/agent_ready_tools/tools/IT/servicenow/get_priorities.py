from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Priority:
    """Represents the details of priority in ServiceNow."""

    priority: str
    priority_value: str


@dataclass
class GetPrioritiesResponse:
    """A list of priority details in a Servicenow deployment."""

    system_choice: list[Priority]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_priorities() -> GetPrioritiesResponse:
    """
    Gets a list of priority details configured in this Servicenow deployment.

    Returns:
        A list of system users.
    """

    client = get_servicenow_client()
    params = {"name": "task", "element": "priority"}
    response = client.get_request(entity="sys_choice", params=params)
    choices = [
        Priority(priority=choice.get("label"), priority_value=choice.get("value"))
        for choice in response["result"]
    ]

    return GetPrioritiesResponse(system_choice=choices)
