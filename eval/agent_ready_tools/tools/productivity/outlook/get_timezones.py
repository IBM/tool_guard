from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class OutlookTimeZone:
    """Represents a timezone record in Microsoft Outlook."""

    timezone_value: str
    display_name: str


@dataclass
class OutlookTimeZonesResponse:
    """A list of timezones in Microsoft Outlook."""

    timezones: List[OutlookTimeZone]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_timezones() -> OutlookTimeZonesResponse:
    """
    Gets a list of timezone details in Microsoft Outlook.

    Returns:
        A list of timezone details.
    """
    client = get_microsoft_client()
    response = client.get_request(
        endpoint=f"{client.get_user_resource_path()}/outlook/supportedTimeZones"
    )
    timezone_list = [
        OutlookTimeZone(
            timezone_value=item.get("alias", ""), display_name=item.get("displayName", "")
        )
        for item in response.get("value", [])
    ]
    return OutlookTimeZonesResponse(timezones=timezone_list)
