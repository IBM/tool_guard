from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    AssetStatus,
    PickListOptionsPair,
)


@tool
def list_asset_statuses() -> List[AssetStatus]:
    """
    Retrieves a list of asset status values in Salesforce.

    Returns:
        List of asset status values are returned.
    """
    client = get_salesforce_client()
    response = client.get_picklist_options(
        PickListOptionsPair.AssetStatus.obj_api_name, PickListOptionsPair.AssetStatus.field_api_name
    )

    asset_status_list = [
        AssetStatus(asset_status=value.get("value")) for value in response.get("values", [])
    ]

    return asset_status_list
