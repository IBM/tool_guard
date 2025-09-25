from datetime import datetime
from typing import Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesloft_client import get_salesloft_client
from agent_ready_tools.utils.tool_credentials import SALESLOFT_CONNECTIONS


@dataclass
class CadenceResponse:
    """Dataclass representing cadence response from Salesloft."""

    id: Optional[Union[str, int]]
    name: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    current_state: Optional[str]
    cadence_priority: Optional[
        Union[dict, str, int]
    ]  # TODO: clarify with Sales PM the expected output. Current sandbox data returns a dictionary with no relevant field.
    cadence_people: Optional[Union[str, int]]  # TODO: confirm the definition with Sales PM.

    @staticmethod
    def from_dict(data: dict) -> "CadenceResponse":
        """To extract the value of the individual keys represented in the CadenceResponse class."""
        return CadenceResponse(**data)


def format_datetime(dt_str: Optional[str]) -> Optional[str]:
    """Helper function to make 2023-06-05T08:08:03.288160-04:00 into a readable format."""
    if dt_str is None:
        return None
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%m/%d/%Y %I:%M%p").lower()


def parse_cadence_item(item: dict) -> CadenceResponse:
    """Helper function to extract only the data fields needed and handle None value."""
    return CadenceResponse.from_dict(
        {
            "id": item.get("id", None),
            "name": item.get("name", None),
            "current_state": item.get("current_state", None),
            "cadence_priority": (
                item.get("cadence_priority", {}).get("id") if item.get("cadence_priority") else None
            ),
            "cadence_people": item.get("counts", {}).get("cadence_people", None),
            "created_at": (
                format_datetime(item.get("created_at")) if item.get("created_at") else None
            ),
            "updated_at": (
                format_datetime(item.get("updated_at")) if item.get("updated_at") else None
            ),
        }
    )


@tool(
    expected_credentials=SALESLOFT_CONNECTIONS,
    description="Lists cadences from Salesloft. If an ID is provided, returns a single cadence. Otherwise, returns all cadences.",
)
def salesloft_list_cadence(
    cadence_id: Optional[str] = None,
) -> Optional[list[CadenceResponse]]:
    """
    Retrieves one or multiple cadences from Salesloft. A cadence is a structured sequence of sales
    activities—such as emails, calls, or tasks—designed to guide sales representatives through a
    consistent, repeatable schedule for reaching out to prospects or customers.

    Args:
        cadence_id (Optional[str | int]): The ID of the cadence to retrieve. If not provided, all cadences will be returned.

    Returns:
        A list of one of multiple dict following keys:
            - id (str | int): The ID of the cadence.
            - name (str): The name of the cadence.
            - current_state (str): The current state of the cadence (e.g., "active", "archived").
            - cadence_priority (dict | str | int): The priority level of the cadence.
            - cadence_people (str): The number of individuals assigned to the cadence.
            - created_at (str): The datetime when the cadence was created.
            - updated_at (str): The datetime when the cadence was last updated.
    """

    raw_payload = {"version": "v2", "endpoint": "cadences", "path_parameter": cadence_id}
    payload = {k: v for k, v in raw_payload.items() if v is not None}

    client = get_salesloft_client()

    response = client.get_request(
        version=payload["version"],
        endpoint=payload["endpoint"],
        path_parameter=payload.get("path_parameter"),
    )

    cadences = []

    if "data" in response:
        raw = response["data"]
        if isinstance(raw, dict):  # for a single cadence ID
            cadences.append(parse_cadence_item(raw))
        elif isinstance(raw, list):
            cadences.extend(parse_cadence_item(item) for item in raw)

    return cadences
