from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteProductResponse:
    """Represents the deletion of the product in Salesforce."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def delete_product(
    product_id: str,
) -> DeleteProductResponse:
    """
    Delete a product in Salesforce.

    Args:
        product_id: The id of the product, returned by the `find_products2_by_name` tool.

    Returns:
        The status of the delete operation.
    """
    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Product2.delete(product_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DeleteProductResponse(http_code)
