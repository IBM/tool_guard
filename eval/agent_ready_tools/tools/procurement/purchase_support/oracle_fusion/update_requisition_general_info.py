from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionPurchaseRequisitionHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_requisition_general_info(
    purchase_requisition_id: str,
    description: Optional[str] = None,
    justification: Optional[str] = None,
) -> ToolResponse[OracleFusionPurchaseRequisitionHeader]:
    """
    Updates general info of a requisition in Oracle Fusion.

    Args:
        purchase_requisition_id: The id of the requisition, returned by the `oracle_fusion_get_all_purchase_requisitions` tool.
        description: Updated description of the requisition.
        justification: Business justification for the requisition.

    Returns:
        Updated header details for the selected requisition.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "Description": description,
        "Justification": justification,
    }

    payload = {key: value for key, value in payload.items() if value}

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        resource_name=f"purchaseRequisitions/{purchase_requisition_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    header_details = OracleFusionPurchaseRequisitionHeader(
        purchase_requisition_id=response.get("RequisitionHeaderId", -1),
        requisition_number=response.get("Requisition", ""),
        preparer=response.get("Preparer", ""),
        description=response.get("Description", ""),
        document_status=response.get("DocumentStatus", ""),
        creation_date=response.get("CreationDate", ""),
        fund_status=response.get("FundsStatus", ""),
        justification=response.get("Justification", ""),
    )

    return ToolResponse(
        success=True,
        message="Updated the general info of a purchase requisition from Oracle Fusion.",
        content=header_details,
    )
