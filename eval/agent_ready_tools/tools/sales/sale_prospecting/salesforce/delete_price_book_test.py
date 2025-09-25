from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_price_book import (
    delete_price_book,
)


def test_delete_price_book() -> None:
    """Tests that a price book can be deleted successfully by `delete_price_book` tool in
    Salesforce."""

    # Define test data:
    test_data = {"id": "01sfJ000000nEZhQAM", "http_code": 204}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_price_book.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Pricebook2.delete.return_value = test_data["http_code"]

        # Delete a price book
        response = delete_price_book(price_book_id=test_data["id"])

        # Ensure that delete_price_book() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Pricebook2.delete(test_data["id"])
