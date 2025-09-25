from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.common_classes_sap_s4_hana_catalog_management import (
    S4HANABaseUnit,
    S4HANAIndustrySector,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_material(
    material_id: str,
    material_type: Optional[str] = None,
    gross_weight: Optional[str] = None,
    weight_unit: Optional[S4HANABaseUnit] = None,
    net_weight: Optional[str] = None,
    purchase_order_quantity_unit: Optional[S4HANABaseUnit] = None,
    base_unit: Optional[S4HANABaseUnit] = None,
    material_group: Optional[str] = None,
    industry_sector: Optional[S4HANAIndustrySector] = None,
) -> ToolResponse:
    """
    Updates the material in SAP S4 HANA.

    Args:
        material_id: The ID of the material returned by the tool `sap_s4_hana_get_materials`.
        material_type: The Type of the material returned by the tool `sap_s4_hana_get_material_types`.
        gross_weight: The Gross weight of the material.
        weight_unit: The Unit of weight of the material.
        net_weight: The Net weight of the material.
        purchase_order_quantity_unit: The Purchase order quantity unit of the material.
        base_unit: The Base unit of measure.
        material_group: The material group returned by the tool `sap_s4_hana_get_material_groups`.
        industry_sector: The Industry sector of the material.

    Returns:
        The HTTP status code of the update response.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: Dict[str, Any] = {
        "ProductType": material_type,
        "GrossWeight": gross_weight,
        "WeightUnit": S4HANABaseUnit[weight_unit.upper()].value if weight_unit else None,
        "NetWeight": net_weight,
        "PurchaseOrderQuantityUnit": (
            S4HANABaseUnit[purchase_order_quantity_unit.upper()].value
            if purchase_order_quantity_unit
            else None
        ),
        "BaseUnit": S4HANABaseUnit[base_unit.upper()].value if base_unit else None,
        "ProductGroup": material_group,
        "IndustrySector": (
            S4HANAIndustrySector[industry_sector.upper()].value if industry_sector else None
        ),
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        entity=f"100/API_PRODUCT_SRV/A_Product('{material_id}')",
        payload={"d": payload},
    )

    if isinstance(response, int):
        return ToolResponse(
            success=True,
            message="The record was successfully updated.",
            content={"status_code": response},
        )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    return ToolResponse(
        success=True, message="The record was successfully updated.", content=response
    )
