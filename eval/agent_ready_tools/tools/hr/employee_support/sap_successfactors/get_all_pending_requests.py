from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client


@dataclass
class GetPendingEmployee:
    """Represents the details of a single pending request for a user in SAP SuccessFactors."""

    wf_request_id: str
    status: str
    request_type: str
    user_id: str
    created_on: str


@dataclass
class GetAllPendingRequestResponse:
    """A list of pending approvals for employees configured in a SuccessFactors deployment."""

    pending_requests: list[GetPendingEmployee]


def get_all_pending_requests(user_id: str) -> GetAllPendingRequestResponse:
    """
    Gets a list of pending approvals for employees configured in this SuccessFactors deployment.

    Args:
        user_id: The employee's user ID uniquely identifies them within the SuccessFactors API for
            retrieving any pending approval requests.

    Returns:
        A list of pending approvals.
    """

    client = get_sap_successfactors_client()
    response = client.get_request(
        entity="WfRequest",
        filter_expr=f"status eq 'PENDING' and empWfRequestNav/jobInfoNav/userId eq '{user_id}'",
        expand_expr="empWfRequestNav,empWfRequestNav/jobInfoNav,empWfRequestNav/jobInfoNav/userNav",
    )
    results = response["d"]["results"]
    pending_requests_list = [
        GetPendingEmployee(
            wf_request_id=pending.get("wfRequestId"),
            status=pending.get("status"),
            request_type=pending.get("empWfRequestNav").get("requestType"),
            user_id=pending.get("empWfRequestNav")
            .get("jobInfoNav")
            .get("results")[0]
            .get("userId"),
            created_on=pending.get("createdOn"),
        )
        for pending in results
    ]
    return GetAllPendingRequestResponse(pending_requests=pending_requests_list)
