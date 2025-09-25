from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DueIn:
    """Represents a due-in in ServiceNow."""

    due_in: str
    due_in_value: str


@dataclass
class DueInResponse:
    """A response containing the list of due-in."""

    due_in_list: list[DueIn]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_due_in(due_in: Optional[str] = None, due_in_value: Optional[str] = None) -> DueInResponse:
    """
    Gets a list of due-in records.

    Args:
        due_in: The name of the due-in.
        due_in_value: The value of the due-in.

    Returns:
        A list of due-in records.
    """

    client = get_servicenow_client()

    params: dict[str, Any] = {
        "name": "alm_asset",
        "element": "due_in",
        "label": due_in,
        "value": due_in_value,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="sys_choice", params=params)

    due_in_response: list[DueIn] = [
        DueIn(
            due_in=status.get("label", ""),
            due_in_value=status.get("value", ""),
        )
        for status in response["result"]
    ]

    return DueInResponse(due_in_list=due_in_response)
