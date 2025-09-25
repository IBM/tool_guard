from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    get_business_partner_id_of_supplier,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaUpdateSupplierResponse:
    """Represents a update supplier response in SAP S4 HANA."""

    http_code: int


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_supplier(
    supplier_id: str,
    supplier_name: Optional[str] = None,
    supplier_name2: Optional[str] = None,
    supplier_name3: Optional[str] = None,
    supplier_name4: Optional[str] = None,
    search_term: Optional[str] = None,
) -> ToolResponse[S4HanaUpdateSupplierResponse]:
    """
    Updates the supplier in SAP S4 HANA.

    Args:
        supplier_id: The id of the supplier returned by `sap_s4_hana_get_suppliers` tool.
        supplier_name: The Name of the supplier.
        supplier_name2: The Name 2 of the supplier.
        supplier_name3: The Name 3 of the supplier.
        supplier_name4: The Name 4 of the supplier.
        search_term: The search term of the supplier in the SAP S4 HANA.

    Returns:
        The http code of the update response.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "OrganizationBPName1": supplier_name,
        "OrganizationBPName2": supplier_name2,
        "OrganizationBPName3": supplier_name3,
        "OrganizationBPName4": supplier_name4,
        "SearchTerm1": search_term,
    }
    payload = {key: value for key, value in payload.items() if value}

    bp_response = get_business_partner_id_of_supplier(supplier_id=supplier_id)

    if not bp_response.success:
        content = bp_response.content
        return ToolResponse(success=False, message=f"Failed to fetch Supplier ID {content}")

    if bp_response.content is not None:
        business_partner_id = bp_response.content.business_partner_id
    if not business_partner_id:
        return ToolResponse(success=False, message="Please enter a valid supplier ID")

    response = client.patch_request(
        entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{business_partner_id}')",
        payload=payload,
    )

    if "error" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["error"]["message"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    return ToolResponse(
        success=True,
        message="The data was successfully updated",
        content=S4HanaUpdateSupplierResponse(http_code=response["http_code"]),
    )
