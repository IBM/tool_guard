"""Tests for the 3-way matching functionality."""

from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_support.coupa.three_way_matching_batch import (
    coupa_batch_three_way_matching,
)


def test_batch_three_way_matching_success() -> None:
    """Test successful batch 3-way matching when all documents match."""

    test_data = {
        "invoice_ids": [713514, 713515],
        "po_ids": [4187, 4188],
    }

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.three_way_matching_batch.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        # Mock responses for multiple invoices
        mock_client.get_request.side_effect = [
            # Invoice 1
            {
                "id": test_data["invoice_ids"][0],
                "status": "pending_receipt",
                "total-with-taxes": "1550.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4909,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "po-number": str(test_data["po_ids"][0]),
                        "order-line-id": 6105,
                    },
                ],
            },
            # PO 1
            {
                "id": test_data["po_ids"][0],
                "po-number": str(test_data["po_ids"][0]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "1550.00",
                "order-lines": [
                    {
                        "id": 6105,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1234,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "1550.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
            # Invoice 2
            {
                "id": test_data["invoice_ids"][1],
                "status": "pending_receipt",
                "total-with-taxes": "800.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4910,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "po-number": str(test_data["po_ids"][1]),
                        "order-line-id": 6106,
                    },
                ],
            },
            # PO 2
            {
                "id": test_data["po_ids"][1],
                "po-number": str(test_data["po_ids"][1]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "800.00",
                "order-lines": [
                    {
                        "id": 6106,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1235,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "800.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
        ]

        # Mock receipts lists for both POs
        mock_client.get_request_list.side_effect = [
            # Receipts for PO 1
            [{"id": 10596}],
            # Receipts for PO 2
            [{"id": 10597}],
        ]

        # Mock individual receipt responses
        mock_client.get_request.side_effect = [
            # Invoice 1
            {
                "id": test_data["invoice_ids"][0],
                "status": "pending_receipt",
                "total-with-taxes": "1550.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4909,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "po-number": str(test_data["po_ids"][0]),
                        "order-line-id": 6105,
                    },
                ],
            },
            # PO 1
            {
                "id": test_data["po_ids"][0],
                "po-number": str(test_data["po_ids"][0]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "1550.00",
                "order-lines": [
                    {
                        "id": 6105,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1234,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "1550.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
            # Receipt 1 for PO 1
            {
                "id": 10596,
                "status": "received",
                "price": "1050.00",
                "quantity": "1.0",
                "total": "1050.00",
                "order-line": {"id": 6105},
                "account": {
                    "id": 1001,
                    "account-type": {
                        "id": 99,
                        "currency": {"id": 1, "code": "USD", "decimals": 2},
                        "active": True,
                        "dynamic-flag": False,
                    },
                },
            },
            # Invoice 2
            {
                "id": test_data["invoice_ids"][1],
                "status": "pending_receipt",
                "total-with-taxes": "800.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4910,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "po-number": str(test_data["po_ids"][1]),
                        "order-line-id": 6106,
                    },
                ],
            },
            # PO 2
            {
                "id": test_data["po_ids"][1],
                "po-number": str(test_data["po_ids"][1]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "800.00",
                "order-lines": [
                    {
                        "id": 6106,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1235,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "800.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
            # Receipt 2 for PO 2
            {
                "id": 10597,
                "status": "received",
                "price": "400.00",
                "quantity": "2.0",
                "total": "800.00",
                "order-line": {"id": 6106},
                "account": {
                    "id": 1001,
                    "account-type": {
                        "id": 99,
                        "currency": {"id": 1, "code": "USD", "decimals": 2},
                        "active": True,
                        "dynamic-flag": False,
                    },
                },
            },
        ]

        response = coupa_batch_three_way_matching(test_data["invoice_ids"])
        result = response.content
        assert result
        assert result.total_invoices == 2
        assert result.successful_matches == 2
        assert result.blocked_matches == 0
        assert result.error_matches == 0
        assert len(result.results) == 2
        assert "2 approved" in result.summary

        # Check individual results
        assert result.results[0].invoice_id == test_data["invoice_ids"][0]
        assert result.results[0].overall_status == "APPROVED"
        assert result.results[1].invoice_id == test_data["invoice_ids"][1]
        assert result.results[1].overall_status == "APPROVED"


def test_batch_three_way_matching_mixed_results() -> None:
    """Test batch 3-way matching with mixed results (some approved, some blocked, some errors)."""

    test_data = {
        "invoice_ids": [713514, 713515, 713516],
        "po_ids": [4187, 4188, 4189],
    }

    with patch(
        "agent_ready_tools.tools.procurement.invoice_support.coupa.three_way_matching_batch.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        # Mock responses for multiple invoices
        mock_client.get_request.side_effect = [
            # Invoice 1 (will be approved)
            {
                "id": test_data["invoice_ids"][0],
                "status": "pending_receipt",
                "total-with-taxes": "1550.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4909,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "po-number": str(test_data["po_ids"][0]),
                        "order-line-id": 6105,
                    },
                ],
            },
            # PO 1
            {
                "id": test_data["po_ids"][0],
                "po-number": str(test_data["po_ids"][0]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "1550.00",
                "order-lines": [
                    {
                        "id": 6105,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1234,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "1550.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
            # Invoice 2 (will be blocked - no receipts)
            {
                "id": test_data["invoice_ids"][1],
                "status": "pending_receipt",
                "total-with-taxes": "800.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4910,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "po-number": str(test_data["po_ids"][1]),
                        "order-line-id": 6106,
                    },
                ],
            },
            # PO 2
            {
                "id": test_data["po_ids"][1],
                "po-number": str(test_data["po_ids"][1]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "800.00",
                "order-lines": [
                    {
                        "id": 6106,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1235,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "800.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
        ]

        # Mock receipts lists
        mock_client.get_request_list.side_effect = [
            [{"id": 10596}],
            [],
        ]

        # Mock individual receipt responses
        mock_client.get_request.side_effect = [
            # Invoice 1
            {
                "id": test_data["invoice_ids"][0],
                "status": "pending_receipt",
                "total-with-taxes": "1550.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4909,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "po-number": str(test_data["po_ids"][0]),
                        "order-line-id": 6105,
                    },
                ],
            },
            # PO 1
            {
                "id": test_data["po_ids"][0],
                "po-number": str(test_data["po_ids"][0]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "1550.00",
                "order-lines": [
                    {
                        "id": 6105,
                        "description": "macbook pro",
                        "quantity": "1.0",
                        "price": "1050.00",
                        "total": "1050.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1234,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "1550.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
            # Receipt 1 for PO 1
            {
                "id": 10596,
                "status": "received",
                "price": "1050.00",
                "quantity": "1.0",
                "total": "1050.00",
                "order-line": {"id": 6105},
                "account": {
                    "id": 1001,
                    "account-type": {
                        "id": 99,
                        "currency": {"id": 1, "code": "USD", "decimals": 2},
                        "active": True,
                        "dynamic-flag": False,
                    },
                },
            },
            # Invoice 2
            {
                "id": test_data["invoice_ids"][1],
                "status": "pending_receipt",
                "total-with-taxes": "800.00",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "invoice-lines": [
                    {
                        "id": 4910,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "po-number": str(test_data["po_ids"][1]),
                        "order-line-id": 6106,
                    },
                ],
            },
            # PO 2
            {
                "id": test_data["po_ids"][1],
                "po-number": str(test_data["po_ids"][1]),
                "status": "issued",
                "currency": {"id": 1, "code": "USD", "decimals": 2},
                "total-with-estimated-tax": "800.00",
                "order-lines": [
                    {
                        "id": 6106,
                        "description": "keyboard",
                        "quantity": "2.0",
                        "price": "400.00",
                        "total": "800.00",
                        "type": "OrderQuantityLine",
                    },
                ],
                "created-by": {"login": "test"},
                "updated-by": {"login": "test"},
                "requisition-header": {
                    "id": 1235,
                    "created-at": "2024-01-01T00:00:00Z",
                    "updated-at": "2024-01-01T00:00:00Z",
                    "created-by": {"login": "test"},
                    "updated-by": {"login": "test"},
                    "requested-by": {"login": "test"},
                    "status": "approved",
                    "currency": {"id": 1, "code": "USD", "decimals": 2},
                    "line-count": 1,
                    "total-with-estimated-tax": "800.00",
                    "requisition-lines": [],
                },
                "supplier": {"id": 1, "name": "test"},
                "ship-to-address": {"street1": "test"},
            },
        ]

        response = coupa_batch_three_way_matching(test_data["invoice_ids"])
        result = response.content

        assert result
        assert result.total_invoices == 3
        assert result.successful_matches == 1
        assert result.blocked_matches == 1
        assert result.error_matches == 1
        assert len(result.results) == 3
        assert "1 approved, 1 blocked, 1 errors" in result.summary

        # Check individual results
        assert result.results[0].invoice_id == test_data["invoice_ids"][0]
        assert result.results[0].overall_status == "APPROVED"
        assert result.results[1].invoice_id == test_data["invoice_ids"][1]
        assert result.results[1].overall_status == "BLOCKED"
        assert result.results[2].invoice_id == test_data["invoice_ids"][2]
        assert result.results[2].overall_status == "error"


def test_batch_three_way_matching_empty_list() -> None:
    """Test batch 3-way matching with an empty list of invoice IDs."""

    response = coupa_batch_three_way_matching([])

    assert response.success is True
    result = response.content

    assert result.total_invoices == 0
    assert result.successful_matches == 0
    assert result.blocked_matches == 0
    assert result.error_matches == 0
    assert len(result.results) == 0
    assert "0 approved" in result.summary
