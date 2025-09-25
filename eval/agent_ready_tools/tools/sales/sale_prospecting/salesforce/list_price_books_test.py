from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_price_books import (
    list_price_books,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Pricebook2


def test_list_price_books_without_parameter() -> None:
    """Tests that the `list_price_books` function returns the expected response."""

    # Define test data:
    test_data = [
        Pricebook2(id="01sgL0000019HNdQAM", name="Standard Book 1", is_active=True),
        Pricebook2(id="01sgL000001Rke5QAC", name="Custom Price Book", is_active=True),
    ]

    expected: List[Pricebook2] = test_data  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_price_books.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {"Id": test_data[0].id, "Name": test_data[0].name, "IsActive": test_data[0].is_active},
            {"Id": test_data[1].id, "Name": test_data[1].name, "IsActive": test_data[1].is_active},
        ]

        # List price books
        response = list_price_books("IsActive= True")

        # Ensure that list_price_books() executed and returned proper values
        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Name, IsActive, Description FROM Pricebook2 WHERE IsActive = True"
        )
