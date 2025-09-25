from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Pricebook2
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_price_books(search: Optional[str] = None) -> List[Pricebook2]:
    """
    Returns a list of Pricebook objects based on search parameter in Salesforce.

    Args:
        search: The search parameter to filter the results of price book in Salesforce.

    Returns:
        A list of Pricebook objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(f"SELECT Id, Name, IsActive, Description FROM Pricebook2 {cleaned_clause}")
    )
    results: List[Pricebook2] = []
    for row in rs:
        price_book_id = row.get("Id")
        price_book_name = row.get("Name")
        price_book_is_active = row.get("IsActive")
        price_book_description = row.get("Description")
        results.append(
            Pricebook2(
                id=price_book_id,
                name=price_book_name,
                is_active=price_book_is_active,
                description=price_book_description,
            )
        )

    return results
