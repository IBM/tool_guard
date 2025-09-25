from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.create_purchase_order import (
    sap_s4_hana_create_purchase_order,
)


def test_create_purchase_order() -> None:
    """Test that purchase order was created successfully by the sap_s4_hana_create_purchase_order
    tool."""

    # Define test data:
    test_data = {
        "supplier_id": "10200001",
        "company_code": "1010",
        "purchasing_organization": "1010",
        "purchasing_group": "001",
        "international_commercial_terms": "EX_WORKS",
        "material_id": "2000000025",
        "plant": "SE01",
        "purchase_order_quantity_unit": "PC",
        "quantity": 25,
        "net_price": 1275,
        "document_currency": "EUR",
        "purchase_order_id": "4500001955",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.create_purchase_order.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "PurchaseOrder": test_data["purchase_order_id"],
            "Supplier": test_data["supplier_id"],
        }

        response = sap_s4_hana_create_purchase_order(
            supplier_id=test_data["supplier_id"],
            company_code=test_data["company_code"],
            purchasing_organization=test_data["purchasing_organization"],
            purchasing_group=test_data["purchasing_group"],
            international_commercial_terms=test_data["international_commercial_terms"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            purchase_order_quantity_unit=test_data["purchase_order_quantity_unit"],
            quantity=test_data["quantity"],
            net_price=test_data["net_price"],
            document_currency=test_data["document_currency"],
        ).content

        assert response
        assert response.purchase_order_id == test_data["purchase_order_id"]
        assert response.supplier_id == test_data["supplier_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="PurchaseOrder/0001/PurchaseOrder",
            payload={
                "PurchaseOrderType": "NB",
                "Supplier": "10200001",
                "CompanyCode": "1010",
                "IncotermsClassification": "EXW",
                "PurchasingOrganization": "1010",
                "PurchasingGroup": "001",
                "_PurchaseOrderItem": [
                    {
                        "Material": "2000000025",
                        "Plant": "SE01",
                        "PurchaseOrderQuantityUnit": "PC",
                        "OrderQuantity": 25,
                        "NetPriceAmount": 1275,
                        "DocumentCurrency": "EUR",
                    }
                ],
            },
        )
