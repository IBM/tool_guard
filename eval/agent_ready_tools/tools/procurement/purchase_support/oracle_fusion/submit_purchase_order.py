from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionSubmitPurchaseOrder,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_submit_purchase_order(
    purchase_order_id: str,
) -> ToolResponse[OracleFusionSubmitPurchaseOrder]:
    """
    Submits a purchase order in Oracle Fusion.

    Args:
        purchase_order_id: The ID of the purchase order to submit, returned by oracle_fusion_get_all_purchase_orders.

    Returns:
        A ToolResponse object containing the API response or an error message.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError) as e:
        return ToolResponse(success=False, message=f"Failure to retrieve credentials: {e}")

    headers = {
        "Content-Type": "application/vnd.oracle.adf.action+json",
    }

    payload = {"validateBeforeSubmitFlag": "true"}

    response = client.post_request(
        resource_name=f"draftPurchaseOrders/{purchase_order_id}/action/submit",
        headers=headers,
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    submit_purchase_order = OracleFusionSubmitPurchaseOrder(
        result=response.get("result", ""),
    )

    return ToolResponse(
        success=True,
        message="Purchase order submitted successfully in Oracle Fusion.",
        content=submit_purchase_order,
    )
