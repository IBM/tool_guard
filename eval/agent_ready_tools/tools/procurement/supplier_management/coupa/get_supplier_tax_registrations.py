from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierTaxRegistration,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_supplier_tax_registrations(
    supplier_id: int,
) -> ToolResponse[List[CoupaSupplierTaxRegistration]]:
    """
    Get a supplier's tax registrations by their id.

    Args:
        supplier_id: Supplier ID

    Returns:
        A list of a supplier's tax registrations
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}",
        params={
            "fields": '[{"supplier_addresses":[{"tax_registrations":["id","number","active",{"country":["name"]}]}]}]'
        },
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    tax_registrations = []

    supplier_address_data = response.get("supplier-addresses", [])
    for registrations in supplier_address_data:
        tax_reg_list = registrations.get("tax-registrations", [])
        if tax_reg_list:
            for tax_reg in tax_reg_list:
                tax_registrations.append(
                    CoupaSupplierTaxRegistration(
                        id=tax_reg.get("id"),
                        number=tax_reg.get("number"),
                        active=tax_reg.get("active"),
                        country=tax_reg.get("country", {}).get("name"),
                    )
                )

    return ToolResponse(
        success=True,
        message="Get supplier tax registrations successful",
        content=tax_registrations,
    )
