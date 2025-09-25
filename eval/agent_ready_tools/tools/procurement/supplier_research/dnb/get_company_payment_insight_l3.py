from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class CompanyPaymentInsight:
    """Represents company payment insight of a company."""

    duns_number: str
    paydex_score: Optional[int] = None
    three_months_prior_paydex_score: Optional[str] = None
    total_experiences_amount: Optional[float] = None
    average_high_credit_amount: Optional[float] = None
    maximum_past_due_amount: Optional[int] = None
    maximum_owed_amount: Optional[int] = None
    maximum_high_credit_amount: Optional[float] = None
    negative_experiences_amount: Optional[float] = None
    negative_payments_count: Optional[float] = None
    slow_experiences_amount: Optional[float] = None
    slow_experiences_count: Optional[int] = None
    slow_or_negative_payments_count: Optional[int] = None
    placed_for_collection_amount: Optional[str] = None
    average_owing_amount: Optional[str] = None
    total_past_due_amount: Optional[str] = None
    total_past_due_experiences_count: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_payment_insight_l3(duns_number: str) -> ToolResponse[CompanyPaymentInsight]:
    """
    Returns the company's financial insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 3 financial insight.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "paymentinsight_L3_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    # Build the CompanyInfoResponse object for return
    org = response.get("organization")

    if org is None or "businessTrading" not in org and len(org["businessTrading"]) > 0:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = CompanyPaymentInsight(duns_number=org["duns"])

    result.total_experiences_amount = org["businessTrading"][0]["summary"][0].get(
        "totalExperiencesAmount"
    )
    result.average_high_credit_amount = org["businessTrading"][0]["summary"][0].get(
        "averageHighCreditAmount"
    )
    result.maximum_past_due_amount = org["businessTrading"][0]["summary"][0].get(
        "maximumPastDueAmount"
    )
    result.maximum_owed_amount = org["businessTrading"][0]["summary"][0].get("maximumOwedAmount")
    result.paydex_score = org["businessTrading"][0]["summary"][0].get("paydexScore")
    result.three_months_prior_paydex_score = org["businessTrading"][0]["summary"][0].get(
        "threeMonthsPriorPaydexScore"
    )
    result.maximum_high_credit_amount = org["businessTrading"][0]["summary"][0].get(
        "maximumHighCreditAmount"
    )
    result.negative_experiences_amount = org["businessTrading"][0]["summary"][0].get(
        "negativeExperiencesAmount"
    )
    result.negative_payments_count = org["businessTrading"][0]["summary"][0].get(
        "negativePaymentsCount"
    )
    result.slow_experiences_amount = org["businessTrading"][0]["summary"][0].get(
        "slowExperiencesAmount"
    )
    result.slow_experiences_count = org["businessTrading"][0]["summary"][0].get(
        "slowExperiencesCount"
    )
    result.slow_or_negative_payments_count = org["businessTrading"][0]["summary"][0].get(
        "slowOrNegativePaymentsCount"
    )
    result.placed_for_collection_amount = org["businessTrading"][0]["summary"][0].get(
        "placedForCollectionAmount"
    )
    result.average_owing_amount = org["businessTrading"][0]["summary"][0].get("averageOwingAmount")
    result.total_past_due_amount = org["businessTrading"][0]["summary"][0].get("totalPastDueAmount")
    result.total_past_due_experiences_count = org["businessTrading"][0]["summary"][0].get(
        "totalPastDueExperiencesCount"
    )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
