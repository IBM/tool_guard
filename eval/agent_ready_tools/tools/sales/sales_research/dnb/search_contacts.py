from dataclasses import field
import re
from typing import Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class Contact:
    """Dataclass representing one search contact response from DnB."""

    full_name: Optional[str] = None  # mapped from fullName
    email: Optional[str] = None  # mapped from email
    social_media: Optional[List[str]] = field(default=None)  # mapped from socialMedia
    job_title: Optional[List[str]] = field(default=None)  # mapped from jobTitles
    vanity_title: Optional[List[str]] = field(default=None)  # mapped from vanityTitles
    duns_number: Optional[str] = None  # mapped from duns
    primary_name: Optional[str] = None  # mapped from primaryName


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def search_contacts(
    duns_number: str,
    search_term: Optional[str] = None,
) -> List[Contact] | ErrorResponse:
    """
    Retrieves contact details based on duns number, and optionally search terms (name, job title
    etc.).

    Args:
        duns_number: a duns number retrieved by the search_company_by_typeahead tool
        search_term: string to search

    Returns:
        a list of contacts objects for the requested company. each object includes:
            - full_name (Optional[str]): The full name of the contact associated to the company. # mapped from fullName
            - email (Optional[str]): The published professional email address for the individual that is specific to their place of employment. # mapped from email
            - social_media (Optional[List[object]]):  The details of the websites and applications that enable the contact to create and share content or to participate in social networking. # mapped from socialMedia
            - job_title (Optional[List[object]]): The professional job role(s) for the individual. # mapped from jobTitles
            - vanity_title (Optional[List[object]]): The details of the highly-formatted version of a contact's Job Title to remove errant characters and to expand on abbreviated titles. # mapped from vanityTitles
            - duns_number (Optional[str]):   identification number assigned by Dun & Bradstreet that uniquely identifies the entity # mapped from duns
            - primary_name (Optional[str]): Single name by which the organization is primarily known or identified. # mapped from primaryName
    """
    search_criteria: Dict[str, object] = {
        "duns": duns_number,
        "searchTerm": search_term,
    }
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    response = client.post_request(
        version="v2",  # The API version.
        category="search",  # The API category.
        endpoint="contact",
        data=search_criteria,
    )
    search_candidates = response.get("searchCandidates", None)

    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v2/search/contact"
    url_params = search_criteria
    error_response = process_dnb_error(response, api_url, url_params)

    contacts_list: List[Contact] = []
    if search_candidates:
        for candidate in search_candidates:
            contact = candidate.get("contact", None)
            social_media_raw = contact.get("socialMedia", None)
            organization = contact.get("organization", None)
            contacts_list.append(
                Contact(
                    full_name=contact.get("fullName"),
                    email=contact.get("email"),
                    social_media=(
                        []
                        if social_media_raw is None
                        else [
                            x["url"]
                            for x in social_media_raw
                            if isinstance(x, dict)
                            and "url" in x
                            and re.search("linkedin", x["url"])
                        ]
                    )
                    or None,  # search and extract linkedin only from social media
                    job_title=[
                        jt["title"]
                        for jt in contact.get("jobTitles", [])
                        if isinstance(jt, dict) and "title" in jt and isinstance(jt["title"], str)
                    ]
                    or None,
                    vanity_title=[
                        vt["title"]
                        for vt in contact.get("vanityTitles", [])
                        if isinstance(vt, dict) and "title" in vt and isinstance(vt["title"], str)
                    ]
                    or None,
                    duns_number=(None if organization is None else organization.get("duns", None)),
                    primary_name=(
                        None if organization is None else organization.get("primaryName", None)
                    ),
                )
            )

    # If there is no contacts_list, then return error_response, else return contacts_list
    if not contacts_list or not isinstance(contacts_list, list):
        return error_response
    else:
        return contacts_list
