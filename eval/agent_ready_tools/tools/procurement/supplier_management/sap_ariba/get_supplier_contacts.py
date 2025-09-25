from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ariba_client import get_ariba_client
from agent_ready_tools.clients.clients_enums import AribaApplications
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ARIBA_SUPPLIER_CONNECTIONS


@dataclass
class AribaSupplierContact:
    """Represents the single supplier contact in SAP Ariba."""

    first_name: str
    last_name: str
    email_address: str
    is_primary: bool
    timezone: str
    language: str
    middle_name: Optional[str] = None
    mobile_phone: Optional[str] = None
    office_phone: Optional[str] = None
    region: Optional[str] = None
    contact_type: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None


@dataclass
class AribaSupplierContactsResponse:
    """List of the supplier contacts in SAP Ariba."""

    contact_details: List[AribaSupplierContact]


@tool(expected_credentials=ARIBA_SUPPLIER_CONNECTIONS)
def ariba_get_supplier_contacts(sm_vendor_id: str) -> ToolResponse[AribaSupplierContactsResponse]:
    """
    Gets the list of the supplier contacts in SAP Ariba.

    Args:
        sm_vendor_id: The SM Vendor ID of the supplier, returned by the `get_suppliers` tool.

    Returns:
        The list of supplier contacts.
    """

    # Setting the application name to SUPPLIER from ariba_client.py, as this tool operates with these credentials.
    try:
        client = get_ariba_client(application=AribaApplications.SUPPLIER)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {"smVendorIds": [f"{sm_vendor_id}"]}

    response = client.post_request(
        endpoint="supplierdatapagination/v4/prod/vendorContactsRequests", payload=payload
    )

    if "errorMsg" in response:
        content = response.get("errorMsg", "")
        return ToolResponse(
            success=False,
            message=f"Request unsuccessful {content}",
        )

    vendor_details = response.get("vendorDetails", [])
    contact_details_list = [
        AribaSupplierContact(
            first_name=contact.get("firstName", ""),
            last_name=contact.get("lastName", ""),
            middle_name=contact.get("middleName", ""),
            email_address=contact.get("email", ""),
            mobile_phone=contact.get("mobilePhone", ""),
            office_phone=contact.get("telephone", ""),
            region=contact.get("regions", ""),
            contact_type=contact.get("type", ""),
            title=contact.get("title", ""),
            department=contact.get("departments", ""),
            timezone=contact.get("timeZoneId", ""),
            language=contact.get("locale", ""),
            is_primary=contact.get("primary", False),
        )
        for vendor_contact in vendor_details
        for contact in vendor_contact.get("vendorContactInfos", [])
    ]
    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=AribaSupplierContactsResponse(contact_details=contact_details_list),
    )
