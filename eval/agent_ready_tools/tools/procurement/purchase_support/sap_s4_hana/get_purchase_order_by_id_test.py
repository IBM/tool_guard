from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderDetails,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_by_id import (
    sap_s4_hana_get_purchase_order_by_id,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_sap_s4_hana_get_purchase_order_by_id() -> None:
    """Tests that the purchase order details can be retrieved by the
    `sap_s4_hana_get_purchase_order_by_id` tool in SAP S4 HANA."""

    test_data: dict[str, Any] = {
        "PurchaseOrder": "4500000001",
        "PurchaseOrderType": "NB",
        "CreatedByUser": "MROY",
        "CreationDate": "2017-11-08",
        "PurchaseOrderDate": "2017-11-08",
        "Supplier": "10200001",
        "CompanyCode": "1010",
        "PurchasingOrganization": "1010",
        "PurchasingGroup": "001",
        "PaymentTerms": "0001",
        "DocumentCurrency": "EUR",
        "ExchangeRate": 1.00000,
    }

    purchase_order_id = test_data["PurchaseOrder"]

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_by_id.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {"response": test_data}

        # Call the function
        response = sap_s4_hana_get_purchase_order_by_id(purchase_order_id).content

        # Verify that the purchase order details match the expected data
        expected_response = SAPS4HANAPurchaseOrderDetails(
            purchase_order_number=test_data["PurchaseOrder"],
            purchase_order_type=test_data["PurchaseOrderType"],
            created_by=test_data["CreatedByUser"],
            creation_date=sap_date_to_iso_8601(test_data["CreationDate"]),
            purchase_order_date=sap_date_to_iso_8601(test_data["PurchaseOrderDate"]),
            supplier=test_data["Supplier"],
            company_code=test_data["CompanyCode"],
            purchasing_organization=test_data["PurchasingOrganization"],
            purchasing_group=test_data["PurchasingGroup"],
            payment_terms=test_data["PaymentTerms"],
            document_currency=test_data["DocumentCurrency"],
            exchange_rate=float(test_data["ExchangeRate"]),
        )
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"PurchaseOrder/0001/PurchaseOrder/{purchase_order_id}"
        )
