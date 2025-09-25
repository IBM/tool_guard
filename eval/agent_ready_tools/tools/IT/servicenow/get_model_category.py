from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetModelCategory:
    """Represents the details of a single model category of the asset in ServiceNow."""

    name: str
    system_id: str


@dataclass
class GetModelCategoryResponse:
    """A list of model categories of the assets configured in a ServiceNow deployment."""

    categories: list[GetModelCategory]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_model_category(
    name: Optional[str] = None,
    system_id: Optional[str] = None,
) -> GetModelCategoryResponse:
    """
    Gets a list of model categories of the assets configured in this ServiceNow deployment.

    Args:
        name: The name of the model category within the ServiceNow API for retrieving any model.
        system_id: The system_id of the model category uniquely identifying them within the
            ServiceNow API for retrieving any model category.

    Returns:
        A list of model categories.
    """

    client = get_servicenow_client()

    params = {"name": name, "system_id": system_id}

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="cmdb_model_category", params=params)

    categories_list: list[GetModelCategory] = []
    for item in response["result"]:
        categories_list.append(
            GetModelCategory(name=item.get("name"), system_id=item.get("sys_id"))
        )

    return GetModelCategoryResponse(categories=categories_list)
