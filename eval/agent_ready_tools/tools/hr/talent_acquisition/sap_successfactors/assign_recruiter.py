from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class AssignRecruiterResponse:
    """Represents the response from assigning a job requisition in SAP SuccessFactors."""

    message: Optional[str] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def assign_recruiter_to_job_requisition(
    job_requisition_id: str, recruiter: str
) -> AssignRecruiterResponse:
    """
    Assigns a job requisition to a recruiter in SAP SuccessFactors.

    Args:
        job_requisition_id: The ID of the job requisition in SAP SuccesFactors, returned by the tool `get_job_requisitions`.
        recruiter: The username of the recruiter to assign to the job requisition, returned by `get_user_successfactors_ids` tool.

    Returns:
        A response message indicating the result of the assignment of recruiter.
    """
    try:
        client = get_sap_successfactors_client()
        response = client.get_request(
            entity="reassignJobReq",
            params={"jobReqId": job_requisition_id, "recruiter": recruiter, "$format": "json"},
        )

        result = response.get("d", {}).get("reassignJobReq", "")
        return AssignRecruiterResponse(message=result)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return AssignRecruiterResponse(
            message="",
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            error_message=message,
        )
