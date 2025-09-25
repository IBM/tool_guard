from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAMaterialGroup:
    """Represents a material Group in SAP S4 HANA."""

    material_group: str
    material_group_name: str


@dataclass
class S4HANAMaterialGroupResponse:
    """A response containing the list of material groups from SAP S4 HANA."""

    material_group: List[S4HANAMaterialGroup]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_material_groups(
    material_group_name: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAMaterialGroupResponse]:
    """
    Retrieves a list of material groups from SAP S4 HANA.

    Args:
        material_group_name: The name of the material group in SAP S4 HANA.
        limit: The maximum number of material groups to retrieve.
        skip: The number of material groups to skip.

    Returns:
        A list of material groups in SAP S4 HANA
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filter_expr = f"ProductGroupName eq '{material_group_name}'" if material_group_name else None
    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="productgroup/0001/ProductGroup", filter_expr=filter_expr, params=params
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    results = response.get("response", {}).get("value", [])

    material_group = [
        S4HANAMaterialGroup(
            material_group=item.get("ProductGroup", ""),
            material_group_name=item.get("ProductGroupName", ""),
        )
        for item in results
    ]

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved.",
        content=S4HANAMaterialGroupResponse(material_group=material_group),
    )
