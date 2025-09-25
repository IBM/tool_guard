from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetConfigurationItem:
    """Represents a configuration item in ServiceNow."""

    system_id: str
    configuration_item_name: str


@dataclass
class GetConfigurationItemResponse:
    """A list of configuration items configured in a ServiceNow deployment."""

    configuration_items: list[GetConfigurationItem]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_configuration_item(
    configuration_item_name: Optional[str] = None,
    system_id: Optional[str] = None,
) -> GetConfigurationItemResponse:
    """
    Gets a list of the configuration_items configured in this ServiceNow.

    Args:
        configuration_item_name: The configuration item of the asset within the ServiceNow API for
            retrieving any configuration item.
        system_id: The system_id of the configuration item uniquely identifying them within the
            ServiceNow API for retrieving any configuration item.

    Returns:
        A list of configuration_items.
    """

    configuration_items_list: list[GetConfigurationItem] = []
    client = get_servicenow_client()

    params = {
        "name": configuration_item_name,
        "sys_id": system_id,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="cmdb_ci", params=params)

    for item in response["result"]:
        configuration_items_list.append(
            GetConfigurationItem(
                system_id=item.get("sys_id"),
                configuration_item_name=item.get("name"),
            )
        )

    return GetConfigurationItemResponse(configuration_items=configuration_items_list)
