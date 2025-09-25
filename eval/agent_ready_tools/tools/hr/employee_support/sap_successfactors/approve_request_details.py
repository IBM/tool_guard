from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client


@dataclass
class ApproveRequestDetailsResponse:
    """Represents the result of approving or rejecting a user's pending request in SAP
    SuccessFactors."""

    status: str


def approve_request_details(workflow_request_id: str, status: str) -> ApproveRequestDetailsResponse:
    """
    approves the user request details in SAP SuccessFactors.

    Args:
        workflow_request_id: The workflow request ID uniquely identifies pending requests within the
            SuccessFactors API for approval returned by the tool `get_all_pending_requests`.
        status: The status is for approving or rejecting the pending termination.

    Returns:
        The result from approving the pending termination details.
    """

    client = get_sap_successfactors_client()
    if status.lower() == "approve":
        entity_type = "approveWfRequest"
    elif status.lower() == "reject":
        entity_type = "rejectWfRequest"
    else:
        raise ValueError(f"Invalid status: {status}, valid status are approve and reject")

    response = client.post_request(
        entity=entity_type,
        params={"wfRequestId": f"{workflow_request_id}L"},
    )
    if "d" in response:
        return ApproveRequestDetailsResponse(status=response["d"][0]["status"])
    else:
        raise ValueError(f"Unexpected response format: {response}")
