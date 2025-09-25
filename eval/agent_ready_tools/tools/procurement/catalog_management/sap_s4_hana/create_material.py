from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.common_classes_sap_s4_hana_catalog_management import (
    S4HANABaseUnit,
    S4HANAIndustrySector,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANACreateMaterialResponse:
    """Represents the result of creating a material in SAP S4 HANA."""

    material_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_material(
    material_type: str,
    base_unit: S4HANABaseUnit,
    industry_sector: S4HANAIndustrySector,
    material_description: str,
) -> ToolResponse[S4HANACreateMaterialResponse]:
    """
    Creates a material in SAP S4 HANA.

    Args:
        material_type: The type of the material.
        base_unit: The base unit of measure for material.
        industry_sector: The industry sector of the material.
        material_description: The description of the material.

    Returns:
        Result from creating a material.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: Dict[str, Any] = {
        "ProductType": material_type.upper(),
        "BaseUnit": S4HANABaseUnit[base_unit.upper()].value,
        "IndustrySector": S4HANAIndustrySector[industry_sector.upper()].value,
        "to_Description": {
            "results": [{"Language": "EN", "ProductDescription": material_description}]
        },
    }

    response = client.post_request(
        entity="API_PRODUCT_SRV/A_Product",
        payload=payload,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    material_id = response.get("d", {}).get("Product", "")
    result = S4HANACreateMaterialResponse(material_id=material_id)

    return ToolResponse(
        success=True, message="The record was successfully created.", content=result
    )
