from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class TimeZones:
    """Represents a time zone record in ServiceNow."""

    time_zone_label: str


@dataclass
class TimeZonesResponse:
    """Represents the response containing the time zone records."""

    timezones: List[TimeZones]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_time_zones(time_zone_label: Optional[str] = None) -> TimeZonesResponse:
    """
    Retrieves a list of time zone records.

    Args:
        time_zone_label: The label of the time zone record.

    Returns:
        A list of time zone records.
    """
    params = {"name": "sys_user", "element": "time_zone", "inactive": "false"}
    if time_zone_label:
        params["label"] = time_zone_label

    client = get_servicenow_client()
    response = client.get_request(
        entity="sys_choice",
        params=params,
    )

    timezones_list = [
        TimeZones(time_zone_label=item.get("label", "")) for item in response.get("result", [])
    ]

    return TimeZonesResponse(timezones=timezones_list)
