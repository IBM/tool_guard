from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class TagCandidateResponse:
    """Represents the result of `tag_candidate_for_specific_job` in SAP SuccessFactors."""

    message: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def tag_candidate_for_specific_job(
    job_requisition_id: str,
    candidate_id: str,
) -> TagCandidateResponse:
    """
    Tags a candidate for a specific job requisition in SAP SuccessFactors.

    Args:
        job_requisition_id: The job requisition id, returned by `get_job_requisitions` tool.
        candidate_id: The candidate id, returned by `get_all_candidates` tool.

    Returns:
        The result from performing the upsert operation of tag a candidate for specific job.
    """
    try:
        client = get_sap_successfactors_client()

        # The 'status' field indicates the tagging status of the candidate for the job requisition where 'Default' is typically used to represent a standard or initial tagging state in Successfactors

        payload = {
            "__metadata": {"uri": "JobReqFwdCandidates", "type": "SFOData.JobReqFwdCandidates"},
            "jobReqId": job_requisition_id,
            "candidateId": candidate_id,
            "status": "Default",
        }

        response = client.post_request(entity="JobReqFwdCandidates", payload=payload)
        http_code = response["http_code"]
        return TagCandidateResponse(http_code=http_code)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return TagCandidateResponse(
            message=message,
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )
