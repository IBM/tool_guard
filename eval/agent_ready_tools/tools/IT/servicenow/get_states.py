from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class State:
    """Represents the result of a state in ServiceNow."""

    state_name: str
    state_code: str


@dataclass
class StatesResponse:
    """A list of states in ServiceNow."""

    states_list: list[State]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_states() -> StatesResponse:
    """
    Retrieves a list of all states for an incident in ServiceNow.

    Returns:
        The result contains all states details of an incident.
    """

    client = get_servicenow_client()
    params = {"name": "task", "element": "state"}
    response = client.get_request(entity="sys_choice", params=params)
    states_list = [
        State(state_name=state.get("label"), state_code=state.get("value"))
        for state in response["result"]
    ]
    return StatesResponse(states_list=states_list)
