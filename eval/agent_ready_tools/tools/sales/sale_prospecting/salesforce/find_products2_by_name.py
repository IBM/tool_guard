from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Product2
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def find_products2_by_name(search_name: str) -> list[Product2]:
    """
    Returns a list of Product objects that match the given name query.

    Args:
        search_name: The name of the product to search for.

    Returns:
        A list of Product objects that match the query.
    """
    client = get_salesforce_client()

    rs = client.salesforce_object.query_all_iter(
        format_soql(
            "SELECT Name, Id, Description, ProductCode FROM Product2 WHERE Name LIKE '%{:like}%'",
            search_name,
        )
    )
    results: list[Product2] = []
    for obj in rs:
        data = {
            "name": obj.get("Name", ""),
            "id": obj.get("Id", ""),
            "description": obj.get("Description", ""),
            "product_code": obj.get("ProductCode", ""),
        }
        results.append(Product2(**data))

    return results
