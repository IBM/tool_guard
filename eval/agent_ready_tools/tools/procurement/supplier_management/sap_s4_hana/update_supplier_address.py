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
class S4HanaUpdateSupplierAddressResponse:
    """Represents a update supplier's address response in SAP S4 HANA."""

    http_code: int


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_supplier_address(
    supplier_id: str,
    address_id: str,
    address_line: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    postal_code: Optional[str] = None,
    house_number: Optional[str] = None,
    region: Optional[str] = None,
) -> ToolResponse[S4HanaUpdateSupplierAddressResponse]:
    """
    Updates the supplier address in SAP S4 HANA.

    Args:
        supplier_id: The id of the supplier returned by sap_s4_hana_get_suppliers tool..
        address_id: The address ID of the supplier, returned by sap_s4_hana_get_supplier_address
            tool.
        address_line: The address of the supplier.
        city: The city of the supplier address.
        country: The country_code of the supplier address, returned by sap_s4_hana_get_countries
            tool.
        postal_code: The postal code of the supplier address.
        house_number: The house number of the supplier address.
        region: The region of the supplier address.

    Returns:
        The http code of the update response.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "StreetName": address_line,
        "CityName": city,
        "Country": country,
        "PostalCode": postal_code,
        "HouseNumber": house_number,
        "Region": region,
    }
    payload = {key: value for key, value in payload.items() if value}

    bp_response = get_business_partner_id_of_supplier(supplier_id=supplier_id)

    if not bp_response.success:
        content = bp_response.content
        return ToolResponse(
            success=False,
            message=f"Failed to fetch Supplier ID {content}",
        )

    if bp_response.content is not None:
        business_partner_id = bp_response.content.business_partner_id
    if not business_partner_id:
        return ToolResponse(
            success=False,
            message="Please enter a valid supplier ID",
        )

    response = client.patch_request(
        entity=f"API_BUSINESS_PARTNER/A_BusinessPartnerAddress(BusinessPartner='{business_partner_id}',AddressID='{address_id}')",
        payload={"d": payload},
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
        content=S4HanaUpdateSupplierAddressResponse(http_code=response["http_code"]),
    )
