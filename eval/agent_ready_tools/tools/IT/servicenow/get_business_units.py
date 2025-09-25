from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetBusinessUnits:
    """Represents the details of business units in ServiceNow."""

    system_id: str
    business_unit_name: str


@dataclass
class GetBusinessUnitsResponse:
    """A list of business units configured in a ServiceNow deployment."""

    business_units: list[GetBusinessUnits]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_business_units(
    system_id: Optional[str] = None, business_unit_name: Optional[str] = None
) -> GetBusinessUnitsResponse:
    """
    Gets a list of business units configured in this ServiceNow deployment.

    Args:
        system_id: The system ID of the business unit.
        business_unit_name: The name of the business unit.

    Returns:
        A list of business units.
    """

    client = get_servicenow_client()

    params = {
        "system_id": system_id,
        "business_unit_name": business_unit_name,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="business_unit", params=params)
    results = response["result"]
    business_units_list = [
        GetBusinessUnits(system_id=item.get("sys_id", ""), business_unit_name=item.get("name", ""))
        for item in results
    ]

    return GetBusinessUnitsResponse(business_units=business_units_list)
