from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class SeniorPrincipal:
    """Represents name of the CEO."""

    title: str
    name: str


@dataclass
class CompanyPrincipalsResponse:
    """represents company principals."""

    duns_number: str
    principals: Optional[list[SeniorPrincipal]] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_principals_l1(duns_number: str) -> ToolResponse[CompanyPrincipalsResponse]:
    """
    Returns the company name of CEO.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 principals and contacts insight.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "principalscontacts_L1_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "mostSeniorPrincipals" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = CompanyPrincipalsResponse(duns_number=org["duns"])

    result.principals = []
    for p in org.get("mostSeniorPrincipals", []):
        for j in p.get("jobTitles", []):
            result.principals.append(SeniorPrincipal(name=p.get("fullName"), title=j.get("title")))

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
