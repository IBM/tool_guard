from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaSupplierAddress,
    get_business_partner_id_of_supplier,
)
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaSupplierAddressResponse:
    """A response containing the list of supplier address details from SAP S4 HANA."""

    address_details: list[S4HanaSupplierAddress]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_supplier_address(
    supplier_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaSupplierAddressResponse]:
    """
    Gets the address details of a supplier.

    Args:
        supplier_id: The id of the supplier returned by sap_s4_hana_get_suppliers tool.
        limit: The number of suppliers returned.
        skip: The number of suppliers to skip for pagination.

    Returns:
        The address details of the supplier.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    params = {"$top": limit, "$skip": skip}

    # calling the utility function to get the business_partner_id associated to supplier.
    bp_response = get_business_partner_id_of_supplier(supplier_id=supplier_id)

    if not bp_response.success:
        content = bp_response.content
        return ToolResponse(success=False, message=f"Failed to fetch Supplier ID {content}")

    if bp_response.content is not None:
        business_partner_id = bp_response.content.business_partner_id
    if not business_partner_id:
        return ToolResponse(
            success=False,
            message="Please enter a valid supplier ID",
        )

    response = client.get_request(
        entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{business_partner_id}')/to_BusinessPartnerAddress",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    address_details: List[S4HanaSupplierAddress] = []

    for address in response["response"]["d"]["results"]:
        address_details.append(
            S4HanaSupplierAddress(
                address_id=address.get("AddressID", ""),
                street_name=address.get("StreetName", ""),
                house_number=address.get("HouseNumber", ""),
                postal_code=address.get("PostalCode", ""),
                city=address.get("CityName", ""),
                country=address.get("Country", ""),
                region=address.get("Region", ""),
                time_zone=address.get("AddressTimeZone", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HanaSupplierAddressResponse(address_details=address_details),
    )
