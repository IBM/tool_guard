from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_price_book import (
    create_price_book,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Pricebook


def test_create_pricebook() -> None:
    """Test that the `create_pricebook` function returns the expected response."""

    # Define test data:
    test_data: dict = {
        "id": "01sgL000001Rkm9QAC",
        "Name": "Pricebook test",
        "IsActive": True,
        "Description": "This is a test",
    }

    expected = Pricebook(
        id=test_data["id"],
        name=test_data["Name"],
        is_active=test_data["IsActive"],
        description=test_data["Description"],
    )

    # Patch `create_pricebook` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_price_book.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Pricebook2.create.return_value = {"id": test_data["id"]}

        # Create Pricebook
        response = create_price_book(
            name=test_data["Name"],
            is_active=test_data["IsActive"],
            description=test_data["Description"],
        )

        # Ensure that create_pricebook() executed and returned proper values
        assert response
        assert response == expected
