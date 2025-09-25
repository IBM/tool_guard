from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionLineDetails,
)
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_helper_functions import (
    oracle_fusion_build_requisition_line_from_response,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_requisition_line_item(
    purchase_requisition_id: str,
    requisition_line_id: str,
    requisition_distribution_id: str,
    quantity: Optional[int] = None,
    deliver_to_location_code: Optional[str] = None,
    destination_type_code: Optional[str] = None,
    requester_email: Optional[str] = None,
    requested_delivery_date: Optional[str] = None,
    billing_quantity: Optional[int] = None,
    budget_date: Optional[str] = None,
) -> ToolResponse[OracleFusionPurchaseRequisitionLineDetails]:
    """
    Updates line item of a purchase requisition in Oracle Fusion.

    Args:
        purchase_requisition_id: The id of the purchase requsition, returned by the tool `oracle_fusion_get_all_purchase_requisitions`.
        requisition_line_id: The id of the specific line item within the requisition, returned by the `oracle_fusion_get_purchase_requisition_by_id` tool.
        requisition_distribution_id: The id of the distribution associated with the line item, returned by the `oracle_fusion_get_purchase_requisition_by_id` tool.
        quantity: Quantity of the item to be updated in the requisition line.
        deliver_to_location_code: Code representing the delivery location for the item, returned by the `oracle_fusion_get_ship_to_locations` tool.
        destination_type_code: Type of destination for the item, such as 'EXPENSE' or 'INVENTORY'.
        requester_email: Email address of the person requesting the item.
        requested_delivery_date: Date by which the item is expected to be delivered in ISO 8601 format.
        billing_quantity: Quantity used for billing purposes.
        budget_date: Date associated with the budget allocation for the requisition in ISO 8601 format..

    Returns:
        Updated line item of a purchase requisition.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {
        "Quantity": quantity,
        "DeliverToLocationCode": deliver_to_location_code,
        "DestinationTypeCode": destination_type_code,
        "RequesterEmail": requester_email,
        "RequestedDeliveryDate": requested_delivery_date,
    }
    payload = {key: value for key, value in payload.items() if value}

    distributions = {
        "RequisitionDistributionId": requisition_distribution_id,
        "Quantity": billing_quantity,
        "BudgetDate": budget_date,
    }
    distributions = {key: value for key, value in distributions.items() if value}

    if distributions:
        payload["distributions"] = [distributions]

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        resource_name=f"purchaseRequisitions/{purchase_requisition_id}/child/lines/{requisition_line_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    update_item_response = oracle_fusion_build_requisition_line_from_response(response)

    return ToolResponse(
        success=True,
        message="Updated the line item of a purchase requisition in Oracle Fusion.",
        content=update_item_response,
    )
