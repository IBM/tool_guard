from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_all_purchase_orders import (
    ariba_get_all_purchase_order_details,
)


def test_ariba_get_all_purchase_order_details() -> None:
    """Verifies the list of PO Buyer was retrieved successfully by
    `ariba_get_all_purchase_order_details`"""

    # Define test data:
    test_data: Dict[str, Any] = {
        "start_date": "2025-04-20T12:00:00",
        "end_date": "2025-04-24T12:00:00",
        "documentNumber": "PO11",
        "supplierName": "IBMInnovation Demo Supplier 2 - TEST",
        "customerName": "IBMInnovationDSAPP",
        "poAmount": {
            "amount": 42.75,
            "currencyCode": "USD",
            "approx": 42.75,
            "conversionDate": "22 Apr 2025 8:17:42 AM",
        },
        "status": "Sent",
        "orderDate": "22 Apr 2025 8:13:10 AM",
        "poShipToCode": "3000",
    }

    # Patch `get_ariba_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_all_purchase_orders.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "content": [
                {
                    "documentNumber": test_data["documentNumber"],
                    "supplierName": test_data["supplierName"],
                    "customerName": test_data["customerName"],
                    "poAmount": test_data["poAmount"],
                    "status": test_data["status"],
                    "orderDate": test_data["orderDate"],
                    "poShipToCode": test_data["poShipToCode"],
                }
            ]
        }

        response = ariba_get_all_purchase_order_details(
            start_date="2025-04-20T12:00:00",
            end_date="2025-04-24T12:00:00",
        ).content

        # Ensure that get_all_purchase_orders() executed and returned proper values

        assert response
        assert response.po_details_result[0].supplier_name == test_data["supplierName"]
        assert response.po_details_result[0].customer_name == test_data["customerName"]
        assert response.po_details_result[0].po_amount == test_data["poAmount"]["amount"]
        assert response.po_details_result[0].po_currency == test_data["poAmount"]["currencyCode"]
        assert response.po_details_result[0].po_status == test_data["status"]
        assert response.po_details_result[0].order_date == test_data["orderDate"]
        assert response.po_details_result[0].po_ship_to_code == test_data["poShipToCode"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="purchase-orders/v1/prod/orders",
            params={
                "$filter": "startDate eq '2025-04-20T12:00:00' and endDate eq '2025-04-24T12:00:00'"
            },
        )
