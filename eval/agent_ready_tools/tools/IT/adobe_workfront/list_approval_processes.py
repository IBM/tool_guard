from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class ApprovalProcess:
    """Represents a single approval process in Adobe Workfront."""

    approval_process_id: str
    approval_process_name: str
    created_date: str
    is_active: bool


@dataclass
class ListApprovalProcessesResponse:
    """Represents the response for retrieving approval processes in Adobe Workfront."""

    approval_processes: List[ApprovalProcess]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_approval_processes(
    approval_process_name: Optional[str] = None,
    is_active: Optional[bool] = True,
    limit: Optional[int] = 50,
    skip: Optional[int] = 0,
) -> ListApprovalProcessesResponse:
    """
    Gets a list of approval processes from Adobe Workfront.

    Args:
        approval_process_name: The name of the approval processes in Adobe Workfront.
        is_active: The status of the approval processes. If True, only active approval processes are
            retrieved. If False, only inactive approval processes are retrieved.
        limit: The maximum number of approval processes to retrieve in a single API call. Defaults
            to 50. Use this to control the size of the result set.
        skip: The number of approval processes to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of approval processes with approval_process_id, approval_process_name, created_date,
        and active status.
    """

    client = get_adobe_workfront_client()

    params: Dict[str, Any] = {
        "name": approval_process_name,
        "isActive": is_active,
        "$$LIMIT": limit,
        "$$FIRST": skip,
    }
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="arvprc/search", params=params)

    approval_processes: List[ApprovalProcess] = [
        ApprovalProcess(
            approval_process_id=result.get("ID", ""),
            approval_process_name=result.get("name", ""),
            created_date=result.get("entryDate", ""),
            is_active=result.get("isActive", True),
        )
        for result in response.get("data", [])
    ]

    return ListApprovalProcessesResponse(approval_processes=approval_processes)
