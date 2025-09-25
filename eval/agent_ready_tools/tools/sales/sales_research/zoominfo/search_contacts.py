from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.zoominfo_client import get_zoominfo_client
from agent_ready_tools.tools.sales.sales_research.zoominfo.zoominfo_schemas import (
    ErrorResponse,
    ZoominfoContact,
)
from agent_ready_tools.utils.tool_credentials import ZOOMINFO_CONNECTIONS


@tool(expected_credentials=ZOOMINFO_CONNECTIONS)
def zoominfo_search_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    company_id: Optional[str] = None,
    company_name: Optional[str] = None,
    job_title: Optional[str] = None,
    management_level: Optional[str] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    address: Optional[str] = None,
    zip_code: Optional[str] = None,
    zipcode_radius_miles: Optional[str] = None,
) -> List[ZoominfoContact] | ErrorResponse:
    """
    Retrieves contact information based on specific search fields from Zoominfo API.

    Args:
        first_name: First name of the contact.
        last_name: Last name of the contact.
        email: Email address of the contact.
        company_id: ZoomInfo unique identifier for the company.
        company_name: Company Name.
        job_title: Contact title at current place of employment.
        management_level: Contact management level at current place of employment.
        country: Country for the company's primary address.
        state: Company state (U.S.) or province (Canada).
        address: address of the company.
        zip_code: Zip Code of the company's primary address.
        zipcode_radius_miles: Used in conjunction with zipCode, designates a geographical radius (in miles) from the zipCode provided.

    Returns:
        A list of contacts objects returned from the search. Each object includes:
            - person_id [str]: The Zoominfo ID of a contact.
            - first_name [str]: The first name of the contact.
            - last_name [str]: The last name of the contact.
            - has_email [bool]: Indicates whether ZoomInfo has an email address for the contact.
    """
    client = get_zoominfo_client()

    if all(p is None for p in [country, state, address, zip_code]):
        location_search_type = None
    else:
        location_search_type = "Person"  # Default to search on person's location, if any of the location related parameters are requested.

    response = client.post_request(
        category="search",
        endpoint="contact",
        data={
            "firstName": first_name,
            "lastName": last_name,
            "emailAddress": email,
            "companyId": company_id,
            "companyName": company_name,
            "jobTitle": job_title,
            "managementLevel": management_level,
            "country": country,
            "state": state,
            "address": address,
            "zipCode": zip_code,
            "zipCodeRadiusMiles": zipcode_radius_miles,
            "locationSearchType": location_search_type,
        },
    )
    if "error" not in response:
        contacts_data = response.get("data", None)

        results: list[ZoominfoContact] = []
        if contacts_data:
            for contact in contacts_data:
                company_data = contact.get("company", None)
                has_email = contact.get("hasEmail", False)
                if has_email:
                    results.append(
                        ZoominfoContact(
                            person_id=contact.get("id", None),
                            first_name=contact.get("firstName", ""),
                            last_name=contact.get("lastName", ""),
                            job_title=contact.get("jobTitle", ""),
                            company_name=(
                                ""
                                if len(company_data) == 0 or company_data is None
                                else company_data.get("name", "")
                            ),
                            has_email=contact.get("hasEmail", None),
                        )
                    )
        return results
    else:
        return ErrorResponse(message=response.get("error"), status_code=response.get("statusCode"))
