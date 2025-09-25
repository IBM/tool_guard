from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAItemTextTypes,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_requisition_item_texts import (
    sap_s4_hana_get_requisition_item_texts,
)


def test_get_requisition_item_texts() -> None:
    """Test that the `sap_s4_hana_get_requisition_item_texts` function returns the expected
    response."""

    test_data = {
        "purchase_requisition_id": "10000015",
        "purchase_requisition_item_id": "10",
        "item_text_type": "B01",
        "item_text": "text retrieved from  item text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_requisition_item_texts.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "DocumentText": test_data["item_text_type"],
                            "NoteDescription": test_data["item_text"],
                        }
                    ]
                }
            }
        }

        response = sap_s4_hana_get_requisition_item_texts(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
        ).content
        assert response
        assert (
            response.requisition_texts[0].item_text_type
            == SAPS4HANAItemTextTypes(test_data["item_text_type"]).name
        )
        assert response.requisition_texts[0].item_text == test_data["item_text"]

        mock_client.get_request.assert_any_call(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data["purchase_requisition_id"]}',PurchaseRequisitionItem='{test_data["purchase_requisition_item_id"]}')/to_PurchaseReqnItemText",
            params={"$top": 20, "$skip": 0},
        )
