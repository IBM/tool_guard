from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class CompanyInformation:
    """Dataclass representing the company info response from Dnb."""

    duns_number: str = ""
    primary_name: Optional[str] = ""
    operating_status: Optional[Any] = None
    number_of_employees: Optional[Any] = None
    start_date: Optional[str] = ""
    website: Optional[str] = ""
    email: Optional[str] = ""
    telephone: Optional[str] = ""
    address: Optional[Any] = None
    business_activities_info: Optional[Any] = None
    business_entities_type: Optional[Any] = None
    is_small_business: Optional[bool] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_information_l3(duns_number: str) -> ToolResponse[CompanyInformation]:
    """
    Retrieves Data Blocks to customers transactionally based on a request for a given list of DUNS.

    Args:
        duns_number: The company id.

    Returns:
        The list of CompanyInformation from the DnB REST API.
    """

    # Retrieve the DNB client using the helper function.
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")
    # Hard code block_id for company info specifically
    params = {"blockIDs": "companyinfo_L4_v1"}

    # Make the GET request with the DNB Client.
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "duns" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = CompanyInformation(duns_number=org["duns"])

    result.primary_name = org.get("primaryName", "")
    result.operating_status = org.get("localOperatingStatus")
    result.number_of_employees = org.get("numberOfEmployees")
    result.start_date = org.get("startDate", "")
    result.website = org.get("websiteAddress", "")
    result.email = org.get("email", "")
    result.telephone = org.get("telephone", "")
    result.address = org.get("primaryAddress")
    result.business_activities_info = org.get("businessActivitiesInfo")
    result.business_entities_type = org.get("businessEntityType")
    result.is_small_business = org.get("isSmallBusiness")

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
