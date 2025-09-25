from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderLineItem,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_items import (
    sap_s4_hana_get_purchase_order_items,
)


def test_sap_s4_hana_get_purchase_order_items() -> None:
    """Tests that the purchase order items can be retrieved by the
    `sap_s4_hana_get_purchase_order_items` tool in SAP S4 HANA."""

    # Define test data
    test_data = {
        "value": [
            {
                "PurchaseOrder": "4500000040",
                "PurchaseOrderItem": "10",
                "DocumentCurrency": "EUR",
                "Material": "FG05",
                "OrderQuantity": 4,
                "NetPriceAmount": 50.00,
                "NetAmount": 200.00,
                "Plant": "1010",
            },
            {
                "PurchaseOrder": "4500000040",
                "PurchaseOrderItem": "20",
                "DocumentCurrency": "EUR",
                "Material": "FG11",
                "OrderQuantity": 7,
                "NetPriceAmount": 80.00,
                "NetAmount": 560.00,
                "Plant": "1010",
            },
        ],
    }

    purchase_order_id = "4500000040"

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_items.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {"response": test_data}

        # Call the function
        response: ToolResponse = sap_s4_hana_get_purchase_order_items(purchase_order_id).content

        # Verify that the purchase order items match the expected data
        expected_response = [
            SAPS4HANAPurchaseOrderLineItem(
                purchase_order="4500000040",
                purchase_order_item="10",
                material="FG05",
                order_quantity=4.0,
                net_price_amount=50.0,
                net_amount=200.0,
                document_currency="EUR",
                plant="1010",
            ),
            SAPS4HANAPurchaseOrderLineItem(
                purchase_order="4500000040",
                purchase_order_item="20",
                material="FG11",
                order_quantity=7.0,
                net_price_amount=80.0,
                net_amount=560.0,
                document_currency="EUR",
                plant="1010",
            ),
        ]
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"PurchaseOrder/0001/PurchaseOrder/{purchase_order_id}/_PurchaseOrderItem"
        )
