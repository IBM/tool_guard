from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.get_po_receipts import (
    coupa_get_purchase_order_receipts,
)


def test_coupa_get_po_receipts() -> None:
    """Test that the coupa_get_purchase_order_receipts function returns expected receipt IDs."""
    test_po_id = 4187
    mock_response = [
        {
            "id": 10596,
            "created-at": "2025-05-01T15:03:53-07:00",
            "price": "1050.00",
            "quantity": "1.0",
            "total": "1050.00",
            "type": "ReceivingQuantityConsumption",
            "status": "created",
            "order-line": {
                "id": 6105,
                "description": "macbook pro",
                "line-num": "1",
                "order-header-id": 4187,
                "price": "1050.00",
                "quantity": "1.0",
                "status": "received",
            },
        },
        {
            "id": 10597,
            "created-at": "2025-05-01T15:04:17-07:00",
            "price": "250.00",
            "quantity": "1.0",
            "total": "250.00",
            "type": "ReceivingQuantityConsumption",
            "status": "created",
            "order-line": {
                "id": 6106,
                "description": "mouse",
                "line-num": "2",
                "order-header-id": 4187,
                "price": "250.00",
                "quantity": "2.0",
                "status": "received",
            },
        },
        {
            "id": 10598,
            "created-at": "2025-05-01T15:13:37-07:00",
            "price": "250.00",
            "quantity": "1.0",
            "total": "250.00",
            "type": "ReceivingQuantityConsumption",
            "status": "created",
            "order-line": {
                "id": 6106,
                "description": "mouse",
                "line-num": "2",
                "order-header-id": 4187,
                "price": "250.00",
                "quantity": "2.0",
                "status": "received",
            },
        },
    ]

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_po_receipts.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_request_list.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = coupa_get_purchase_order_receipts(test_po_id).content

        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0].order_id == test_po_id
        assert result[1].order_id == test_po_id
        assert result[2].order_id == test_po_id
