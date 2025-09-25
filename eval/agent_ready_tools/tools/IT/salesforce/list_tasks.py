from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Task
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_tasks(search: Optional[str] = None) -> list[Task]:
    """
    Retrieves a list of tasks within Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of tasks objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")
    results: list[Task] = []

    rs = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT Id, Subject, Status, Priority, Description FROM Task {cleaned_clause}")
    )

    for obj in rs:
        results.append(
            Task(
                task_id=obj.get("Id"),
                task_subject=obj.get("Subject"),
                task_status=obj.get("Status"),
                task_priority=obj.get("Priority"),
                task_description=obj.get("Description"),
            )
        )

    return results
