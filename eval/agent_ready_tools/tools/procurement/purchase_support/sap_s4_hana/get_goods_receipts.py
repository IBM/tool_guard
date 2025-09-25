from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAGoodsReceipt:
    """Represents an goods receipt in SAP S4 HANA."""

    goods_receipt_id: str
    goods_receipt_year: str
    inventory_transaction_type: str
    created_by_user: str
    date_received: Optional[str] = None
    date_created: Optional[str] = None


@dataclass
class S4HANAGoodsReceiptsResponse:
    """Represents the response from retrieving a list of goods receipts in SAP S4 HANA."""

    goods_receipts: List[S4HANAGoodsReceipt]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_goods_receipts(
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    created_by: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAGoodsReceiptsResponse]:
    """
    Gets the list of the goods receipts from SAP S4 HANA.

    Args:
        created_after: The start date of the range for creation date given by user in ISO 8601
            format (e.g., YYYY-MM-DD).
        created_before: The end date of the range for creation date given by user in ISO 8601 format
            (e.g., YYYY-MM-DD).
        created_by: The info of user who created good receipt.
        limit: The number of goods receipts returned.
        skip: The number of goods receipts to skip for pagination.

    Returns:
        List of supplier goods receipts.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filters = []
    if created_after:
        filters.append(f"CreationDate ge datetime'{(created_after)}T00:00:00'")
    if created_before:
        filters.append(f"CreationDate le datetime'{(created_before)}T00:00:00'")
    if created_by:
        filters.append(f"CreatedByUser eq '{created_by}'")

    filter_expr = " and ".join(filters) if filters else None

    params = {"$top": limit, "$skip": skip}

    response = (
        client.get_request(
            entity="API_MATERIAL_DOCUMENT_SRV1/A_MaterialDocumentHeader",
            filter_expr=filter_expr,
            params=params,
        )
        if filter_expr
        else client.get_request(
            entity="API_MATERIAL_DOCUMENT_SRV1/A_MaterialDocumentHeader",
            params=params,
        )
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    goods_receipts: List[S4HANAGoodsReceipt] = []

    for result in response["response"]["d"]["results"]:
        goods_receipts.append(
            S4HANAGoodsReceipt(
                goods_receipt_id=result.get("MaterialDocument", ""),
                goods_receipt_year=result.get("MaterialDocumentYear", ""),
                inventory_transaction_type=result.get("InventoryTransactionType", ""),
                date_received=(
                    sap_date_to_iso_8601(result.get("DocumentDate", ""))
                    if result.get("DocumentDate") is not None
                    else None
                ),
                date_created=(
                    sap_date_to_iso_8601(result.get("CreationDate", ""))
                    if result.get("CreationDate") is not None
                    else None
                ),
                created_by_user=result.get("CreatedByUser", ""),
            )
        )
    result = S4HANAGoodsReceiptsResponse(goods_receipts=goods_receipts)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
