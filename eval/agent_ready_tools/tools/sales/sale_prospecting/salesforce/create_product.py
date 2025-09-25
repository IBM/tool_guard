from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class CreateProductResponse:
    """Represents the result of creating a product in Salesforce."""

    product_id: str


@tool(
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_product(
    product_name: str,
    product_code: Optional[str] = None,
    is_active: Optional[bool] = False,
    description: Optional[str] = None,
) -> CreateProductResponse:
    """
    Creates a product in Salesforce.

    Args:
        product_name: The name of the product in Salesforce.
        product_code: The code for the product in Salesforce.
        is_active: The status of product in Salesforce.
        description: The description of product in Salesforce.

    Returns:
        The result of create operation for a product.
    """
    client = get_salesforce_client()

    payload = {
        "Name": product_name,
        "ProductCode": product_code,
        "IsActive": is_active,
        "Description": description,
    }
    response = client.salesforce_object.Product2.create(data=payload)  # type: ignore[operator]

    return CreateProductResponse(product_id=response.get("id"))
