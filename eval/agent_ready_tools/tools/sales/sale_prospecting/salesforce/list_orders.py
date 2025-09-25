from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Order
from agent_ready_tools.utils.sql_utils import format_where_input_string
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def list_orders(search: Optional[str] = None) -> list[Order]:
    """
    Retrieves a list of orders from Salesforce.

    Args:
        search: The SQL where clause from LLM (to clean up).

    Returns:
        A list of Order objects.
    """
    client = get_salesforce_client()
    cleaned_clause = format_where_input_string(search or "")

    response = client.salesforce_object.query_all_iter(
        format_soql(
            f"SELECT Id, Status, EffectiveDate, AccountId, ContractId, OrderNumber, TotalAmount FROM Order {cleaned_clause}"
        )
    )

    orders: list[Order] = []
    for record in response:
        orders.append(
            Order(
                id=record.get("Id", ""),
                status=record.get("Status", ""),
                effective_date=record.get("EffectiveDate"),
                account_id=record.get("AccountId", ""),
                contract_id=record.get("ContractId"),
                order_number=record.get("OrderNumber", ""),
                order_amount=record.get("TotalAmount"),
            )
        )

    return orders
