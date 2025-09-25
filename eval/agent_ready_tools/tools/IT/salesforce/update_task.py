from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_task(
    task_id: str,
    task_subject: Optional[str] = None,
    assignee_id: Optional[str] = None,
    task_priority: Optional[str] = None,
    task_activity_date: Optional[str] = None,
    task_status: Optional[str] = None,
    task_contact_id: Optional[str] = None,
    task_description: Optional[str] = None,
    task_related_to_account: Optional[str] = None,
) -> int:
    """
    Updates an existing task in Salesforce.

    Args:
        task_id: The id of the task in Salesforce returned by the `list_tasks` tool.
        task_subject: The subject of the task in Salesforce.
        assignee_id: The unique identifier of the user is returned by `list_users` tool
        task_priority: The priority of the task in Salesforce returned by the tool
            `list_task_priority`.
        task_activity_date: The activity date of the task in Salesforce ISO 8601 format (Eg. YYYY-
            MM-DD).
        task_status: The status of the task in Salesforce returned by the tool `list_task_status`.
        task_contact_id: The contact name in the task in Salesforce returned by the tool
            `list_contacts`.
        task_description: The comment of the task in Salesforce.
        task_related_to_account: The account id related to task in Salesforce returned by the tool
            `list_accounts`.

    Returns:
        The status of the update operation performed on the task.
    """
    client = get_salesforce_client()
    data = {
        "WhoId": task_contact_id,
        "WhatId": task_related_to_account,
        "Subject": task_subject,
        "ActivityDate": task_activity_date,
        "Status": task_status,
        "OwnerId": assignee_id,
        "Priority": task_priority,
        "Description": task_description,
    }
    data = {key: value for key, value in data.items() if value}
    status = client.salesforce_object.Task.update(task_id, data)  # type: ignore[operator]

    return status
