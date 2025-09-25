from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionItem,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_create_item(
    item_number: str,
    item_description: str,
    organization_code: str = "0000",
    item_status: str = "Active",
    lifecycle_phase: str = "Active",
    item_class: str = "Root Item Class",
    primary_uom: str = "Ea",
    customer_order_enabled: str = "true",
    customer_order_flag: str = "true",
) -> ToolResponse[OracleFusionItem]:
    """
    Creates a new item in an Oracle Fusion organization.

    Args:
        item_number: The unique name or number for the item.
        item_description: A description of the item.
        organization_code: The mandatory ID of the organization for this item.
        item_status: The status of the item, e.g., "Active".
        lifecycle_phase: The lifecycle phase of the item, e.g., "Active".
        item_class: "ItemClass": "Root Item Class",
        primary_uom: The primary unit of measure for the item, e.g., "Each".
        customer_order_enabled: Set to 'true'
        customer_order_flag: We set to 'true'

    Returns:
        A ToolResponse object containing the API response or an error message.
    """
    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError) as e:
        return ToolResponse(success=False, message=f"Failure to retrieve credentials: {e}")

    payload_data = {
        "OrganizationCode": organization_code,
        "ItemNumber": item_number,
        "ItemDescription": item_description,
        "ItemStatusValue": item_status,
        "LifecyclePhaseValue": lifecycle_phase,
        "ItemClass": item_class,
        "PrimaryUOMValue": primary_uom,
        "CustomerOrderEnabledFlag": customer_order_enabled,
        "CustomerOrderFlag": customer_order_flag,
    }

    payload = {key: value for key, value in payload_data.items() if value}

    response = client.post_request(
        resource_name="itemsV2",
        payload=payload,
    )

    if "errors" in response or "error" in response:
        error_message = response.get("errors", response.get("error", "Unknown API error"))
        return ToolResponse(success=False, message=str(error_message))

    required_fields = ["ItemId", "OrganizationCode", "ItemNumber", "ItemDescription"]
    for field in required_fields:
        if response.get(field) is None:
            return ToolResponse(
                success=False,
                message=f"API response was successful but missing required field: '{field}'.",
            )

    output_item = OracleFusionItem(
        organization_code=response["OrganizationCode"],
        item_id=response["ItemId"],
        item_number=response["ItemNumber"],
        item_description=response["ItemDescription"],
        item_status=response["ItemStatusValue"],
        lifecycle_phase=response["LifecyclePhaseValue"],
        item_class=response["ItemClass"],
        primary_uom_value=response["PrimaryUOMValue"],
    )

    return ToolResponse(
        success=True,
        message=f"Successfully created item '{output_item.item_number}'.",
        content=output_item,
    )
