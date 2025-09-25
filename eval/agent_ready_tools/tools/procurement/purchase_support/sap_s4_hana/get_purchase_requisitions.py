from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAPurchaseRequisitionGeneralDetails:
    """Represents the single header detail of the purchase requisition in SAP S4 HANA."""

    purchase_requisition_id: str
    purchase_requisition_type: Optional[str] = None
    purchase_requisition_description: Optional[str] = None


@dataclass
class S4HANAPurchaseRequisitionGeneralDetailsResponse:
    """The response containing the list of purchase requisition header details from SAP S4 HANA."""

    purchase_requisitions: List[S4HANAPurchaseRequisitionGeneralDetails]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchase_requisitions(
    purchase_requisition_id: Optional[str] = None,
    purchase_requisition_description: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAPurchaseRequisitionGeneralDetailsResponse]:
    """
    Gets the list of purchase requisitions in SAP S4 HANA.

    Args:
        purchase_requisition_id: The id of the purchase requisition in the SAP S4 HANA.
        purchase_requisition_description: The description of the purchase requisition in the SAP S4
            HANA.
        limit: The number of purchase requisitions returned.
        skip: The number of purchase requisitions to skip for pagination.

    Returns:
        The purchase requisition header details of the supplier.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = None
    if purchase_requisition_id:
        filter_expr = f"PurchaseRequisition eq '{purchase_requisition_id}'"
    elif purchase_requisition_description:
        filter_expr = f"PurReqnDescription eq '{purchase_requisition_description}'"
    elif purchase_requisition_id and purchase_requisition_description:
        filter_expr = f"PurchaseRequisition eq '{purchase_requisition_id}' and PurReqnDescription eq '{purchase_requisition_description}'"

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader",
        expand_expr="to_PurchaseReqnItem",
        params=params,
        filter_expr=filter_expr,
    )
    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    purchase_requisition_list = [
        S4HANAPurchaseRequisitionGeneralDetails(
            purchase_requisition_id=requisition.get("PurchaseRequisition", ""),
            purchase_requisition_type=requisition.get("PurchaseRequisitionType", ""),
            purchase_requisition_description=requisition.get("PurReqnDescription", ""),
        )
        for requisition in response["response"]["d"]["results"]
    ]

    result = S4HANAPurchaseRequisitionGeneralDetailsResponse(
        purchase_requisitions=purchase_requisition_list
    )
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
