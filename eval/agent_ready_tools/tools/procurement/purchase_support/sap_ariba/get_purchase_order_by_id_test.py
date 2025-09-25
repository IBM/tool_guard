from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_purchase_order_by_id import (
    ariba_get_purchase_order_details_by_id,
)


def test_ariba_get_purchase_order_details_by_id() -> None:
    """Test the `ariba_get_purchase_order_details_by_id` function returns the expected response."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "documentNumber": "PO12",
        "supplierName": "IBMInnovation Demo Supplier 2 - TEST",
        "customerName": "IBMInnovationDSAPP",
        "poAmount": {"amount": 42.75, "currencyCode": "USD"},
        "created": "22 Apr 2025 8:17:41 AM",
        "ordered": "22 Apr 2025 8:17:41 AM",
        "status": "Sent",
        "poShipToStreet": "691 Broadway",
        "poShipToCity": "NEW YORK",
        "poShipToState": "NY",
    }

    # Patch `get_ariba_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_purchase_order_by_id.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "limit": 10,
            "totalPages": 1,
            "count": 1,
            "content": [
                {
                    "documentNumber": test_data["documentNumber"],
                    "supplierName": test_data["supplierName"],
                    "supplierANID": "AN01503434985-T",
                    "customerName": test_data["customerName"],
                    "customerANID": "AN01479140833-T",
                    "poAmount": test_data["poAmount"],
                    "created": test_data["created"],
                    "status": test_data["status"],
                    "dashboardStatus": "PO_NEW",
                    "numberOfInvoices": 0,
                    "isRelease": "N",
                    "documentStatus": "Unconfirmed",
                    "payloadId": "1745335061189.1689695571.000002230@KJmTadSmCarnc3zdKZchanicn5A=",
                    "poVersion": 1,
                    "orderDate": test_data["ordered"],
                    "attachmentCount": 0,
                    "poShipToName": {"encryptedValue": "New York", "value": "New York"},
                    "revision": "Original",
                    "poShipToStreet": test_data["poShipToStreet"],
                    "poShipToCity": test_data["poShipToCity"],
                    "poShipToState": test_data["poShipToState"],
                    "poShipToPostalCode": "10001",
                    "poShipToCountry": "United States",
                    "poShipToCode": "3000",
                    "settlement": "PCard",
                    "paymentTerms": ["2% 30 NET 45", "3% 20 NET 45"],
                }
            ],
            "offset": 0,
        }

        response = ariba_get_purchase_order_details_by_id(
            purchase_order_num=test_data["documentNumber"]
        ).content
        assert response
        assert response.purchase_order_num == test_data["documentNumber"]
        assert response.supplier_name == test_data["supplierName"]
        assert response.customer_name == test_data["customerName"]
        assert response.po_amount == test_data["poAmount"]["amount"]
        assert response.po_currency == test_data["poAmount"]["currencyCode"]
        assert response.po_status == test_data["status"]
        assert response.created_date == test_data["created"]
        assert response.order_date == test_data["ordered"]
        assert response.po_ship_to_street == test_data["poShipToStreet"]
        assert response.po_ship_to_city == test_data["poShipToCity"]
        assert response.po_ship_to_state == test_data["poShipToState"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="purchase-orders/v1/prod/orders",
            params={"$filter": f"documentNumber eq '{test_data["documentNumber"]}'"},
        )
