from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateAssetResult:
    """Represents the result of an asset update operation in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_an_asset(
    system_id: str,
    assigned_to_user_system_id: Optional[str] = None,
    cost: Optional[str] = None,
    quantity: Optional[str] = None,
    due_in: Optional[str] = None,
    disposal_reason: Optional[str] = None,
    install_status: Optional[str] = None,
    purchase_date: Optional[str] = None,
) -> UpdateAssetResult:
    """
    Updates an asset in ServiceNow.

    Args:
        system_id: The system_id of the asset returned by the `get_assets` tool.
        assigned_to_user_system_id: The system_id of the user for whom the asset is assigned to as
            returned by `get_system_users` tool.
        cost: The cost of the asset.
        quantity: The quantity of the asset.
        due_in: The due_in_value field returned from the `get_due_in` tool.
        disposal_reason: The reason for the asset disposal.
        install_status: The install_status of the asset returned from the `get_install_status` tool.
        purchase_date: The purchase date of the asset in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The result from performing the update an asset operation.
    """
    client = get_servicenow_client()

    payload: dict[str, Any] = {
        "assigned_to": assigned_to_user_system_id,
        "cost": cost,
        "quantity": quantity,
        "due_in": due_in,
        "disposal_reason": disposal_reason,
        "install_status": install_status,
        "purchase_date": purchase_date,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(entity="alm_asset", entity_id=system_id, payload=payload)

    return UpdateAssetResult(http_code=response.get("status_code", ""))
