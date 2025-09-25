from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    PriceBookEntry,
)
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_price_book_entries(search: Optional[str] = None) -> List[PriceBookEntry]:
    """
    Returns a list of Price book Entry objects representing all price book entries in the Salesforce
    org.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Price book Entries objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Product2Id, Product2.Name, UnitPrice FROM PricebookEntry {cleaned_clause}"
        )
    )
    results: List[PriceBookEntry] = []
    for row in rs:
        pricebook_entry_id = row.get("Id")
        pricebook_entry_product_id = row.get("Product2Id")
        pricebook_entry_product_name = row.get("Product2").get("Name")
        pricebook_entry_unit_price = row.get("UnitPrice")
        results.append(
            PriceBookEntry(
                id=pricebook_entry_id,
                product_id=pricebook_entry_product_id,
                product_name=pricebook_entry_product_name,
                unit_price=pricebook_entry_unit_price,
            )
        )
    return results
