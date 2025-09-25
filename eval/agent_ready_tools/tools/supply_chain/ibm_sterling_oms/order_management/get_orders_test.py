from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.supply_chain.ibm_sterling_oms.order_management.get_orders import (
    sterling_oms_get_orders,
)

TEST_ORDERS = [
    {
        "id": "20250418135903670531",
        "OrderNo": "OM1000001",
        "OrderDate": "2025-04-18T14:02:57+00:00",
        "DocumentType": "0001",
        "ShipToID": "CUST_1000886",
        "MaxOrderStatusDesc": "Shipped",
        "OriginalTotalAmount": "0.00",
        "PaymentStatus": "PAID",
    },
    {
        "id": "20250421135130692525",
        "OrderNo": "OM1000006",
        "OrderDate": "2025-04-21T13:52:19+00:00",
        "DocumentType": "0001",
        "ShipToID": "CUST_1000798",
        "MaxOrderStatusDesc": "Shipped",
        "OriginalTotalAmount": "0.00",
        "PaymentStatus": "AWAIT_PAY_INFO",
    },
    {
        "id": "20250421173341696549",
        "OrderNo": "OM1000008",
        "OrderDate": "2025-04-21T17:34:31+00:00",
        "DocumentType": "0001",
        "ShipToID": "100000109",
        "MaxOrderStatusDesc": "Backordered",
        "OriginalTotalAmount": "0.00",
        "PaymentStatus": "PAID",
    },
]


def test_get_orders() -> None:
    """Test get item supplies using a mock client."""

    with patch(
        "agent_ready_tools.tools.supply_chain.ibm_sterling_oms.order_management.get_orders.get_sterling_oms_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = TEST_ORDERS

        response = sterling_oms_get_orders().content

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="order",
            params={"MaximumRecords": "10"},
        )
