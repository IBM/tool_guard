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
class SAPS4HanaCreateAddressResponse:
    """Represents the response of the create address in SAP S4 HANA."""

    supplier_id: str
    address_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_supplier_address(
    supplier_id: str,
    city: str,
    country: str,
    postal_code: str,
    address_line: str,
    house_number: Optional[str] = None,
    region: Optional[str] = None,
    address_timezone: Optional[str] = None,
) -> ToolResponse[SAPS4HanaCreateAddressResponse]:
    """
    Creates the supplier address in SAP S4 HANA.

    Args:
        supplier_id: The id of the supplier, returned by sap_s4_hana_get_suppliers tool.
        city: The city of the supplier address.
        country: Country of the supplier in ISO 3166-1 alpha-2 standard.
        postal_code: The postal code of the supplier address.
        address_line: The street name of the supplier.
        house_number: The house number of the supplier address.
        region: The region of the supplier address.
        address_timezone: The timezone of the supplier address.

    Returns:
        The result from performing the creation of the supplier address.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    # calling the utility function to get the business_partner_id associated to supplier.
    bp_response = get_business_partner_id_of_supplier(supplier_id=supplier_id)

    if not bp_response.success:
        content = bp_response.content
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    if bp_response.content is not None:
        business_partner_id = bp_response.content.business_partner_id
    if not business_partner_id:
        return ToolResponse(
            success=False,
            message="Please enter a valid supplier ID",
        )

    payload = {
        "StreetName": address_line,
        "CityName": city,
        "Country": country,
        "PostalCode": postal_code,
        "HouseNumber": house_number,
        "Region": region,
        "AddressTimeZone": address_timezone,
    }
    payload = {key: value for key, value in payload.items() if value}
    response = client.post_request(
        entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{business_partner_id}')/to_BusinessPartnerAddress",
        payload=payload,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    result = response.get("d", {})

    supplier_id = result.get("BusinessPartner", "")
    address_id = result.get("AddressID", "")

    return ToolResponse(
        success=True,
        message="The supplier address was successfully created.",
        content=SAPS4HanaCreateAddressResponse(supplier_id=supplier_id, address_id=address_id),
    )
