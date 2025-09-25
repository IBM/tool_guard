from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_price_book(
    price_book_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> int:
    """
    Create a price book in Salesforce. Confirm your parameters with the user before creating the
    price book.

    Args:
        price_book_id: The id of the price book, returned by the tool `list_price_books` in
            Salesforce.
        name: The price book name in Salesforce.
        description: The price book description in Salesforce.
        is_active: Indicates whether the price book is active (true) or not (false). Inactive price
            books are hidden in many areas in the user interface. You can change this field’s value
            as often as necessary. Label is Active.

    Returns:
        The status of the update operation performed on the pricebook.
    """
    client = get_salesforce_client()

    data = {}
    if name is not None:
        data["Name"] = name
    if is_active is not None:
        data["IsActive"] = str(is_active).lower()
    if description is not None:
        data["Description"] = description

    response = client.salesforce_object.Pricebook2.update(price_book_id, data)  # type: ignore[operator]
    return response
