from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_MANAGER_CONNECTIONS


@dataclass
class ApproveTimeOffTimeEntriesResponse:
    """Represents the response from approving a user's time off and time entries in Workday."""

    descriptor: str


statuses = {
    "approval": "approval",
    "approve": "approval",
    "approved": "approval",
    "denial": "denial",
    "denied": "denial",
    "reject": "denial",
    "rejected": "denial",
}


@tool(expected_credentials=WORKDAY_MANAGER_CONNECTIONS)
def approve_time_off_and_time_entries(
    pending_request_id: str, request_response: str, comment: str
) -> ApproveTimeOffTimeEntriesResponse:
    """
    Approve an employee's time off and time entry requests in Workday.

    Args:
        pending_request_id: The pending time off or time entry request id.
        request_response: The response to the request. Acceptable values are: 'approval' or
            'denial'.
        comment: The request payload containing the comment for managing time off and time entry
            request.

    Returns:
        The JSON response from the Workday API.
    """

    normalized_request_response = statuses.get(request_response.lower(), "")
    # Should request_response not be found in Statuses, let the agent/user know what the correct input should be.
    assert (
        normalized_request_response
    ), f"request_response parameter, '{request_response}' must be either 'approval' or 'denial'."

    # requires manager credentials
    client = get_workday_client(access_level=AccessLevel.MANAGER)
    response = client.approve_time_off_and_time_entries(
        pending_request_id=pending_request_id,
        request_response=normalized_request_response,
        payload={"comment": comment},
    )
    return ApproveTimeOffTimeEntriesResponse(
        descriptor=response["descriptor"],
    )
