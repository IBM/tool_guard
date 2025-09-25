from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class CompanyThirdPartyRiskInsight:
    """Establishes third party risk insights of a company which providesa basic level of risk
    management."""

    duns_number: str = ""

    stability_class_score: Optional[int] = None
    stability_failure_rate: Optional[int] = None
    stability_score_card_id: Optional[str] = ""
    stability_score_date: Optional[str] = ""
    stability_score_model: Optional[str] = ""
    stability_commentary_descriptions: Optional[str] = ""

    evaluation_raw_score: Optional[int] = None
    evaluation_commentary_descriptions: Optional[str] = ""


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_third_party_risk_insight_l1(
    duns_number: str,
) -> ToolResponse[CompanyThirdPartyRiskInsight]:
    """
    Returns the company third party risk insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 1 company third party risk insight.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "thirdpartyriskinsight_L1_v4"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "thirdPartyRiskAssessment" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = CompanyThirdPartyRiskInsight(org.get("duns"))

    # Supplier Stability Index Data
    stability_score_data = org["thirdPartyRiskAssessment"].get("supplierStabilityIndexScore")

    result.stability_class_score = stability_score_data.get("classScore")
    result.stability_failure_rate = stability_score_data.get("failureRate")
    result.stability_score_card_id = stability_score_data.get("scoreCardID", "")
    result.stability_score_date = stability_score_data.get("scoreDate", "")

    score_model = stability_score_data.get("scoreModel")
    if isinstance(score_model, dict):
        result.stability_score_model = score_model.get("description", "")

    stability_commentaries = stability_score_data.get("scoreCommentary", [])
    if isinstance(stability_commentaries, list):
        result.stability_commentary_descriptions = ". ".join(
            [
                item.get("description", "")
                for item in stability_commentaries
                if isinstance(item, dict)
            ]
        )

    # Supplier Evaluation Risk Score Data
    if "supplierEvaluationRiskScore" in org["thirdPartyRiskAssessment"]:
        eval_score_data = org["thirdPartyRiskAssessment"]["supplierEvaluationRiskScore"]

        result.evaluation_raw_score = eval_score_data.get("rawScore")
        # Extract descriptions from commentary
        eval_commentaries = eval_score_data.get("scoreCommentary", [])
        if isinstance(eval_commentaries, list):
            result.evaluation_commentary_descriptions = ". ".join(
                [
                    item.get("description", "")
                    for item in eval_commentaries
                    if isinstance(item, dict)
                ]
            )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
