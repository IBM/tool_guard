from http import HTTPStatus
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class ApproveJobRequisitionResponse:
    """Represents the result of the approval of Job requisition in SAP Successfactors."""

    message: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def approve_a_new_job_requisition(
    job_requisition_id: str,
    comments: Optional[str] = None,
) -> ApproveJobRequisitionResponse:
    """
    Approves a job requisition in SAP SuccessFactors, filtered by hiring manager userSysId.

    Args:
        job_requisition_id: The job requisition ID which need to get approval returned by the tool `get_all_job_requisitions`.
        comments: The approval comments for the job requisition in SAP Successfactors.

    Returns:
        The approval message for job requisition.
    """
    try:
        client = get_sap_successfactors_client()

        params: dict[str, Any] = {
            "jobReqId": f"{job_requisition_id}L",
            "comments": comments,
            "actionType": "'APPROVE'",
        }

        params = {key: value for key, value in params.items() if value}

        response = client.post_request(entity="approveOrDeclineJobReqForm", params=params)

        result = response.get("d", {})

        return ApproveJobRequisitionResponse(message=result.get("approveOrDeclineJobReqForm", ""))

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return ApproveJobRequisitionResponse(
            message=message,
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )
