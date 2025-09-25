from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_price_book import (
    update_price_book,
)


def test_update_pricebook() -> None:
    """Test that the `update_price_book` function returns the expected response."""

    # Define test data:
    test_data: dict = {
        "id": "01sgL000001Rkm9QAC",
        "Name": "Pricebook test",
        "IsActive": True,
        "Description": "This is a test",
    }

    expected = 204

    # Patch `update_price_book` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_price_book.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Pricebook2.update.return_value = expected

        # Update Price book
        response = update_price_book(price_book_id=test_data["id"], name="tes")

        # Ensure that update_price_book() executed and returned proper values
        assert response
        assert response == expected
