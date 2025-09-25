from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    Order,
    OrderItem,
)
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_order(
    status: str,
    account_id: str,
    effective_date: str,
    pricebook2_id: str,
    contract_id: str,
    order_items: List[OrderItem],
) -> Order:
    """
    Create a new order in Salesforce. Confirm your parameters with the user before creating the
    order.

    Args:
        status: The order status, returned by the tool `get_order_status` in Salesforce.
        account_id: The account id, returned by the tool `list_accounts` in Salesforce.
        effective_date: The order date should be between the contract dates in Salesforce.
        pricebook2_id: The price book, returned by the tool `list_pricebooks` in Salesforce, with
            the IsActive = true search criteria.
        contract_id: The contract id, returned by the tool `list_contracts` in Salesforce, using the
            AccountId with the same account at the account_id parameter  search criteria .
        order_items: The order item, returned by the tool `list_pricebook_entries` in Salesforce,
            using Pricebook2Id with the same pricebook at the pricebook2_id parameter AND IsActive =
            true search criteria .

    Returns:
        The created order object.
    """
    client = get_salesforce_client()

    data = {
        "attributes": {"type": "Order"},
        "Status": status,
        "EffectiveDate": effective_date,
        "accountId": account_id,
        "Pricebook2Id": pricebook2_id,
        "ContractId": contract_id,
    }

    response = client.salesforce_object.Order.create(data)  # type: ignore[operator]
    order = Order(
        id=response.get("id", ""),
        items=order_items,
        status=status,
        effective_date=effective_date,
        account_id=account_id,
        contract_id=contract_id,
    )
    if order.items:
        for order_item in order.items:

            item_data = {
                "OrderId": order.id,
                "PricebookEntryId": order_item.pricebook_entry_id,
                "Quantity": order_item.quantity,
                "UnitPrice": order_item.unit_price,
            }
            item_result = client.salesforce_object.OrderItem.create(item_data)  # type: ignore[operator]
            order_item.id = item_result.get("id", "")

    return order
