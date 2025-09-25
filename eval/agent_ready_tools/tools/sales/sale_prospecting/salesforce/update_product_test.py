from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_product import update_product


def test_update_product() -> None:
    """Test that the `update_product` function returns the expected response."""

    # Define test data:
    test_data = {
        "product_id": "01tgL000001vgMvQAI",
        "product_code": "PRDT125",
        "product_name": "Product_12_5",
        "description": "Description_UPDATE",
        "product_sku": "PRDT125UP_SKU",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_product.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Product2.update.return_value = test_response

        # Update product
        response = update_product(**test_data)

        # Ensure that update_product() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Product2.update(test_data, test_data["product_id"])
