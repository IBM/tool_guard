from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils import format_tool_input
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class CompanyInfoResponse:
    """Dataclass representing the company info response from Dnb."""

    name: Optional[str] = None
    summary: Optional[List] = None
    number_of_employees: Optional[List[object]] = None
    country: Optional[str] = None
    address: Optional[object] = None
    email: Optional[List[str]] = None
    website: Optional[List[object]] = None
    revenue: Optional[List[object]] = None
    is_small_business: Optional[bool] = None
    is_marketable: Optional[bool] = None
    is_registered_address: Optional[bool] = None
    is_mail_undeliverable: Optional[bool] = None
    is_telephone_disconnected: Optional[bool] = None
    is_delisted: Optional[bool] = None
    is_standalone: Optional[bool] = None


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_company_info(duns_number: str) -> List[CompanyInfoResponse] | ErrorResponse:
    """
    Retrieve detailed company information using DUNS numbers.

    Args:
        duns_number: The duns number.

    Returns:
        The list of CompanyInfoResponses objectfrom the DnB REST API. Each object
        contains:
            - name (str): Single name by which the organization is primarily known or identified.
            - summary (list): The details of the editorial comments for the entity.
            - number_of_employees (list[object]): The details of the number of individuals engaged by a business for various purposes, e.g., to perform its business operations.
            - country (str): The two-letter country code
            - address (object): The details of the organization's official address as recorded with an external authority.
            - email (list[str]): The details of the email address used to contact the entity.
            - website (list[object]): The details of the internet URLs used for online information and communication with the Organization.
            - revenue (list[object]): The details of the standardized summary view of the financial results (actual or estimated) for the organization.
            - is_small_business (bool): Indicates if the business qualifies as small business, eligible for assistance from SBA, with a place of business located in the United States.
            - is_marketable (bool): Indicates whether the data on the organization satisfies Dun & Bradstreet's marketability rules for Sales & Marketing Solutions products.
            - is_registered_address (bool): Indicates if the address is the same as the organization's Registered Address
            - is_mail_undeliverable (bool): Indicates whether it is possible to deliver mail to the address of this entity.
            - is_telephone_disconnected (bool): Indicates whether the telephone number can be connected to successfully.
            - is_delisted (bool): Indicates whether the organization has requested that they not be included in any Direct marketing lists (e.g., mail, telephone, email).
            - is_standalone (bool): Indicates if the entity is a member of a legal family tree.
    """

    # Retrieve the DNB client using the helper function.
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    # Hard code block_id for company info specifically
    block_id = "companyinfo_L2_v1"

    # Convert duns input to list
    duns_numbers_list: List[str] = format_tool_input.string_to_list_of_strings(duns_number)

    company_info_responses = []
    for dun_number_str in duns_numbers_list:
        # Make the GET request with the DNB Client.
        response = client.get_request(
            version="v1",  # The API version.
            category="data",  # The API category.
            endpoint="duns",  # The command endpoint.
            path_parameter=dun_number_str,  # path parameters
            params={"blockIDs": block_id},  # block_id parameter
        )

        company_info_organization = response.get("organization", None)
        if company_info_organization is not None:
            company_info_global_ultimate = company_info_organization.get("globalUltimate", {})
            company_info_duns_control_status = company_info_organization.get(
                "dunsControlStatus", {}
            )
            company_info_primary_address = company_info_organization.get("primaryAddress", {})
        else:
            company_info_global_ultimate = {}
            company_info_duns_control_status = {}
            company_info_primary_address = {}

        # Check if we have an error in the response.
        api_url = "https://plus.dnb.com/v1/data/duns"
        url_params = {"blockIDs": block_id}
        error_response = process_dnb_error(response, api_url, url_params)

        # Attempt to construct and append the CompanyInfoResponse object only if company_info_organization not None
        if company_info_organization:

            company_info_responses.append(
                CompanyInfoResponse(
                    name=company_info_organization.get("primaryName", None),
                    summary=company_info_organization.get("summary", None),
                    number_of_employees=(
                        []
                        if company_info_global_ultimate is None
                        else company_info_global_ultimate.get("numberOfEmployees", None)
                    ),
                    country=company_info_organization.get("countryISOAlpha2Code", None),
                    address=company_info_organization.get("registeredAddress", None),
                    email=company_info_organization.get("email", None),
                    website=company_info_organization.get("websiteAddress", None),
                    revenue=company_info_organization.get("financials", None),
                    is_small_business=company_info_organization.get("isSmallBusiness", False),
                    is_marketable=company_info_duns_control_status.get("isMarketable", False),
                    is_registered_address=company_info_primary_address.get(
                        "isRegisteredAddress", False
                    ),
                    is_mail_undeliverable=company_info_duns_control_status.get(
                        "isMailUndeliverable", False
                    ),
                    is_telephone_disconnected=company_info_duns_control_status.get(
                        "isTelephoneDisconnected", False
                    ),
                    is_delisted=company_info_duns_control_status.get("isDelisted", False),
                    is_standalone=company_info_organization.get("isStandalone", None),
                )
            )
    # If there is no company_info_responses, then return error_response, else return company_info_responses
    if not company_info_responses or not isinstance(company_info_responses, list):
        return error_response
    else:
        return company_info_responses
