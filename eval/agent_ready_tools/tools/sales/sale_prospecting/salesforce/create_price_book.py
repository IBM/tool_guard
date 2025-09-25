from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Pricebook
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_price_book(name: str, description: str, is_active: bool) -> Pricebook:
    """
    Create a new pricebook in Salesforce.

    Confirm your parameters with the user before creating the pricebook.

    Args:
        name: The pricebook name in Salesforce.
        description: The pricebook description in Salesforce.
        is_active: Indicates whether the price book is active (true) or not (false). Inactive price
            books are hidden in many areas in the user interface. You can change this field’s value
            as often as necessary. Label is Active.

    Returns:
        The created pricebook object.
    """
    client = get_salesforce_client()

    data = {"Name": name, "IsActive": is_active, "Description": description}

    response = client.salesforce_object.Pricebook2.create(data)  # type: ignore[operator]
    pricebook = Pricebook(
        id=response.get("id", ""), name=name, description=description, is_active=is_active
    )

    return pricebook
