from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Case
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_cases(search: Optional[str] = None) -> list[Case]:
    """
    Searches for Salesforce cases using a SQL query with zero, one, or more of the optional
    filters: ID, name, access level, creation date.

    Args:
        search: The SQL where clause, passed in from the LLM, with zero, one, or more of the optional filters, namely ID, name, access level, creation date.

    Returns:
        A list of cases from Salesforce.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    response = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Subject, CaseNumber, AccountId, OwnerId, CreatedDate FROM Case {cleaned_clause}"
        )
    )

    results: list[Case] = []
    for case in response:
        results.append(
            Case(
                case_id=case.get("Id"),
                case_name=case.get("Subject"),
                case_number=case.get("CaseNumber"),
                account_id=case.get("AccountId"),
                owner_id=case.get("OwnerId"),
                created_date=case.get("CreatedDate", ""),
            )
        )
    return results
