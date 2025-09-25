from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierContactDetails,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_supplier_contact(
    supplier_id: str,
    supplier_contact_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone_country_code: Optional[str] = None,
    phone_area_code: Optional[str] = None,
    phone_number: Optional[str] = None,
    mobile_country_code: Optional[str] = None,
    mobile_area_code: Optional[str] = None,
    mobile_number: Optional[str] = None,
    email: Optional[str] = None,
) -> ToolResponse[OracleFusionSupplierContactDetails]:
    """
    Update contact details of a supplier in Oracle Fusion.

    Args:
        supplier_id: The id of the supplier, returned by the oracle_fusion_get_all_suppliers tool. This ID is obtained by
            applying filters such as the supplier's name, number, or other relevant criteria.
        supplier_contact_id: The unique identifier of a supplier contact, obtained by calling the oracle_fusion_get_supplier_contacts tool using the supplier_id.
        first_name: The first name of the supplier contact.
        last_name: The last name of the supplier contact.
        phone_country_code: The country code for the contact's phone number.
        phone_area_code: The area code for the contact's phone number.
        phone_number: The contact's phone number.
        mobile_country_code: The country code for the contact's mobile number.
        mobile_area_code: The area code for the contact's mobile number.
        mobile_number: The contact's mobile number.
        email: The email address of the supplier contact.

    Returns:
        Updated contact details for the selected supplier contact.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "FirstName": first_name,
        "LastName": last_name,
        "PhoneCountryCode": phone_country_code,
        "PhoneAreaCode": phone_area_code,
        "PhoneNumber": phone_number,
        "MobileCountryCode": mobile_country_code,
        "MobileAreaCode": mobile_area_code,
        "MobileNumber": mobile_number,
        "Email": email,
    }

    payload = {key: value for key, value in payload.items() if value}

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        resource_name=f"suppliers/{supplier_id}/child/contacts/{supplier_contact_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    contact_details = OracleFusionSupplierContactDetails(
        supplier_contact_id=response.get("SupplierContactId", -1),
        first_name=response.get("FirstName", ""),
        last_name=response.get("LastName", ""),
        phone_country_code=response.get("PhoneCountryCode", ""),
        phone_area_code=response.get("PhoneAreaCode", ""),
        phone_number=response.get("PhoneNumber", ""),
        mobile_country_code=response.get("MobileCountryCode", ""),
        mobile_area_code=response.get("MobileAreaCode", ""),
        mobile_number=response.get("MobileNumber", ""),
        email=response.get("Email", ""),
    )

    return ToolResponse(
        success=True,
        message="Updated the contact of a supplier from Oracle Fusion.",
        content=contact_details,
    )
