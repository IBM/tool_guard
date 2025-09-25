from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAPricingConditions:
    """Represents the pricing condition details of a purchase info record in SAP S4 HANA."""

    condition_record_id: str
    condition_rate_value: str
    condition_currency: str
    condition_quantity: str


@dataclass
class S4HANAPurchaseInfoRecord:
    """Represents a purchase info record in SAP S4 HANA."""

    purchasing_info_record_id: str
    material_id: str
    supplier_id: str
    supplier_phone_number: str
    plant: str
    currency: str
    net_amount: str
    quantity_per_net_amount: str
    standard_quantity: str
    planned_delivery_time: str
    supply_available_from: Optional[str] = None
    supply_available_to: Optional[str] = None
    minimum_quantity: Optional[str] = None
    tolerance_limit_over_delivery: Optional[str] = None
    tolerance_limit_under_delivery: Optional[str] = None
    unlimited_delivery_allowed: Optional[bool] = None
    pricing_conditions: Optional[List[S4HANAPricingConditions]] = None


@dataclass
class S4HANAPurchaseInfoResponse:
    """A response containing the list of purchase info records from SAP S4 HANA."""

    purchase_info: List[S4HANAPurchaseInfoRecord]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_purchasing_info_records(
    supplier_id: Optional[str] = None,
    material_id: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAPurchaseInfoResponse]:
    """
    Gets a list of purchase info records from SAP S4 HANA.

    Args:
        supplier_id: The unique identifer of the supplier in SAP S4 HANA, returned by the sap_s4_hana_get_suppliers tool.
        material_id: The id of the material in SAP S4 HANA, returned by the sap_s4_hana_get_materials tool.
        limit: The number of records returned.
        skip: The number of records to skip for pagination.

    Returns:
        A list of purchase info records.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = None
    if supplier_id and material_id:
        filter_expr = f"Supplier eq '{supplier_id}' and Material eq '{material_id}'"
    elif supplier_id:
        filter_expr = f"Supplier eq '{supplier_id}'"
    elif material_id:
        filter_expr = f"Material eq '{material_id}'"

    params = {"$top": limit, "$skip": skip}
    response = client.get_request(
        entity="100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord",
        filter_expr=filter_expr,
        expand_expr="to_PurgInfoRecdOrgPlantData/to_PurInfoRecdPrcgCndnValidity/to_PurInfoRecdPrcgCndn",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)
    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    results = response.get("response", {}).get("d", {}).get("results", [])
    purchase_info = []

    for item in results:
        for data in item.get("to_PurgInfoRecdOrgPlantData", {}).get("results", []):
            pricing_conditions = []
            availability_start = item.get("AvailabilityStartDate")
            availability_end = item.get("AvailabilityEndDate")

            for info in data.get("to_PurInfoRecdPrcgCndnValidity", {}).get("results", []):
                record = info.get("to_PurInfoRecdPrcgCndn", {})
                pricing_conditions.append(
                    S4HANAPricingConditions(
                        condition_record_id=info.get("ConditionRecord", ""),
                        condition_rate_value=record.get("ConditionRateValue", ""),
                        condition_currency=record.get("ConditionCurrency", ""),
                        condition_quantity=record.get("ConditionQuantity", ""),
                    )
                )

            purchase_info.append(
                S4HANAPurchaseInfoRecord(
                    purchasing_info_record_id=item.get("PurchasingInfoRecord", ""),
                    material_id=item.get("Material", ""),
                    supplier_id=item.get("Supplier", ""),
                    supplier_phone_number=item.get("SupplierPhoneNumber", ""),
                    plant=data.get("Plant", ""),
                    currency=data.get("Currency", ""),
                    minimum_quantity=data.get("MinimumPurchaseOrderQuantity", ""),
                    standard_quantity=data.get("StandardPurchaseOrderQuantity", ""),
                    planned_delivery_time=data.get("MaterialPlannedDeliveryDurn", ""),
                    supply_available_from=(
                        sap_date_to_iso_8601(availability_start) if availability_start else None
                    ),
                    supply_available_to=(
                        sap_date_to_iso_8601(availability_end) if availability_end else None
                    ),
                    tolerance_limit_over_delivery=data.get("OverdelivTolrtdLmtRatioInPct", ""),
                    tolerance_limit_under_delivery=data.get("UnderdelivTolrtdLmtRatioInPct", ""),
                    unlimited_delivery_allowed=data.get("UnlimitedOverdeliveryIsAllowed", ""),
                    net_amount=data.get("NetPriceAmount", ""),
                    quantity_per_net_amount=data.get("MaterialPriceUnitQty", ""),
                    pricing_conditions=pricing_conditions,
                )
            )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved.",
        content=S4HANAPurchaseInfoResponse(purchase_info=purchase_info),
    )
