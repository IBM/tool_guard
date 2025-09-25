from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionDetails,
)
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_helper_functions import (
    oracle_fusion_build_requisition_from_response,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_purchase_requisition_by_id(
    purchase_requisition_id: str,
) -> ToolResponse[OracleFusionPurchaseRequisitionDetails]:
    """
    Gets a purchase requisition by purchase requisition id in Oracle Fusion.

    Args:
        purchase_requisition_id: The id of the purchase requisition, returned by the `oracle_fusion_get_all_purchase_requisitions` tool.

    Returns:
        The resulting purchase order retrieved using the purchase_requisition_id.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"purchaseRequisitions/{purchase_requisition_id}",
        params={"expand": "lines.distributions"},
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    purchase_requisitions = oracle_fusion_build_requisition_from_response(response)

    return ToolResponse(
        success=True,
        message="Retrieved the purchase requisitions from Oracle Fusion.",
        content=purchase_requisitions,
    )
