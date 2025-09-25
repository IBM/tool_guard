from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_goods_receipts import (
    sap_s4_hana_get_goods_receipts,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_sap_s4_hana_get_goods_receipts() -> None:
    """Test that the `sap_s4_hana_get_goods_receipts` function returns the expected response."""
    # Define test data:
    test_data = {
        "goods_receipt_id": "4900000493",
        "goods_receipt_year": "2019",
        "inventory_transaction_type": "WA",
        "date_received": "/Date(1550102400000)/",
        "date_created": "/Date(1550102400000)/",
        "created_after": "2019-02-14",
        "created_before": "2019-02-15",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_goods_receipts.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "MaterialDocumentYear": "2019",
                            "MaterialDocument": "4900000493",
                            "InventoryTransactionType": "WA",
                            "DocumentDate": "/Date(1550102400000)/",
                            "CreationDate": "/Date(1550102400000)/",
                            "CreatedByUser": "NKOLISETTI",
                        },
                    ]
                }
            }
        }

        # Get good receipts
        response = sap_s4_hana_get_goods_receipts(
            created_after=test_data["created_after"], created_before=test_data["created_before"]
        ).content

        # Ensure that sap_s4_hana_get_goods_receipts() executed and returned proper values.
        assert response
        goods_receipt = response.goods_receipts[0]
        assert goods_receipt.goods_receipt_id == test_data["goods_receipt_id"]
        assert goods_receipt.goods_receipt_year == test_data["goods_receipt_year"]
        assert goods_receipt.inventory_transaction_type == test_data["inventory_transaction_type"]
        assert goods_receipt.date_received == sap_date_to_iso_8601(str(test_data["date_received"]))
        assert goods_receipt.date_created == sap_date_to_iso_8601(str(test_data["date_created"]))

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_MATERIAL_DOCUMENT_SRV1/A_MaterialDocumentHeader",
            filter_expr=f"CreationDate ge datetime'{test_data["created_after"]}T00:00:00' and CreationDate le datetime'{test_data["created_before"]}T00:00:00'",
            params={"$top": 20, "$skip": 0},
        )
