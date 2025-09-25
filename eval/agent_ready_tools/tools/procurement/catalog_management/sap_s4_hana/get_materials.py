from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAMaterial:
    """Represents a material in SAP S4 HANA."""

    material_id: str
    material_type: str
    created_by: str
    creation_date: str
    material_group: str
    base_unit: str


@dataclass
class S4HANAMaterialResponse:
    """A response containing the list of materials from SAP S4 HANA."""

    materials: List[S4HANAMaterial]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_materials(
    material_id: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAMaterialResponse]:
    """
    Retrieves a list of materials from SAP S4 HANA.

    Args:
        material_id: The material's id uniquely identifying it within the SAP S4 HANA.
        limit: The maximum number of materials to retrieve.
        skip: The number of materials to skip.

    Returns:
        A list of materials in SAP S4 HANA
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = f"Product eq '{material_id}'" if material_id else None
    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="API_PRODUCT_SRV/A_Product", filter_expr=filter_expr, params=params
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    results = response.get("response", {}).get("d", {}).get("results", [])

    materials = [
        S4HANAMaterial(
            material_id=item.get("Product", ""),
            material_type=item.get("ProductType", ""),
            created_by=item.get("CreatedByUser", ""),
            creation_date=sap_date_to_iso_8601(item.get("CreationDate", "")),
            material_group=item.get("ProductGroup", ""),
            base_unit=item.get("BaseUnit", ""),
        )
        for item in results
    ]

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved.",
        content=S4HANAMaterialResponse(materials=materials),
    )
