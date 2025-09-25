from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_all_purchase_orders import (
    oracle_fusion_get_all_purchase_orders,
)


def test_oracle_fusion_get_all_purchase_orders() -> None:
    """Test the getting of all purchase orders from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "POHeaderId": 8675309,
                "OrderNumber": "US10000",
                "Description": "Test PO",
                "Supplier": "Test supplier",
                "Ordered": 230.78,
                "Currency": "US Dollar",
                "Status": "Open",
                "CreationDate": "2025-07-28T010:30:00.666+00:00",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_all_purchase_orders.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_all_purchase_orders()

        assert response
        assert response.content[0].purchase_order_id == test_result["items"][0]["POHeaderId"]
        assert response.content[0].po_number == test_result["items"][0]["OrderNumber"]

        mock_client.get_request.assert_called_once_with(
            resource_name="purchaseOrders",
            params={"limit": 10, "offset": 0},
        )


def test_oracle_fusion_get_purchase_orders_for_supplier() -> None:
    """Test the getting of all purchase orders from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "POHeaderId": 8675309,
                "OrderNumber": "US10000",
                "Description": "Test PO",
                "Supplier": "I Got It Inc.",
                "Ordered": 230.78,
                "Currency": "US Dollar",
                "Status": "Open",
                "CreationDate": "2025-07-28T010:30:00.666+00:00",
            }
        ]
    }

    test_data = {"supplier_name": "Test supplier"}

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_all_purchase_orders.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_all_purchase_orders(supplier_name=test_data["supplier_name"])

        assert response
        assert response.content[0].purchase_order_id == test_result["items"][0]["POHeaderId"]
        assert response.content[0].po_number == test_result["items"][0]["OrderNumber"]

        mock_client.get_request.assert_called_once_with(
            resource_name="purchaseOrders",
            params={"limit": 10, "offset": 0, "q": f"Supplier={test_data["supplier_name"]}"},
        )
