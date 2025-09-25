from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class InitiatePromotionResults:
    """Represents the result of an initiate promotion operation in SAP SuccessFactors."""

    message: str


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def initiate_promotion_sap(
    user_id: str,
    start_date: str,
    job_code: str,
    pay_grade: Optional[str] = None,
) -> InitiatePromotionResults:
    """
    Initiates a promotion request for a user in SAP SuccessFactors.

    Args:
        user_id: The user id uniquely identifying the user within SAP SuccessFactors.
        start_date: The effective start date for the business title update in ISO 8601 format (e.g.,
            YYYY-MM-DD).
        job_code: The new job code of the user as returned by `get_job_codes` tool.
        pay_grade: The new pay grade for the employee as returned by `get_pay_grades` tool.

    Returns:
        The result from performing the upsert operation on the user's business title.
    """

    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "EmpJob"},
        "userId": user_id,
        "startDate": iso_8601_to_sap_date(start_date),
        "jobCode": job_code,
        "payGrade": pay_grade,
    }
    response = client.upsert_request(payload=payload)
    return InitiatePromotionResults(message=response["d"][0]["message"])
