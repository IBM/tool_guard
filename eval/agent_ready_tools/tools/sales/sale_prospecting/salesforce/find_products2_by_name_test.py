from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.find_products2_by_name import (
    find_products2_by_name,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Product2


def test_find_products2_by_name() -> None:
    """Test that the `find_products2_by_name` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "01tgL543201p8asCGA",
        "name": "Rubber product",
        "product_code": "PRD 1",
        "description": "Product desc",
    }

    expected = Product2(**test_data)

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.find_products2_by_name.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": "01tgL543201p8asCGA",
                "Name": "Rubber product",
                "ProductCode": "PRD 1",
                "Description": "Product desc",
            }
        ]

        # Get all products by name
        response = find_products2_by_name(search_name="Product")

        # Assertions
        assert response
        assert len(response) == 1
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                "SELECT Name, Id, Description, ProductCode FROM Product2 WHERE Name LIKE '%{:like}%'",
                "Product",
            )
        )
