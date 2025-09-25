from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetCategories:
    """Represents the details of the category in ServiceNow."""

    category_name: str
    system_id: str


@dataclass
class GetCategoriesResponse:
    """A list of categories for incidents in ServiceNow."""

    categories: list[GetCategories]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_categories() -> GetCategoriesResponse:
    """
    Retrieves a list of categories in Servicenow.

    Returns:
        A list of all the categories.
    """

    client = get_servicenow_client()
    response = client.get_request(
        entity="sys_choice", params={"name": "incident", "element": "category"}
    )

    category_list: list[GetCategories] = [
        GetCategories(
            category_name=incident.get("label", ""),
            system_id=incident.get("sys_id", ""),
        )
        for incident in response["result"]
    ]

    return GetCategoriesResponse(categories=category_list)
