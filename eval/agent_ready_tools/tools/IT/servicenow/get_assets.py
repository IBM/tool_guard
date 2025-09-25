from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Asset:
    """Represents the details of a single asset in ServiceNow."""

    system_id: str
    quantity: str
    display_name: Optional[str] = None
    serial_number: Optional[str] = None
    assigned_to_user: Optional[str] = None
    asset_tag: Optional[str] = None
    invoice_number: Optional[str] = None
    owned_by: Optional[str] = None
    delivery_date: Optional[str] = None
    purchase_date: Optional[str] = None
    model_category: Optional[str] = None
    model: Optional[str] = None
    comments: Optional[str] = None


@dataclass
class GetAssetsResponse:
    """A list of assets configured in a ServiceNow deployment."""

    assets: list[Asset]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_assets(
    model_name_system_id: Optional[str] = None,
    display_name: Optional[str] = None,
    assigned_to_user: Optional[str] = None,
    serial_number: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> GetAssetsResponse:
    """
    Gets a list of assets configured in this ServiceNow deployment.

    Args:
        model_name_system_id: The system_id of the model as returned by `get_model` tool within the
            ServiceNow API for retrieving any asset.
        display_name: The display_name of the asset within the ServiceNow API for retrieving any
            asset.
        assigned_to_user: The name of the user for whom the asset is assigned to returned by
            `get_system_users` within the ServiceNow API for retrieving any asset.
        serial_number: The serial number of the asset uniquely identifying them within the
            ServiceNow API for retrieving any asset.
        limit: The maximum number of assets to retrieve in a single API call. Defaults to 20. Use
            this to control the size of the result set.
        skip: The number of assets to skip for pagination.

    Returns:
        A list of assets.
    """

    client = get_servicenow_client()

    params = {
        "model": model_name_system_id,
        "display_name": display_name,
        "assigned_to": assigned_to_user,
        "serial_number": serial_number,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
        "sysparm_display_value": True,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="alm_asset", params=params)
    assets = [
        Asset(
            model_category=(
                item.get("model_category", {}).get("display_value")
                if isinstance(item.get("model_category"), dict)
                else item.get("model_category")
            ),
            model=(
                item.get("model", {}).get("display_value")
                if isinstance(item.get("model"), dict)
                else item.get("model")
            ),
            invoice_number=item.get("invoice_number"),
            asset_tag=item.get("asset_tag"),
            owned_by=(
                item.get("owned_by", {}).get("display_value")
                if isinstance(item.get("owned_by"), dict)
                else item.get("owned_by")
            ),
            display_name=item.get("display_name"),
            delivery_date=item.get("delivery_date"),
            purchase_date=item.get("purchase_date"),
            system_id=item.get("sys_id"),
            assigned_to_user=(
                item.get("assigned_to", {}).get("display_value")
                if isinstance(item.get("assigned_to"), dict)
                else item.get("assigned_to")
            ),
            quantity=item.get("quantity"),
            serial_number=item.get("serial_number"),
            comments=item.get("comments"),
        )
        for item in response.get("result", [])
    ]

    return GetAssetsResponse(assets)
