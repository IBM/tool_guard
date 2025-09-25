from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_product(
    product_id: str,
    product_name: Optional[str] = None,
    product_code: Optional[str] = None,
    description: Optional[str] = None,
    product_sku: Optional[str] = None,
) -> int:
    """
    Updates an existing product in Salesforce.

    Args:
        product_id: The id of product in Salesforce, returned by `list_products_by_name` tool.
        product_name: The name of the product in Salesforce.
        product_code: The code for the product in Salesforce.
        description: The description of product in Salesforce.
        product_sku: The stock keeping unit of a product in Salesforce.

    Returns:
        The status of the update operation performed on the product.
    """
    client = get_salesforce_client()

    payload = {
        "Name": product_name,
        "ProductCode": product_code,
        "Description": description,
        "StockKeepingUnit": product_sku,
    }
    payload = {key: value for key, value in payload.items() if value}
    status_code = client.salesforce_object.Product2.update(product_id, data=payload)  # type: ignore[operator]

    return status_code
