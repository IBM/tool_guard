from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.create_purchase_order import (
    oracle_fusion_create_purchase_order,
)


def test_oracle_fusion_create_purchase_order() -> None:
    """Tests oracle_fusion_create_purchase_order using a mock client."""

    test_data = {
        "procurement_business_unit_id": 300000002168484,
        "requisitioning_business_unit": "US1 Business Unit",
        "buyer_email": "Singh, Saurabh",
        "currency_code": "USD",
        "pay_on_receipt": False,
        "buyer_managed_transport": True,
        "supplier_id": 300000010011003,
        "supplier_site_id": 300000010011025,
        "special_handling_type_code": "ORA_PO_BILL_ONLY",
        "default_ship_to_location_id": 300000006267076,
        "purchase_order_id": 300000025813403,
        "purchase_order_number": "US164571",
        "procurement_business_unit": "US1 Business Unit",
        "currency": "US Dollar",
        "supplier": "United Parcel Service",
        "supplier_site": "UPS US1",
        "special_handling_type": "Bill Only",
        "default_ship_to_location": "Riverbed Technology Pte. Ltd.",
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.create_purchase_order.get_oracle_fusion_client"
    ) as mock_oracle_client:
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "POHeaderId": test_data["purchase_order_id"],
            "OrderNumber": test_data["purchase_order_number"],
            "ProcurementBU": test_data["procurement_business_unit"],
            "RequisitioningBU": test_data["requisitioning_business_unit"],
            "BuyerEmail": test_data["buyer_email"],
            "Currency": test_data["currency"],
            "Supplier": test_data["supplier"],
            "SupplierSite": test_data["supplier_site"],
            "SpecialHandlingType": test_data["special_handling_type"],
            "DefaultShipToLocation": test_data["default_ship_to_location"],
        }

        response = oracle_fusion_create_purchase_order(
            procurement_business_unit_id=test_data["procurement_business_unit_id"],
            requisitioning_business_unit=test_data["requisitioning_business_unit"],
            buyer_email=test_data["buyer_email"],
            currency_code=test_data["currency_code"],
            pay_on_receipt=test_data["pay_on_receipt"],
            buyer_managed_transport=test_data["buyer_managed_transport"],
            supplier_id=test_data["supplier_id"],
            supplier_site_id=test_data["supplier_site_id"],
            special_handling_type_code=test_data["special_handling_type_code"],
            default_ship_to_location_id=test_data["default_ship_to_location_id"],
        ).content

        assert response
        assert response.purchase_order_id == test_data["purchase_order_id"]
        assert response.purchase_order_number == test_data["purchase_order_number"]

        mock_client.post_request.assert_called_once_with(
            resource_name=f"draftPurchaseOrders",
            payload={
                "ProcurementBUId": test_data["procurement_business_unit_id"],
                "RequisitioningBU": test_data["requisitioning_business_unit"],
                "BuyerEmail": test_data["buyer_email"],
                "CurrencyCode": test_data["currency_code"],
                "PayOnReceiptFlag": test_data["pay_on_receipt"],
                "BuyerManagedTransportFlag": test_data["buyer_managed_transport"],
                "SupplierId": test_data["supplier_id"],
                "SupplierSiteId": test_data["supplier_site_id"],
                "SpecialHandlingTypeCode": test_data["special_handling_type_code"],
                "DefaultShipToLocationId": test_data["default_ship_to_location_id"],
            },
        )
