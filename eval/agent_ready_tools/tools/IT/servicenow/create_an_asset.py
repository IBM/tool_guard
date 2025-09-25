from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateAnAssetResults:
    """Represents the result of an create an asset operation in ServiceNow."""

    system_id: str
    display_name: str


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_an_asset(
    asset_type: str,
    model_category: str,
    model: str,
    quantity: str,
    asset_tag: Optional[str] = None,
    serial_number: Optional[str] = None,
    configuration_item_system_id: Optional[str] = None,
) -> CreateAnAssetResults:
    """
    Creates an asset in ServiceNow.

    Args:
        asset_type: The asset_type_name of the asset type as returned by `get_asset_types` tool
        model_category: The name of the model category as returned by `get_model_category` tool.
        model: The name of the model as returned by `get_model` tool.
        quantity: The quantity of the assets from servicenow.
        asset_tag: The asset tag of the asset from the servicenow.
        serial_number: The serial_number of the assets from servicenow.
        configuration_item_system_id: The system_id of the configuration item as returned by
            `get_configuration_item` tool.

    Returns:
        The result from performing the create operation for the assets.
    """

    client = get_servicenow_client()

    payload: dict[str, Any] = {
        "sys_class_name": asset_type,
        "model_category": model_category,
        "model": model,
        "asset_tag": asset_tag,
        "quantity": quantity,
        "serial_number": serial_number,
        "ci": configuration_item_system_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="alm_asset", payload=payload)

    result = response.get("result", None)
    return CreateAnAssetResults(
        display_name=result.get("display_name", ""),
        system_id=result.get("sys_id", ""),
    )
