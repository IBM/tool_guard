from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.clients.workday_client import get_workday_client


@dataclass
class JobChangeLocation:
    """Represents a job change location in Workday."""

    descriptor: str
    location_id: str


@dataclass
class JobChangeLocationsResponse:
    """Represents the available job change locations."""

    locations: list[JobChangeLocation]


@dataclass
class JobChangeLocationsCategoryResponse:
    """Represents an available job change locations category."""

    category_id: str


def get_job_change_locations_categories() -> str:
    """
    Gets the job change locations category_id of "All Locations" in Workday.

    Returns:
        The category_id of locations category "All Locations" in  Workday.
    """

    client = get_workday_client(access_level=AccessLevel.MANAGER)
    url = f"api/staffing/v6/{client.tenant_name}/values/jobChangesGroup/locations"
    response = client.get_request(url=url)

    category_id = response["data"][1].get("id", "")
    return category_id


@tool
def get_job_change_locations(category_id: str) -> JobChangeLocationsResponse:
    """
    Gets all configured job change locations from the selected category in Workday.

    Args:
        category_id: Job Change Location category ID

    Returns:
        The available job change locations in the requested category.
    """

    client = get_workday_client(access_level=AccessLevel.MANAGER)

    category_id = get_job_change_locations_categories()
    url = f"api/staffing/v6/{client.tenant_name}/values/jobChangesGroup/locations/{category_id}"
    response = client.get_request(url=url)

    return JobChangeLocationsResponse(
        locations=[
            JobChangeLocation(descriptor=data.get("descriptor", ""), location_id=data.get("id", ""))
            for data in response.get("data", [])
        ]
    )
