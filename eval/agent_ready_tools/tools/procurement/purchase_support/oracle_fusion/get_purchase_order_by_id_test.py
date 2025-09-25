from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_purchase_order_by_id import (
    oracle_fusion_get_purchase_order_by_id,
)


def test_oracle_fusion_get_purchase_order_by_id() -> None:
    """Test that the `oracle_fusion_get_purchase_order_by_id` function returns expected purchase
    order details."""

    # Define test data
    purchase_order_id = "300000025673187"
    test_data: Dict[str, Any] = {
        "POHeaderId": 300000025673187,
        "OrderNumber": "US164535",
        "SupplierId": 300000024164123,
        "Supplier": "TEST_SUPP1",
        "SupplierSite": "CHicago",
        "SupplierSiteId": 300000024164155,
        "SupplierContact": "Test contact",
        "SupplierCommunicationMethod": "None",
        "SupplierEmailAddress": None,
        "SupplierCCEmailAddress": None,
        "SupplierBCCEmailAddress": None,
        "SupplierFax": None,
        "Status": "Pending Approval",
        "Ordered": 1.00,
        "Currency": "US Dollar",
        "PurchaseBasis": "GOODS_AND_SERVICES",
        "SoldToLegalEntity": "Virgin Atlantic",
        "ProcurementBU": "US1 Business Unit",
        "BillToBU": "US1 Business Unit",
        "Buyer": "Singh, Saurabh",
        "Requisition": None,
        "TotalTax": 0,
        "ShippingMethod": "UPS",
        "PaymentTerms": "Net 30",
        "ShipToLocationAddress": "411 University Street, Seattle, WA 98101, King, United States",
        "BillToLocationAddress": "500 Oracle Parkway, Redwood City, CA 94065, San Mateo, United States",
        "CreationDate": "2025-08-08T07:26:01+00:00",
        "lines": [
            {
                "POLineId": 300000025673189,
                "LineNumber": 1,
                "Item": "PK101",
                "Description": "Test Product ",
                "Quantity": 1,
                "Total": 1.00,
                "Currency": "US Dollar",
                "PricingUOM": "Ea",
            }
        ],
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_purchase_order_by_id.get_oracle_fusion_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Call the function
        response = oracle_fusion_get_purchase_order_by_id(
            purchase_order_id=purchase_order_id
        ).content

        assert response
        assert response.purchase_order_id == test_data["POHeaderId"]
        assert response.po_number == test_data["OrderNumber"]
        assert response.status == test_data["Status"]
        assert response.ordered_amount == test_data["Ordered"]
        assert response.currency == test_data["Currency"]
        assert response.supplier_name == test_data["Supplier"]
        assert response.shipping_method == test_data["ShippingMethod"]
        assert response.payment_terms == test_data["PaymentTerms"]
        assert response.shipping_address == test_data["ShipToLocationAddress"]
        assert response.billing_address == test_data["BillToLocationAddress"]
        assert response.purchase_order_items[0].item_name == test_data["lines"][0]["Item"]
        assert (
            response.purchase_order_items[0].item_description
            == test_data["lines"][0]["Description"]
        )

        mock_client.get_request.assert_called_once_with(
            resource_name=f"purchaseOrders/{purchase_order_id}", params={"expand": "lines"}
        )
