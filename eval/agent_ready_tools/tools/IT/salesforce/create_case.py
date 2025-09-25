from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateCaseResponse:
    """Represents the result of creating a case in Salesforce."""

    case_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_case(
    case_subject: str,
    case_status: str,
    case_origin: str,
    priority: str,
    case_type: Optional[str] = None,
    case_reason: Optional[str] = None,
) -> CreateCaseResponse:
    """
    Creates a case in Salesforce.

    Args:
        case_subject: The subject or name of the case in Salesforce.
        case_status: The status of the case, returned by the tool `list_case_status` in Salesforce.
        case_origin: The origin of the case, returned by the tool `list_case_origin` in Salesforce.
        priority: The priority of the case, returned by the tool `list_case_priority` in Salesforce.
        case_type: The type of the case, returned by the tool `list_case_type` in Salesforce.
        case_reason: The reason of the case, returned by the tool `list_case_reason` in Salesforce.

    Returns:
        The result of performing the creation of a case in Salesforce.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "Subject": case_subject,
        "Type": case_type,
        "Reason": case_reason,
        "Status": case_status,
        "Origin": case_origin,
        "Priority": priority,
    }
    response = client.salesforce_object.Case.create(data=payload)  # type: ignore[operator]
    return CreateCaseResponse(case_id=response.get("id", None))
