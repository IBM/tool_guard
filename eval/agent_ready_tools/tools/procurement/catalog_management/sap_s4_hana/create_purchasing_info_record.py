from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANACreatePurchasingInfoRecordResponse:
    """Represents the result of creating a purchasing info record in SAP S4 HANA."""

    purchasing_info_record_id: Optional[str] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_purchasing_info_record(
    supplier_id: str,
    material_id: str,
    purchasing_organization: str,
    planned_delivery_time: str,
    purchasing_group: str,
    standard_quantity: str,
    net_amount: str,
    quantity_per_net_amount: str,
    supply_available_from: Optional[str] = None,
    supply_available_to: Optional[str] = None,
    minimum_quantity: Optional[str] = None,
    tolerance_limit_under_delivery: Optional[str] = None,
    tolerance_limit_over_delivery: Optional[str] = None,
    unlimited_delivery_allowed: Optional[bool] = None,
) -> ToolResponse[S4HANACreatePurchasingInfoRecordResponse]:
    """
    Creates purchasing info record for linking a material to a supplier in SAP S4 HANA.

    Args:
        supplier_id: The id of the supplier, returned by sap_s4_hana_get_suppliers tool.
        material_id: The id of the material, returned by the sap_s4_hana_get_materials tool.
        purchasing_organization: The purchasing organization of the supplier.
        planned_delivery_time: The planned delivery time for the material to deliver.
        purchasing_group: The purchasing group of the supplier.
        standard_quantity: The default quantity for the material.
        net_amount: The total price amount for the specified quantity.
        quantity_per_net_amount: The quantity corresponding to the net amount.
        supply_available_from: The start date when the supply is available in ISO 8601 format (e.g., YYYY-MM-DD).
        supply_available_to: The end date when the supply is available in ISO 8601 format (e.g., YYYY-MM-DD).
        minimum_quantity: The minimum order quantity required.
        tolerance_limit_under_delivery: The allowable percentage below the ordered quantity.
        tolerance_limit_over_delivery: The allowable percentage above the ordered quantity.
        unlimited_delivery_allowed: Indicates if unlimited delivery is permitted (true/false).

    Returns:
        Result from creating a purchasing info record.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    purchasing_info_org_data: Dict[str, Any] = {
        "PurchasingOrganization": purchasing_organization,
        "MaterialPlannedDeliveryDurn": planned_delivery_time,
        "PurchasingGroup": purchasing_group,
        "StandardPurchaseOrderQuantity": standard_quantity,
        "MinimumPurchaseOrderQuantity": minimum_quantity,
        "OverdelivTolrtdLmtRatioInPct": tolerance_limit_under_delivery,
        "UnderdelivTolrtdLmtRatioInPct": tolerance_limit_over_delivery,
        "UnlimitedOverdeliveryIsAllowed": unlimited_delivery_allowed,
        "NetPriceAmount": net_amount,
        "MaterialPriceUnitQty": quantity_per_net_amount,
    }

    purchasing_info_org_data = {
        key: value for key, value in purchasing_info_org_data.items() if value is not None
    }

    payload: Dict[str, Any] = {
        "Supplier": supplier_id,
        "Material": material_id,
        "AvailabilityStartDate": (
            iso_8601_to_sap_date(supply_available_from) if supply_available_from else None
        ),
        "AvailabilityEndDate": (
            iso_8601_to_sap_date(supply_available_to) if supply_available_to else None
        ),
        "to_PurgInfoRecdOrgPlantData": {"results": [purchasing_info_org_data]},
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    response = client.post_request(
        entity="100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord", payload=payload
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    record_id = response.get("d", {}).get("PurchasingInfoRecord", "")
    result = S4HANACreatePurchasingInfoRecordResponse(purchasing_info_record_id=record_id)

    return ToolResponse(
        success=True, message="The record was successfully created.", content=result
    )
