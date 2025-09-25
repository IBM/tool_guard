from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaUpdatePurchasingInfoRecordResponse:
    """Represents update supplier response in SAP S4 HANA."""

    http_code: Optional[int] = None


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_purchasing_info_record(
    purchasing_info_record_id: str,
    supplier: str,
    material: str,
    purchasing_info_record_desc: Optional[str] = None,
    supplier_resp_sales_person_name: Optional[str] = None,
    supplier_phone_number: Optional[str] = None,
    availability_start_date: Optional[str] = None,
    availability_end_date: Optional[str] = None,
    manufacturer: Optional[str] = None,
    product_purchase_points_quantity: Optional[str] = None,
    product_purchase_points_quantity_unit: Optional[str] = None,
) -> ToolResponse[S4HanaUpdatePurchasingInfoRecordResponse]:
    """
    Updates a purchasing info record in SAP S/4HANA with selected fields.

    Args:
        purchasing_info_record_id: The ID of the purchasing info record to be updated, returned by `sap_s4_hana_get_purchasing_info_records` tool .
        supplier: Supplier ID of existing purchasing info record, returned by `sap_s4_hana_get_purchasing_info_records` tool.
        material: Material ID of existing purchasing info record, returned by `sap_s4_hana_get_purchasing_info_records` tool.
        purchasing_info_record_desc: New description for purchasing order info record.
        supplier_resp_sales_person_name: New sales person name for purchasing order info record.
        supplier_phone_number: New supplier phone number for purchasing order info record.
        availability_start_date: New availability start date in ISO 8601 format (e.g., YYYY-MM-DD).
        availability_end_date: New availability end date in ISO 8601 format (e.g., YYYY-MM-DD).
        manufacturer: New manufacturer name for purchasing order info record
        product_purchase_points_quantity: New product purchase points quantity for purchasing order info record.
        product_purchase_points_quantity_unit: New product purchase points quantity unit(UOM) for purchasing order info record.

    Returns:
        The http code of the update response.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    client = get_sap_s4_hana_client()

    payload: Dict[str, Any] = {
        "Supplier": supplier,
        "Material": material,
        "PurchasingInfoRecordDesc": purchasing_info_record_desc,
        "SupplierRespSalesPersonName": supplier_resp_sales_person_name,
        "SupplierPhoneNumber": supplier_phone_number,
        "AvailabilityStartDate": (
            iso_8601_to_sap_date(availability_start_date) if availability_start_date else None
        ),
        "AvailabilityEndDate": (
            iso_8601_to_sap_date(availability_end_date) if availability_end_date else None
        ),
        "Manufacturer": manufacturer,
        "ProductPurchasePointsQty": product_purchase_points_quantity,
        "ProductPurchasePointsQtyUnit": product_purchase_points_quantity_unit,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity=f"100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord('{purchasing_info_record_id}')",
        payload={"d": payload},
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful1", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful2", content=content)

    response_status_code = response.get("http_code")

    return ToolResponse(
        success=True,
        message="Record updated successfully.",
        content=S4HanaUpdatePurchasingInfoRecordResponse(http_code=response_status_code),
    )
