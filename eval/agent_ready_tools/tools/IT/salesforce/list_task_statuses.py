from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import TaskStatus
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_task_statuses(task_status: Optional[str] = None) -> List[TaskStatus]:
    """
    Retrieves the list of task status values from Salesforce.

    Args:
        task_status: The status of the task in salesforce.

    Returns:
        A list of task status values from Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(
        f"MasterLabel = '{task_status}'" if task_status else ""
    )
    rs = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT MasterLabel FROM TaskStatus {cleaned_clause}")
    )

    results: List[TaskStatus] = []
    for row in rs:
        results.append(TaskStatus(task_status=row.get("MasterLabel", "")))
    return results
