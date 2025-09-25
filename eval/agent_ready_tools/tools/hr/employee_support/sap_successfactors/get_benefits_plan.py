from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class Benefit:
    """Represents a benefit plan in SAP SuccessFactors."""

    effective_start_date: str
    external_name: Optional[str]
    currency: Optional[str]
    amount: Optional[str]


@dataclass
class BenefitsPlanResponse:
    """Represents the response from getting a user's benefits plan in SAP SuccessFactors."""

    benefits: List[Benefit]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_benefits_plan(user_id: str) -> BenefitsPlanResponse:
    """
    Gets a user's benefit plan in SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.

    Returns:
        The user's enrolled benefits.
    """
    client = get_sap_successfactors_client()

    response = client.get_request("BenefitEnrollment", filter_expr=f"workerId eq '{user_id}'")

    benefits: list[Benefit] = []
    for result in response["d"]["results"]:
        benefits.append(
            Benefit(
                external_name=result.get("externalName"),
                effective_start_date=(sap_date_to_iso_8601(result.get("effectiveStartDate"))),
                currency=result.get("currency"),
                amount=result.get("amount"),
            )
        )
    return BenefitsPlanResponse(benefits=benefits)
