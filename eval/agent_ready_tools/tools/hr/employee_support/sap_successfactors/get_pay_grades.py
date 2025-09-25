from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class PayGrade:
    """
    Represents a single pay grade record in SAP SuccessFactors.

    An legacy class, which can be used to identify when a job change is a lateral move, a promotion,
    or a demotion.
    """

    code: str
    "external_code"
    name: str
    level: str
    status: str


@dataclass
class PayGradeResponse:
    """Represents all pay_grades records in SAP SuccessFactors."""

    pay_grades: List[PayGrade]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_pay_grades() -> PayGradeResponse:
    """
    Gets the list of pay grades configured for this SAP SuccessFactors deployment.

    Returns:
        A list of pay grades.
    """

    client = get_sap_successfactors_client()
    response = client.get_request(
        entity="FOPayGrade", select_expr="externalCode,paygradeLevel,name,internalCode,status"
    )
    results = response["d"]["results"]

    pay_grades = [
        PayGrade(
            code=record.get("externalCode"),
            name=record.get("name"),
            level=record.get("paygradeLevel"),
            status=record.get("status"),
        )
        for record in results
    ]

    return PayGradeResponse(pay_grades=pay_grades)
