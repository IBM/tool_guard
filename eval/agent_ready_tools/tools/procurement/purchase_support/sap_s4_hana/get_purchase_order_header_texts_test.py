from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAPurchaseOrderHeaderTextTypes,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_header_texts import (
    sap_s4_hana_get_purchase_order_header_texts,
)


def test_get_purchase_order_header_texts() -> None:
    """Test that the `sap_s4_hana_get_purchase_order_header_texts` function returns the expected
    response."""

    test_data = {
        "purchase_order_id": "4500001950",
        "header_text_type": "F01",
        "header_text": "PO Header Text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_order_header_texts.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "TextObjectType": test_data["header_text_type"],
                        "PlainLongText": test_data["header_text"],
                    }
                ]
            }
        }

        response = sap_s4_hana_get_purchase_order_header_texts(
            purchase_order_id=test_data["purchase_order_id"],
            header_text_type=SAPS4HANAPurchaseOrderHeaderTextTypes.TEXT,
        ).content

        assert response
        assert (
            response.header_texts[0].header_text_type
            == SAPS4HANAPurchaseOrderHeaderTextTypes(test_data["header_text_type"]).name
        )
        assert response.header_texts[0].header_text == test_data["header_text"]

        mock_client.get_request.assert_called_once_with(
            entity=f"PurchaseOrder/0001/PurchaseOrder/{test_data['purchase_order_id']}/_PurchaseOrderNote",
            filter_expr=f"TextObjectType eq '{test_data['header_text_type']}'",
            params={"$top": 20, "$skip": 0},
        )
