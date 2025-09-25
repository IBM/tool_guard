from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class FinancialStrength:
    """Represents a financial strength of a company."""

    duns_number: str
    primary_name: str
    financial_condition: Optional[str] = None
    failure_score: Optional[int] = None
    failure_score_description: Optional[str] = None
    delinquency_score: Optional[int] = None
    delinquency_score_description: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_financial_strength(duns_number: str) -> ToolResponse[FinancialStrength]:
    """
    Returns company's financial condition, failure score, and delinquency score.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 financial strength.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "financialstrengthinsight_L1_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "dnbAssessment" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = FinancialStrength(org.get("duns"), org.get("primaryName"))

    assessment = response["organization"]["dnbAssessment"]

    result.financial_condition = assessment.get("financialCondition", {}).get("description")
    result.failure_score = assessment.get("failureScore", {}).get("classScore")
    result.failure_score_description = assessment.get("failureScore", {}).get(
        "classScoreDescription"
    )
    result.delinquency_score = assessment.get("delinquencyScore", {}).get("classScore")
    result.delinquency_score_description = assessment.get("delinquencyScore", {}).get(
        "classScoreDescription"
    )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
