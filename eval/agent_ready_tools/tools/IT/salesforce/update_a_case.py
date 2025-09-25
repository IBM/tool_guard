from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_a_case(
    case_id: str,
    case_status: Optional[str] = None,
    case_origin: Optional[str] = None,
    case_subject: Optional[str] = None,
    case_type: Optional[str] = None,
    case_reason: Optional[str] = None,
    case_priority: Optional[str] = None,
    case_description: Optional[str] = None,
) -> int:
    """
    Updates an existing case in Salesforce.

    Args:
        case_id: The id of the case to update, returned by the tool `list_cases` in Salesforce
        case_status: The status of the case, returned by the tool `list_case_statuses` in
            Salesforce.
        case_origin: The origin of the case, returned by the tool `list_case_origin` in Salesforce.
        case_subject: The subject of the case in Salesforce..
        case_type: The type of the case, returned by the tool `list_case_type` in Salesforce.
        case_reason: The reason of the case, returned by the tool `list_case_reason` in Salesforce.
        case_priority: The priority of the case, returned by the tool `list_case_priority` in
            Salesforce.
        case_description: The comment of the case in Salesforce.

    Returns:
        The status of the update operation performed on the case.
    """
    client = get_salesforce_client()
    data = {
        "Subject": case_subject,
        "Status": case_status,
        "Origin": case_origin,
        "Type": case_type,
        "Reason": case_reason,
        "Priority": case_priority,
        "Description": case_description,
    }
    # Filter out the blank parameters.
    data = {key: value for key, value in data.items() if value}

    status_code = client.salesforce_object.Case.update(case_id, data)  # type: ignore[operator]

    return status_code
