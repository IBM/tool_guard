from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderItemTextTypes,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_item_texts import (
    sap_s4_hana_get_purchase_order_item_texts,
)


def test_get_purchase_order_item_texts() -> None:
    """Test that the `sap_s4_hana_get_purchase_order_item_texts` function returns the expected
    response."""

    test_data = {
        "purchase_order_id": "4500001950",
        "purchase_order_item_id": "10",
        "item_text_type": "F01",
        "item_text": "PO Items Item text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_item_texts.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "TextObjectType": test_data["item_text_type"],
                        "PlainLongText": test_data["item_text"],
                    }
                ]
            }
        }

        response = sap_s4_hana_get_purchase_order_item_texts(
            purchase_order_id=test_data["purchase_order_id"],
            purchase_order_item_id=test_data["purchase_order_item_id"],
        ).content

        assert response
        assert (
            response.item_texts[0].item_text_type
            == SAPS4HANAPurchaseOrderItemTextTypes(test_data["item_text_type"]).name
        )
        assert response.item_texts[0].item_text == test_data["item_text"]

        mock_client.get_request.assert_called_once_with(
            entity=f"PurchaseOrder/0001/PurchaseOrderItem/{test_data['purchase_order_id']}/{test_data['purchase_order_item_id']}/_PurchaseOrderItemNote",
            params={"$top": 20, "$skip": 0},
        )
