from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class AssetTypes:
    """Represents the asset types in ServiceNow."""

    asset_type_name: str
    label: str


@dataclass
class AssetTypesResponse:
    """A list of asset types in ServiceNow."""

    asset_types: list[AssetTypes]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_asset_types(label: Optional[str] = None) -> AssetTypesResponse:
    """
    Retrieves a list of asset types in Servicenow.

    Args:
        label: The label name of the asset type.

    Returns:
        A list of all the assettypes.
    """

    client = get_servicenow_client()
    params = {
        "sysparm_query": "nameINalm_hardware,alm_consumable,alm_license,alm_facility,ORDERBYDESCsys_created_on",
        "label": label,
    }
    params = {key: value for key, value in params.items() if value}
    # print(params)

    response = client.get_request(entity="sys_db_object", params=params)

    asset_type_list: list[AssetTypes] = [
        AssetTypes(
            asset_type_name=type.get("name", ""),
            label=type.get("label", ""),
        )
        for type in response["result"]
    ]

    return AssetTypesResponse(asset_types=asset_type_list)
