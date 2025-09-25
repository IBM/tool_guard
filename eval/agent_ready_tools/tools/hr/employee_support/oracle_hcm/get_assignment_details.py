from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleGetworkerworkrelationship:
    """Get's the period_of_service_id from get a worker work relationship api."""

    period_of_service_id: int
    legal_employer_name: str


@dataclass
class OracleGetworkerworkrelationshipResponse:
    """Represents the response from getting a user's worker work relationship details in Oracle
    HCM."""

    worker_work_relationship: List[OracleGetworkerworkrelationship]


@dataclass
class OracleGetworkersassignmentdetails:
    """Represents assignment details of a user in Oracle HCM."""

    assignment_id: int
    assignment_name: str
    assignment_number: str
    primary_flag: bool
    assignment_uniq_id: str
    period_of_service_id: str
    legal_employer_name: str
    action_code: str


@dataclass
class OracleGetworkersassignmentdetailsResponse:
    """Represents the response from getting a user's assignment details in Oracle HCM."""

    user_assignment_details: List[OracleGetworkersassignmentdetails]


def get_worker_work_relationship(worker_id: str) -> OracleGetworkerworkrelationshipResponse:
    """
    Gets the period_of_service_id from get worker work relationship API in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying a worker within the Oracle HCM is returned by
            the `get_user_oracle_ids` tool.

    Returns:
        The user's worker work relationship details.
    """
    client = get_oracle_hcm_client()

    response = client.get_request(
        f"workers/{worker_id}/child/workRelationships",
    )

    worker_work_relationship: list[OracleGetworkerworkrelationship] = []

    for result in response["items"]:
        worker_work_relationship.append(
            OracleGetworkerworkrelationship(
                period_of_service_id=result.get("PeriodOfServiceId", ""),
                legal_employer_name=result.get("LegalEmployerName", ""),
            )
        )
    return OracleGetworkerworkrelationshipResponse(
        worker_work_relationship=worker_work_relationship
    )


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_assignment_details(worker_id: str) -> OracleGetworkersassignmentdetailsResponse:
    """
    Gets a user's assignment details in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying a worker within the Oracle HCM is returned by
            the `get_user_oracle_ids` tool.

    Returns:
        The user's assignment details.
    """
    get_worker_work = get_worker_work_relationship(worker_id).worker_work_relationship[0]
    period_of_service_id = get_worker_work.period_of_service_id
    legal_employer_name = get_worker_work.legal_employer_name

    client = get_oracle_hcm_client()

    response = client.get_request(
        f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments",
        q_expr=f"PrimaryFlag=true",
    )

    user_assignment_details: list[OracleGetworkersassignmentdetails] = []

    for result in response.get("items", ""):
        user_assignment_details.append(
            OracleGetworkersassignmentdetails(
                assignment_id=result.get("AssignmentId", ""),
                assignment_name=result.get("AssignmentName", ""),
                assignment_number=result.get("AssignmentNumber", ""),
                primary_flag=result.get("PrimaryFlag", ""),
                action_code=result.get("ActionCode", ""),
                assignment_uniq_id=get_id_from_links(result.get("links", [])[0].get("href", "")),
                period_of_service_id=str(period_of_service_id),
                legal_employer_name=legal_employer_name,
            )
        )

    return OracleGetworkersassignmentdetailsResponse(
        user_assignment_details=user_assignment_details
    )
