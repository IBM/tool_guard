from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_purchase_orders import (
    coupa_get_all_purchase_orders,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaPurchaseOrderList,
)


def test_coupa_get_all_purchase_orders() -> None:
    """Test that the `get_all_purchase_orders` function returns the expected response."""

    # Define test data
    test_data: list[dict[str, Any]] = [
        {
            "id": 4171,
            "po-number": "4171",
            "created-by": {"login": "mjordan"},
            "updated-by": {"login": "mjordan"},
            "created-at": "2025-04-07T12:28:32-07:00",
            "updated-at": "2025-04-11T08:56:23-07:00",
            "status": "issued",
            "transmission-status": "not_sent",
            "exported": False,
            "ship-to-attention": "Meg(CEO) Jordan",
            "payment-method": "invoice",
            "currency": {"code": "USD"},
            "total-with-estimated-tax": "1850.00",
            "supplier": {"name": "Grainger (USA)"},
            "ship-to-address": {
                "street1": "wocfioqaqkcl",
                "city": "wokwbxezqtuu",
                "postal-code": "4388260",
                "state": None,
                "country": {"name": "India"},
            },
            "requisition-header": {
                "id": 5335,
                "created-by": {"login": "mjordan"},
                "updated-by": {"login": "mjordan"},
                "created-at": "2025-02-10T22:59:02-08:00",
                "updated-at": "2025-03-21T12:48:17-07:00",
                "requested-by": {"login": "mjordan", "fullname": "Meg(CEO) Jordan"},
                "status": "partially_received",
                "currency": {"code": "USD"},
                "line-count": 2,
                "total-with-estimated-tax": "10000",
                "department": {"name": None},
                "justification": None,
                "ship-to-address": {"street1": "wocfioqaqkcl"},
                "current-approval": None,
                "approvals": [{"id": 85691}],
                "requisition-lines": [
                    {
                        "id": 9948,
                        "description": "laptop",
                        "unit-price": 1000.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionAmountLine",
                        "line-num": 1,
                        "quantity": None,
                        "supplier": {"id": 9},
                        "account": {"id": 1426},
                        "total-with-estimated-tax": "950.0",
                    },
                    {
                        "id": 9949,
                        "description": "9070xt",
                        "unit-price": 850.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionAmountLine",
                        "line-num": 2,
                        "quantity": None,
                        "supplier": {"id": 9},
                        "account": {"id": 1426},
                        "total-with-estimated-tax": "950.0",
                    },
                ],
            },
            "order-lines": [
                {
                    "id": 6082,
                    "description": "laptop",
                    "type": "OrderAmountLine",
                    "line-num": "1",
                    "item": {"description": None, "uom": {"name": None}},
                    "quantity": None,
                    "price": "1200.00",
                    "total": "1200.00",
                    "received": "0.00",
                    "receipt-approval-required": False,
                },
                {
                    "id": 6083,
                    "description": "9070xt",
                    "type": "OrderAmountLine",
                    "line-num": "2",
                    "item": {"description": None, "uom": {"name": None}},
                    "quantity": None,
                    "price": "850.00",
                    "total": "850.00",
                    "received": "0.00",
                    "receipt-approval-required": False,
                },
            ],
        },
        {
            "id": 4170,
            "po-number": "4170",
            "created-by": {"login": "mjordan"},
            "updated-by": {"login": "mjordan"},
            "created-at": "2025-04-06T16:02:51-07:00",
            "updated-at": "2025-04-11T09:50:02-07:00",
            "status": "issued",
            "transmission-status": "sent_via_email",
            "exported": False,
            "ship-to-attention": "Meg(CEO) Jordan",
            "payment-method": "invoice",
            "currency": {"code": "USD"},
            "total-with-estimated-tax": "17000.00",
            "supplier": {"name": "Apple (USA)"},
            "ship-to-address": {
                "street1": "555 Baily Ave",
                "city": "San Jose",
                "postal-code": "95141",
                "state": "CA",
                "country": {"name": "United States"},
            },
            "requisition-header": {
                "id": 5332,
                "created-by": {"login": "mjordan"},
                "updated-by": {"login": "mjordan"},
                "created-at": "2025-02-10T22:59:02-08:00",
                "updated-at": "2025-03-21T12:48:17-07:00",
                "requested-by": {"login": "mjordan", "fullname": "Meg(CEO) Jordan"},
                "status": "received",
                "currency": {"code": "USD"},
                "line-count": 1,
                "total-with-estimated-tax": "10000",
                "department": {"name": None},
                "justification": None,
                "ship-to-address": {"street1": "555 Baily Ave"},
                "current-approval": None,
                "approvals": [{"id": 85679}],
                "requisition-lines": [
                    {
                        "id": 9946,
                        "description": "MacBook Pro Retina - 15-inch",
                        "unit-price": 1700.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionQuantityLine",
                        "line-num": 1,
                        "quantity": "10.0",
                        "supplier": {"id": 38},
                        "account": {"id": 1540},
                        "total-with-estimated-tax": "950.0",
                    }
                ],
            },
            "order-lines": [
                {
                    "id": 6081,
                    "description": "MacBook Pro Retina - 15-inch",
                    "type": "OrderQuantityLine",
                    "line-num": "1",
                    "item": {"description": None, "uom": {"name": None}},
                    "quantity": "10.0",
                    "price": "1700.00",
                    "total": "17000.00",
                    "received": "0.00",
                    "receipt-approval-required": False,
                }
            ],
        },
    ]

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_purchase_orders.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        # Get all purchase orders (2 most recent)
        response = coupa_get_all_purchase_orders(limit=2).content

        # Ensure that get_all_purchase_orders() executed and returned proper values
        assert isinstance(response, CoupaPurchaseOrderList)
        assert len(response.purchase_order_list) == 2

        assert response.purchase_order_list[0].purchase_order_id == 4171
        assert response.purchase_order_list[0].supplier_name == "Grainger (USA)"
        assert response.purchase_order_list[0].total_with_estimated_tax == "1850.00"

        assert response.purchase_order_list[1].purchase_order_id == 4170
        assert response.purchase_order_list[1].supplier_name == "Apple (USA)"
        assert response.purchase_order_list[1].total_with_estimated_tax == "17000.00"

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="purchase_orders",
            params={
                "limit": 2,
                "offset": 0,
                "order_by": "created-at",
                "dir": "desc",
            },
        )
