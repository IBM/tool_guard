from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseStatus
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_case_statuses(search: Optional[str] = None) -> List[CaseStatus]:
    """
    Retrieves the list of case status values from Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of case status values from Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")
    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, MasterLabel, SortOrder, CreatedDate FROM CaseStatus {cleaned_clause}"
        )
    )

    results: list[CaseStatus] = []
    for row in rs:
        results.append(
            CaseStatus(
                case_status_id=row.get("Id", ""),
                case_status_name=row.get("MasterLabel", ""),
                sort_order=row.get("SortOrder", ""),
                created_date=row.get("CreatedDate", ""),
            )
        )
    return results
