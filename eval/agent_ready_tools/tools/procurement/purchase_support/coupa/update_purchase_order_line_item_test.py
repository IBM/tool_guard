from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_by_id_test import (
    mock_purchase_order_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.update_purchase_order_line_item import (
    coupa_update_purchase_order_line_item,
)


def test_coupa_update_purchase_order_line_item() -> None:
    """Test that `update_purchase_order_line_item` returns True for successful update."""

    # Define test data:
    test_po_id = 4152
    test_line_num = 1
    test_order_line_id = 6072
    test_update_payload: dict[str, Any] = {
        "order-lines": [
            {
                "id": test_order_line_id,
                "description": "Updated description",
                "quantity": "10",
                "price": "50.00",
                "item": {"description": "Laptop", "uom": {"name": "EA"}},
                "source-part-num": "SPN123",
                "supp-aux-part-num": "SAPN456",
                "commodity": {"name": "Hardware"},
                "manufacturer-name": "Dell",
                "manufacturer-part-number": 7890,
                "need-by-date": "2025-05-01",
                "savings-pct": 10.0,
                "account": {"id": 1001},
                "period": {"name": "Q2"},
            }
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.update_purchase_order_line_item.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request_list.return_value = [{"id": test_order_line_id}]
        mock_client.put_request.return_value = mock_purchase_order_response()

        # Update purchase order line item
        result = coupa_update_purchase_order_line_item(
            purchase_order_id=test_po_id,
            line_num=test_line_num,
            order_line_description="Updated description",
            item_description="Laptop",
            quantity="10",
            unit="EA",
            price="50.00",
            need_by_date="2025-05-01",
            supplier_part_number="SPN123",
            supplier_auxiliary_part_number="SAPN456",
            commodity="Hardware",
            savings_percent=10.0,
            manufacturer_name="Dell",
            manufacturer_part_number=7890,
            billing_account_id=1001,
            period="Q2",
        ).content

        # Ensure that update_purchase_order_line_item() executed and returned the correct response
        assert result.purchase_order_id == test_po_id

        # Ensure the API call was made with expected parameters and payload
        mock_client.get_request_list.assert_called_once_with(
            "purchase_order_lines",
            params={
                "order-header[po-number]": test_po_id,
                "fields": '["id"]',
                "line-num": test_line_num,
            },
        )

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            f"purchase_orders/{test_po_id}",
            payload=test_update_payload,
        )
