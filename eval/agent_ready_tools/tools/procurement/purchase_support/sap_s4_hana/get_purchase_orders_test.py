from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_orders import (
    sap_s4_hana_get_purchase_orders,
)


def test_sap_s4_hana_get_purchase_orders() -> None:
    """Test that the `sap_s4_hana_get_purchase_orders` function returns the expected response."""
    # Define test data:
    test_data = {
        "purchase_order_id": "5100000012",
        "created_by_user": "John Wick",
        "company_code": "1010",
        "purchase_order_type": "NB",
        "date_created": "2018-03-27",
        "purchase_order_date": "2018-04-27",
        "currency": "EUR",
        "payment_terms": "0001",
        "supplier_id": "10300083",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_orders.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "PurchaseOrder": test_data["purchase_order_id"],
                        "CreatedByUser": test_data["created_by_user"],
                        "CompanyCode": test_data["company_code"],
                        "PurchaseOrderType": test_data["purchase_order_type"],
                        "CreationDate": test_data["date_created"],
                        "DocumentCurrency": test_data["currency"],
                        "PurchaseOrderDate": test_data["purchase_order_date"],
                        "PaymentTerms": test_data["payment_terms"],
                        "Supplier": test_data["supplier_id"],
                    },
                ]
            }
        }

        # Get Purchase orders
        response = sap_s4_hana_get_purchase_orders().content

        # Ensure that sap_s4_hana_get_purchase_orders() executed and returned proper values
        assert response
        assert len(response.purchase_orders) == 1
        purchase_order = response.purchase_orders[0]
        assert purchase_order.purchase_order_id == test_data["purchase_order_id"]
        assert purchase_order.created_by_user == test_data["created_by_user"]
        assert purchase_order.company_code == test_data["company_code"]
        assert purchase_order.purchase_order_type == test_data["purchase_order_type"]
        assert purchase_order.date_created == test_data["date_created"]
        assert purchase_order.currency == test_data["currency"]
        assert purchase_order.purchase_order_date == test_data["purchase_order_date"]
        assert purchase_order.supplier_id == test_data["supplier_id"]
        assert purchase_order.payment_terms == test_data["payment_terms"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="/PurchaseOrder/0001/PurchaseOrder",
            filter_expr=None,
            params={"$top": 20, "$skip": 0},
        )


def test_sap_s4_hana_get_purchase_orders_with_supplier() -> None:
    """Test the `sap_s4_hana_get_purchase_orders` function using one of the optional parameter
    supplier."""
    # Define test data:
    test_data = {
        "purchase_order_id": "5100000012",
        "created_by_user": "John Wick",
        "company_code": "1010",
        "purchase_order_type": "NB",
        "date_created": "2018-03-27",
        "purchase_order_date": "2018-04-27",
        "currency": "EUR",
        "payment_terms": "0001",
        "supplier_id": "10300083",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_orders.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "PurchaseOrder": test_data["purchase_order_id"],
                        "CreatedByUser": test_data["created_by_user"],
                        "CompanyCode": test_data["company_code"],
                        "PurchaseOrderType": test_data["purchase_order_type"],
                        "CreationDate": test_data["date_created"],
                        "DocumentCurrency": test_data["currency"],
                        "PurchaseOrderDate": test_data["purchase_order_date"],
                        "PaymentTerms": test_data["payment_terms"],
                        "Supplier": test_data["supplier_id"],
                    },
                ]
            }
        }

        # Get Purchase orders
        response = sap_s4_hana_get_purchase_orders(supplier_id="10300083").content

        # Ensure that sap_s4_hana_get_purchase_orders() executed and returned proper values
        assert response
        assert len(response.purchase_orders) == 1
        purchase_order = response.purchase_orders[0]
        assert purchase_order.purchase_order_id == test_data["purchase_order_id"]
        assert purchase_order.created_by_user == test_data["created_by_user"]
        assert purchase_order.company_code == test_data["company_code"]
        assert purchase_order.purchase_order_type == test_data["purchase_order_type"]
        assert purchase_order.date_created == test_data["date_created"]
        assert purchase_order.currency == test_data["currency"]
        assert purchase_order.purchase_order_date == test_data["purchase_order_date"]
        assert purchase_order.supplier_id == test_data["supplier_id"]
        assert purchase_order.payment_terms == test_data["payment_terms"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="/PurchaseOrder/0001/PurchaseOrder",
            filter_expr=f"Supplier eq '{test_data['supplier_id']}'",
            params={"$top": 20, "$skip": 0},
        )
