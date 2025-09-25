from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import RequestException

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class JobApplicant:
    """Represents the details of an applicant for a job requisition in SAP SuccessFactors."""

    application_id: str
    candidate_id: str
    job_requisition_id: str
    applicant_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_number: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


@dataclass
class GetJobApplicantsResponse:
    """A list of applicants for a job requisition in SuccessFactors."""

    applicants: list[JobApplicant]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_all_applicants(job_requisition_id: str) -> GetJobApplicantsResponse:
    """
    Gets a list of applicants for a job requisition in SuccessFactors.

    Args:
        job_requisition_id: The job requisition ID, returned by the `get_job_requisitions` tool.

    Returns:
        A list of applicants for a job requisition.
    """

    try:
        applicants = []
        client = get_sap_successfactors_client()
        response = client.get_request(
            entity="JobApplication",
            filter_expr=f"jobReqId eq {job_requisition_id}",
        )

        results = response.get("d", {}).get("results", [])
        applicants = [
            JobApplicant(
                application_id=applicant.get("applicationId", ""),
                job_requisition_id=job_requisition_id,
                applicant_name=f"{applicant.get("firstName", "")}  {applicant.get("lastName", "")}".strip(),
                contact_email=applicant.get("contactEmail", ""),
                contact_number=applicant.get("cellPhone", ""),
                country=applicant.get("country", ""),
                city=applicant.get("city", ""),
                candidate_id=applicant.get("candidateId", ""),
            )
            for applicant in results
        ]

    except RequestException as e:
        message = f"An unexpected error occurred: {e}"

        return GetJobApplicantsResponse(
            applicants=[],
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            message=message,
        )

    return GetJobApplicantsResponse(applicants=applicants)
