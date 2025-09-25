from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class SAPS4HANAMaterialType:
    """Represents a material type in SAP S4 HANA."""

    material_type_id: str
    material_type_name: str


@dataclass
class SAPS4HANAMaterialTypeResponse:
    """A response containing the list of material types from SAP S4 HANA."""

    material_types: List[SAPS4HANAMaterialType]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_material_types(
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    material_type_name: Optional[str] = None,
) -> ToolResponse[SAPS4HANAMaterialTypeResponse]:
    """
    Retrieves a list of material types from SAP S4 HANA.

    Args:
        limit: The maximum number of material types to retrieve.
        skip: The number of material types to skip.
        material_type_name: The name of the material type.

    Returns:
        A list of material types.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = f"ProductTypeName eq '{material_type_name}'" if material_type_name else None
    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="producttype/0001/ProductType", filter_expr=filter_expr, params=params
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    results = response.get("response", {}).get("value", [])

    material_types = [
        SAPS4HANAMaterialType(
            material_type_id=item.get("ProductType", ""),
            material_type_name=item.get("ProductTypeName", ""),
        )
        for item in results
    ]

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved.",
        content=SAPS4HANAMaterialTypeResponse(material_types=material_types),
    )
