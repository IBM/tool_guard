from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sterling_oms_client import get_sterling_oms_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.supply_chain.ibm_sterling_oms.order_management.common_dataclasses import (
    OMSOrderHeader,
    OrderDocumentType,
)
from agent_ready_tools.utils.tool_credentials import STERLING_OMS_CONNECTIONS


@tool(expected_credentials=STERLING_OMS_CONNECTIONS)
def sterling_oms_get_orders(
    enterprise_code: Optional[str] = None,
    order_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 10,
) -> ToolResponse[list[OMSOrderHeader]]:
    """
    Retrieves a list of orders.

    Args:
        enterprise_code: The unique ID of the enterprise to which the orders belong to
        order_type: the type of order based on enum values
        from_date: from date
        to_date: to date
        status: order status
        limit: int = 10

    Returns:
        The retrieved orders.
    """
    try:
        validated_order_type = OrderDocumentType.validate_document_type(order_type)
    except ValueError as e:
        return ToolResponse(success=False, message=str(e))
    try:
        client = get_sterling_oms_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        k: v
        for k, v in {
            "EnterpriseCode": enterprise_code,
            "DocumentType": validated_order_type,
            "FromOrderDate": from_date,
            "ToOrderDate": to_date,
            "Status": status,
            "MaximumRecords": str(limit),
        }.items()
        if v not in (None, "", "null")
    }

    response = client.get_request(resource_name="order", params=params)
    if "errorMessage" in response:
        return ToolResponse(success=False, message=response["errorMessage"])

    assert isinstance(response, list)

    if len(response) == 0:
        return ToolResponse(success=False, message="No orders were found")

    result = [
        OMSOrderHeader(
            order_id=r.get("id", ""),
            order_number=r.get("OrderNo"),
            order_date=r.get("OrderDate"),
            order_type=r.get("DocumentType"),
            ship_to_id=r.get("ShipToID"),
            order_status=r.get("MaxOrderStatusDesc"),
            total_amount=r.get("OriginalTotalAmount"),
            payment_status=r.get("PaymentStatus"),
        )
        for r in response
    ]

    return ToolResponse(success=True, message="Following is the list of orders", content=result)
