from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_order(
    order_id: str,
    owner_id: Optional[str] = None,
    status: Optional[str] = None,
    account_id: Optional[str] = None,
    effective_date: Optional[str] = None,
    pricebook2_id: Optional[str] = None,
    contract_id: Optional[str] = None,
) -> int:
    """
    Update an order in Salesforce.

    Args:
        order_id: The ID of the order to update.
        owner_id: The order owner, returned by the tool `list_users`, with the IsActive = true
            search criteria. in Salesforce.
        status: The order status, returned by the tool `get_order_status` in Salesforce.
        account_id: The account id, returned by the tool `list_accounts` in Salesforce.
        effective_date: The order date should be between the contract dates in Salesforce.
        pricebook2_id: The price book, returned by the tool `list_pricebooks` in Salesforce, with
            the IsActive = true search criteria.
        contract_id: The contract id, returned by the tool `list_contracts` in Salesforce, using the
            AccountId with the same account at the account_id parameter  search criteria .

    Returns:
        The status of the update operation performed on the order.
    """
    client = get_salesforce_client()

    data = {}

    if owner_id:
        data["OwnerId"] = owner_id
    if status:
        data["Status"] = status
    if account_id:
        data["AccountId"] = account_id
    if effective_date:
        data["EffectiveDate"] = effective_date
    if pricebook2_id:
        data["Pricebook2Id"] = pricebook2_id
    if contract_id:
        data["ContractId"] = contract_id

    response = client.salesforce_object.Order.update(order_id, data)  # type: ignore[operator]
    return response
