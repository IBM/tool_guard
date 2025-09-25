from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_purchase_requisition(
    purchase_requisition_id: str,
    description: Optional[str] = None,
) -> ToolResponse:
    """
    Updates the purchase requisition in SAP S4 HANA.

    Args:
        purchase_requisition_id: The id of the purchase requisition returned by `sap_s4_hana_get_purchase_requisitions` tool.
        description: The description of the purchase requisition.

    Returns:
        The http code of the update response.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "PurReqnDescription": description,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader('{purchase_requisition_id}')",
        payload=payload,
    )

    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    result = response
    return ToolResponse(
        success=True,
        message="The data was successfully updated",
        content=result,
    )
