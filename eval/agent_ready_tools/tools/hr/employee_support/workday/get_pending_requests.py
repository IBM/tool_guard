from typing import Optional

from dateutil import parser  # type: ignore[import-untyped]
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_MANAGER_CONNECTIONS


@dataclass
class PendingRequests:
    """Represents a get pending requests in Workday."""

    pending_request_id: str
    description: str
    subject: str
    due_date: str
    initiator: Optional[str]
    over_all_process: str
    assigned_date: str
    status: str


@dataclass
class PendingRequestsResponse:
    """Represents the response from getting pending requests in Workday."""

    pending_requests: list[PendingRequests]


@tool(expected_credentials=WORKDAY_MANAGER_CONNECTIONS)
def get_pending_requests(user_id: str) -> PendingRequestsResponse:
    """
    Gets a user's pending requests in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The user's pending requests.
    """
    # requires manager creds
    client = get_workday_client(access_level=AccessLevel.MANAGER)

    url = f"api/common/v1/{client.tenant_name}/workers/{user_id}/inboxTasks"
    response = client.get_request(url=url)

    pending_requests: list[PendingRequests] = []
    for report in response["data"]:

        assigned_date = str(parser.parse(report.get("assigned")).date())

        initiator = None
        if report.get("initiator") is not None:
            initiator = report.get("initiator").get("descriptor")

        pending_requests.append(
            PendingRequests(
                pending_request_id=report.get("id"),
                description=report.get("descriptor"),
                subject=report.get("subject").get("descriptor") if report.get("subject") else "",
                due_date=report.get("due"),
                over_all_process=report.get("overallProcess").get("descriptor"),
                initiator=initiator,
                assigned_date=assigned_date,
                status=report.get("status").get("descriptor"),
            )
        )
    return PendingRequestsResponse(pending_requests=pending_requests)
