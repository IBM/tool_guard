from enum import StrEnum
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ariba_client import get_ariba_client
from agent_ready_tools.clients.clients_enums import AribaApplications
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ARIBA_SUPPLIER_CONNECTIONS


class RegistrationStatus(StrEnum):
    """Enum specifying the registration status for suppliers in Ariba."""

    REGISTRATION_DENIED = "RegistrationDenied"
    PHASED_OUT = "PhasedOut"
    IN_CREATION = "InCreation"
    IN_EXTERNAL_APPROVAL_FOR_CREATION = "InExternalApprovalForCreation"
    NOT_INVITED = "NotInvited"
    INVITED = "Invited"
    IN_REGISTRATION = "InRegistration"
    PENDING_APPROVAL = "PendingApproval"
    PENDING_RESUBMIT = "PendingResubmit"
    REGISTERED = "Registered"
    UNKNOWN = "Unknown"


@dataclass
class AribaSupplierDetails:
    """Represents a supplier in ariba."""

    supplier_name: str
    sm_vendor_id: str
    erp_vendor_id: str
    supplier_an_id: str
    registration_status: str
    qualification_status: str
    address_line1: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]


@dataclass
class AribaSupplierDetailsResults:
    """Represents the response from getting all suppliers in SAP Ariba."""

    suppliers: List[AribaSupplierDetails]


@tool(expected_credentials=ARIBA_SUPPLIER_CONNECTIONS)
def ariba_get_suppliers(
    sm_vendor_id: Optional[str] = None,
    erp_vendor_id: Optional[str] = None,
    registration_status: Optional[RegistrationStatus] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[AribaSupplierDetailsResults]:
    """
    Gets the list of the suppliers from Sap Ariba.

    Args:
        sm_vendor_id: The SM Vendor ID of the supplier.
        erp_vendor_id: The ERP Vendor ID of the supplier.
        registration_status: The specific registration status to filter the suppliers.
        limit: The maximum number of suppliers to retrieve in a single API call. Defaults to 20. Use
            this to control the size of the result set.
        skip: The number of suppliers to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of suppliers.
    """

    # Setting the application name to SUPPLIER from ariba_client.py, as this tool operates with these credentials.
    try:
        client = get_ariba_client(application=AribaApplications.SUPPLIER)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "outputFormat": "JSON",
        "smVendorIds": [sm_vendor_id],
        "erpVendorIds": [erp_vendor_id],
        "registrationStatusList": [registration_status],
    }

    payload = {key: value for key, value in payload.items() if any(value)}

    params = {"$top": limit, "$skip": skip}
    endpoint = "supplierdatapagination/v4/prod/vendorDataRequests"

    response = client.post_request_list(endpoint=endpoint, payload=payload, params=params)

    if isinstance(response, dict):
        if "errorMsg" in response:
            content = response.get("errorMsg", "")
            return ToolResponse(
                success=False,
                message=f"Request unsuccessful {content}",
            )

    suppliers: List[AribaSupplierDetails] = []

    for supplier in response:
        if supplier.get("Supplier Name"):
            suppliers.append(
                AribaSupplierDetails(
                    supplier_name=supplier.get("Supplier Name", ""),
                    sm_vendor_id=supplier.get("SM Vendor ID", ""),
                    erp_vendor_id=supplier.get("ERP Vendor ID", ""),
                    supplier_an_id=supplier.get("An Id", ""),
                    registration_status=supplier.get("Registration Status", ""),
                    qualification_status=supplier.get("Qualification Status", ""),
                    address_line1=supplier.get("Address - Line1", ""),
                    city=supplier.get("Address - City", ""),
                    postal_code=supplier.get("Address - Postal Code", ""),
                    country_code=supplier.get("Address - Country Code", ""),
                )
            )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=AribaSupplierDetailsResults(suppliers=suppliers),
    )
