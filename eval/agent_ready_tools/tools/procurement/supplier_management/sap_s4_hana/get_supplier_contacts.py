from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    Department,
    FunctionOfPartner,
    get_business_partner_id_of_supplier,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaSupplierContact:
    """Represents a supplier's contact in SAP S4 HANA."""

    contact_person: str
    email_address: str
    relationship: str
    validity_from: str
    validity_to: str
    contact_person_function: str
    department: str
    phone_number: str
    phone_number_extension: str


@dataclass
class S4HanaSupplierContactsResponse:
    """A response containing the list of supplier contact details from SAP S4 HANA."""

    contact_details: list[S4HanaSupplierContact]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_supplier_contacts(
    supplier_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaSupplierContactsResponse]:
    """
    Gets a list of supplier contacts.

    Args:
        supplier_id: The id of the supplier returned by the tool sap_s4_hana_get_suppliers.
        limit: The number of supplier contacts returned.
        skip: The number of supplier contacts to skip for pagination.

    Returns:
        List of supplier contacts from SAP S4 HANA.
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
        return ToolResponse(success=False, message="Please enter a valid supplier ID")

    response = client.get_request(
        entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{business_partner_id}')/to_BusinessPartnerContact",
        expand_expr="to_ContactRelationship,to_ContactAddress",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    contact_details: List[S4HanaSupplierContact] = []

    for contact in response["response"]["d"]["results"]:
        contact_person = contact.get("BusinessPartnerPerson", "")
        relationship = contact.get("RelationshipCategory", "")
        validity_from = sap_date_to_iso_8601(contact.get("ValidityStartDate", ""))
        validity_to = sap_date_to_iso_8601(contact.get("ValidityEndDate", ""))
        contact_person_function = contact.get("to_ContactRelationship", {}).get(
            "ContactPersonFunction", ""
        )
        department = contact.get("to_ContactRelationship", {}).get("ContactPersonDepartment", "")
        phone_number = contact.get("to_ContactRelationship", {}).get("PhoneNumber", "")
        phone_number_extension = contact.get("to_ContactRelationship", {}).get(
            "PhoneNumberExtension", ""
        )
        email_address = contact.get("to_ContactRelationship", {}).get("EmailAddress", "")

        contact_details.append(
            S4HanaSupplierContact(
                contact_person=contact_person,
                relationship=relationship,
                validity_from=validity_from,
                validity_to=validity_to,
                contact_person_function=(
                    FunctionOfPartner(contact_person_function).name
                    if contact_person_function
                    else ""
                ),
                department=Department(department).name if department else "",
                phone_number=phone_number,
                phone_number_extension=phone_number_extension,
                email_address=email_address,
            )
        )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HanaSupplierContactsResponse(contact_details=contact_details),
    )
