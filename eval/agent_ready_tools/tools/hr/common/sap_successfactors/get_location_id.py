from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class LocationOption:
    """Dataclass containing location name and external_code."""

    location: str
    location_id: str


@dataclass
class GetLocationIdResponse:
    """A list of matching locations with their names and external codes."""

    locations: List[LocationOption]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_location_id(
    location_query: Optional[str] = None, company: Optional[str] = None
) -> GetLocationIdResponse:
    """
    Searches for the location in the company's location list.

    Args:
        location_query: The location name to search for in the company's location options.
        company: The company identifier to filter the location search.

    Returns:
        A list of matching location options.
    """
    client = get_sap_successfactors_client()

    filters = ["status eq 'A'"]

    if location_query:
        filters.append(f"name eq '{location_query}'")
    if company:
        filters.append(f"companyFlxNav/externalCode eq '{company}'")

    filter_query = " and ".join(filters)

    response = client.get_request(
        entity="FOLocation",
        filter_expr=filter_query,
        select_expr="externalCode,name",
    )
    results = response.get("d", {}).get("results", [])
    options = [
        LocationOption(location=loc.get("name"), location_id=loc.get("externalCode"))
        for loc in results
    ]
    return GetLocationIdResponse(locations=options)
