from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS

# Dictionary representing the available types of GR/GI Slips
print_version_types = {
    "1": "Individual Slip",
    "2": "Individual Slip with Inspection Text",
    "3": "Collective Slip",
}


@dataclass
class SAPS4HanaGoodsReceiptItemDetails:
    """Represents the item details of a goods receipt in SAP S4 HANA."""

    material_document_item: str
    material_short_text: str
    quantity_in_unit_of_entry: str
    entry_unit: str
    storage_location: str
    gl_account: str
    stock_segment: str
    batch: str
    movement_type: str
    plant: str
    customer: str
    goods_recipient: str
    supplier: str
    sales_order: str
    sales_order_item: str
    purchase_order: str
    purchase_order_item: str
    wbs_element: str
    quantity: str
    base_unit: str
    material_number: str
    currency_code: str


@dataclass
class SapS4HanaGoodsReceiptDetails:
    """Represents the details of a goods receipt in SAP S4 HANA."""

    material_slip: str
    print_version: str
    material_document_header_text: str
    item_details: List[SAPS4HanaGoodsReceiptItemDetails]
    document_date: Optional[str] = None
    posting_date: Optional[str] = None


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_a_goods_receipt_details(
    goods_receipt_id: str, goods_receipt_year: str
) -> ToolResponse[SapS4HanaGoodsReceiptDetails]:
    """
    Gets the details of a goods receipt from SAP S4 HANA.

    Args:
        goods_receipt_id: The goods_receipt_id of the goods receipt, returned by the
            sap_s4_hana_get_goods_receipts tool.
        goods_receipt_year: The goods_receipt_year of the goods receipt, returned by the
            sap_s4_hana_get_goods_receipts tool.

    Returns:
        The details of a goods receipt.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        entity=f"API_MATERIAL_DOCUMENT_SRV1/A_MaterialDocumentHeader(MaterialDocumentYear='{goods_receipt_year}',MaterialDocument='{goods_receipt_id}')",
        expand_expr="to_MaterialDocumentItem",
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    result = response.get("response", {}).get("d", {})

    goods_receipt_details = SapS4HanaGoodsReceiptDetails(
        document_date=(
            sap_date_to_iso_8601(result.get("DocumentDate", ""))
            if result.get("DocumentDate", "") is not None
            else None
        ),
        posting_date=(
            sap_date_to_iso_8601(result.get("PostingDate", ""))
            if result.get("PostingDate", "") is not None
            else None
        ),
        material_slip=result.get("ReferenceDocument", ""),
        print_version=(
            print_version_types.get(result.get("VersionForPrintingSlip", ""), "")
            if result.get("VersionForPrintingSlip", "")
            else ""
        ),
        material_document_header_text=result.get("MaterialDocumentHeaderText", ""),
        item_details=[
            SAPS4HanaGoodsReceiptItemDetails(
                material_document_item=item.get("MaterialDocumentItem", ""),
                material_short_text=item.get("Material", ""),
                quantity_in_unit_of_entry=item.get("QuantityInEntryUnit", ""),
                entry_unit=item.get("EntryUnit", ""),
                storage_location=item.get("StorageLocation", ""),
                gl_account=item.get("GLAccount", ""),
                stock_segment=item.get("StockSegment", ""),
                batch=item.get("Batch", ""),
                movement_type=item.get("GoodsMovementType", ""),
                plant=item.get("Plant", ""),
                customer=item.get("Customer", ""),
                goods_recipient=item.get("GoodsRecipientName", ""),
                supplier=item.get("Supplier", ""),
                sales_order=item.get("SalesOrder", ""),
                sales_order_item=item.get("SalesOrderItem", ""),
                purchase_order=item.get("PurchaseOrder", ""),
                purchase_order_item=item.get("PurchaseOrderItem", ""),
                wbs_element=item.get("WBSElement", ""),
                quantity=item.get("QuantityInBaseUnit", ""),
                base_unit=item.get("MaterialBaseUnit", ""),
                material_number=item.get("Material", ""),
                currency_code=item.get("CompanyCodeCurrency", ""),
            )
            for item in result.get("to_MaterialDocumentItem", {}).get("results", [])
        ],
    )

    return ToolResponse(
        success=True, message="The data was successfully retrieved", content=goods_receipt_details
    )
