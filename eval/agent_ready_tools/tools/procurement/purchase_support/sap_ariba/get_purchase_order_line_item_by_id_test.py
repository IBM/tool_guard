from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_purchase_order_line_item_by_id import (
    ariba_get_purchase_order_line_items_by_po_id,
)


def test_get_ariba_purchase_order_line_item_by_id() -> None:
    """Test that the `get_ariba_purchase_order_line_item_by_id` function returns the expected
    response."""

    # Define test data:
    test_data = {
        "order_line_id": "PO16",
        "order_line_description": "Test order line item PO11 description",
        "order_line_type": "",
        "order_line_num": 1,
        "item_description": "Test item description",
        "part_type": None,
        "quantity": 2,
        "total": 0,
        "supplier_part_number": "AD1513",
        "manufacturer_name": "Hallmark Cables",
        "manufacturer_part_number": "AD1415",
        "need_by_date": "31 May 2025 3:30:00 AM",
        "street": "691 Broadway",
        "postal_code": "10001",
        "state": "NY",
        "country": "USA",
    }

    # Patch `get_ariba_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_ariba.get_purchase_order_line_item_by_id.get_ariba_client"
    ) as mock_ariba_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ariba_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "content": [
                {
                    "documentNumber": test_data["order_line_id"],
                    "lineNumber": test_data["order_line_num"],
                    "description": test_data["order_line_description"],
                    "quantity": test_data["quantity"],
                    "supplierPart": test_data["supplier_part_number"],
                    "unitPrice": {
                        "amount": 34,
                        "currencyCode": "USD",
                        "approx": 34,
                        "conversionDate": "25 Apr 2025 8:13:12 AM",
                    },
                    "manufacturerName": {
                        "encryptedValue": "Hallmark Cables",
                        "kid": None,
                        "value": "Hallmark Cables",
                    },
                    "manufacturerPartId": test_data["manufacturer_part_number"],
                    "needBy": test_data["need_by_date"],
                    "itemShipToStreet": "691 Broadway",
                    "itemShipToCity": "NEW YORK",
                    "itemShipToPostalCode": "10001",
                    "itemShipToState": "NY",
                    "itemShipToCountry": "USA",
                }
            ]
        }

        # Get purchase order line item by ID
        response = ariba_get_purchase_order_line_items_by_po_id(
            purchase_order_id=test_data["order_line_id"]
        ).content

        assert response
        assert len(response.order_lines) == 1
        order_line_details = response.order_lines[0]
        assert order_line_details.order_line_id == "PO16-1"
        assert order_line_details.total != "1"
        assert order_line_details.address == test_data["street"]
        assert order_line_details.supplier_part_number == test_data["supplier_part_number"]
        assert order_line_details.order_line_description == test_data["order_line_description"]
        assert order_line_details.address == test_data["street"]
        assert order_line_details.supplier_part_number == test_data["supplier_part_number"]
        assert order_line_details.order_line_description == test_data["order_line_description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="purchase-orders/v1/prod/items",
            params={"$filter": f"documentNumber eq '{test_data['order_line_id']}'"},
        )
