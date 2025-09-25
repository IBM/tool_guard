from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DelPricebook:
    """Represents the result of price book deletion in Salesforce."""

    http_code: Optional[int] = None


@tool(permission=ToolPermission.WRITE_ONLY, expected_credentials=SALESFORCE_CONNECTIONS)
def delete_price_book(price_book_id: str) -> DelPricebook:
    """
    Deletes a price book in Salesforce.

    Args:
        price_book_id: The unique id of a price book, returned by 'list_price_books' tool in
            Salesforce.

    Returns:
        Confirmation of the price book deletion.
    """
    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Pricebook2.delete(price_book_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DelPricebook(http_code=http_code)
