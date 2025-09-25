from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Contract
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_contracts(search: Optional[str] = None) -> list[Contract]:
    """
    Retrieves a list of contracts within Salesforce.

    Args:
        search: The SQL where clause from LLM.

    Returns:
        A list of Contract objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, ContractNumber, AccountId, StartDate, EndDate, Status, Description, ContractTerm FROM Contract {cleaned_clause}"
        )
    )

    results: list[Contract] = []
    for row in rs:
        results.append(
            Contract(
                contract_id=row.get("Id"),
                contract_number=row.get("ContractNumber"),
                account_id=row.get("AccountId"),
                start_date=row.get("StartDate"),
                end_date=row.get("EndDate"),
                status=row.get("Status"),
                description=row.get("Description"),
                contract_term=row.get("ContractTerm"),
            )
        )
    return results
