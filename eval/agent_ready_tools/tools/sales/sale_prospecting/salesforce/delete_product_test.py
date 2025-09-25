from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_product import delete_product


def test_delete_product() -> None:
    """Test that the `delete_product` function returns the expected response."""

    # Define test data:
    product_id = "01tgL000001pAnxQAE"
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_product.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Product2.delete.return_value = test_response

        # Delete a product
        response = delete_product(product_id)

        # Ensure that delete_product() executed and returned proper values
        assert response
        assert response.http_code == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Product2.delete.assert_called_once_with(product_id)
