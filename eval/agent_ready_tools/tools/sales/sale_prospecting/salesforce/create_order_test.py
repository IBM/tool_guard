from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_order import create_order
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    Order,
    OrderItem,
)


def test_create_order() -> None:
    """Test that the `create_order` function returns the expected response."""

    # Define test data:
    test_data: dict = {
        "attributes": {"type": "Order"},
        "EffectiveDate": "2025-04-26",
        "Status": "Draft",
        "accountId": "001gL000004Zin4QAC",
        "Pricebook2Id": "01sgL0000019HNdQAM",
        "ContractId": "800gL000003nTqLQAU",
        "OrderItems": {
            "records": [
                {
                    "attributes": {"type": "OrderItem"},
                    "PricebookEntryId": "01ugL000000SmT7QAK",
                    "quantity": "2",
                    "UnitPrice": "40000",
                }
            ]
        },
    }

    order_items: List[OrderItem] = [
        OrderItem(
            id="",
            pricebook_entry_id=item["PricebookEntryId"],
            quantity=int(item["quantity"]),
            unit_price=float(item["UnitPrice"]),
        )
        for item in test_data["OrderItems"]["records"]
    ]

    expected = Order(
        id="801gL000005YUyUQAW",
        status=test_data["Status"],
        effective_date=test_data["EffectiveDate"],
        account_id=test_data["accountId"],
        contract_id=test_data["ContractId"],
        items=[
            OrderItem(
                id="802gL000001JM2sQAG",
                pricebook_entry_id="01ugL000000SmT7QAK",
                quantity=2,
                unit_price=40000.0,
            )
        ],
    )

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_order.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Order.create.return_value = {"id": "801gL000005YUyUQAW"}
        mock_client.salesforce_object.OrderItem.create.return_value = {"id": "802gL000001JM2sQAG"}

        # Create Order
        response = create_order(
            status=test_data["Status"],
            account_id=test_data["accountId"],
            effective_date=test_data["EffectiveDate"],
            pricebook2_id=test_data["Pricebook2Id"],
            contract_id=test_data["ContractId"],
            order_items=order_items,
        )

        # Ensure that create_order() executed and returned proper values
        assert response
        assert response == expected
