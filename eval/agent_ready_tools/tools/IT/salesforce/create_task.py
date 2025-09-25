from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class SalesforceCreateTaskResponse:
    """Represents the result of creating a task in Salesforce."""

    task_id: str


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def salesforce_create_task(
    subject: str,
    task_status: str,
    task_priority: str,
    assignee_id: str,
    contact_id: Optional[str] = None,
    due_date: Optional[str] = None,
    description: Optional[str] = None,
) -> SalesforceCreateTaskResponse:
    """
    Creates a task in Salesforce.

    Args:
        subject: The subject of the task in Salesforce.
        task_status: The status of the task returned by `get_task_status` tool.
        task_priority: The priority of the task returned by `get_task_priority` tool.
        assignee_id: The unique identifier of the user is returned by `list_users` tool.
        contact_id: The unique identifier of the contact is returned by `list_contacts` tool.
        due_date: The due date of the task in ISO 8601 format (e.g., YYYY-MM-DD).
        description: The description of the task in Salesforce.

    Returns:
        The result of creating a task.
    """
    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "Subject": subject,
        "Status": task_status,
        "Priority": task_priority,
        "WhoId": contact_id,
        "OwnerId": assignee_id,
        "ActivityDate": due_date,
        "Description": description,
    }
    # Filter out the parameters that are None/Blank
    payload = {key: value for key, value in payload.items() if value}

    response = client.salesforce_object.Task.create(data=payload)  # type: ignore[operator]

    return SalesforceCreateTaskResponse(task_id=response.get("id", ""))
