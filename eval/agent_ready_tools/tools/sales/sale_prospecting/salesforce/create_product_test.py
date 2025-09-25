from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_product import create_product


def test_create_product() -> None:
    """Tests that the `create_product` tool can successfully create a product in Salesforce."""

    # Define test data:
    test_data = {
        "product_name": "New Product",
        "product_code": "",
        "is_active": True,
        "description": "This the description to new product",
        "product_id": "01tfJ000002F3FmQAK",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_product.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Product2.create.return_value = {"id": test_data["product_id"]}

        # Create product
        response = create_product(
            product_name=test_data["product_name"],
            product_code=test_data["product_code"],
            is_active=test_data["is_active"],
            description=test_data["description"],
        )

        # Ensure that create_product() executed and returned proper values
        assert response
        assert response.product_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Product2.create(
            {
                "Name": test_data["product_name"],
                "ProductCode": test_data["product_code"],
                "IsActive": test_data["is_active"],
                "Description": test_data["description"],
            }
        )
