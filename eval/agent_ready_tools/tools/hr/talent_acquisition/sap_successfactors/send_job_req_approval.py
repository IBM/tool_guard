from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SendJobReqApprovalResponse:
    """Represents the result of the approval of Job requisition in SAP Successfactors."""

    message: str


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def send_job_req_approval(
    job_requisition_id: str,
    comments: Optional[str] = None,
) -> SendJobReqApprovalResponse:
    """
    Sends the job requisition record for approval in SAP Successfactors.

    Args:
        job_requisition_id: The uniquely identifier for the job requisition in SAP Succesfactors, returned by the tool `get_all_job_requisitions`.
        comments: The approval comments for the job requisition in SAP Successfactors.

    Returns:
        The approval message for job requisition.
    """
    try:
        client = get_sap_successfactors_client()

        params: dict[str, Any] = {"jobReqId": f"{job_requisition_id}L", "comments": comments}

        params = {key: value for key, value in params.items() if value}

        response = client.post_request(entity="sendJobReqToNextStep", params=params)

        message = response.get("d", {}).get("sendJobReqToNextStep", "")

        return SendJobReqApprovalResponse(message=message)

    except HTTPError as e:
        error_response = e.response.json() if e.response else None
        error_message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )
        return SendJobReqApprovalResponse(
            message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return SendJobReqApprovalResponse(
            message=str(e),
        )
