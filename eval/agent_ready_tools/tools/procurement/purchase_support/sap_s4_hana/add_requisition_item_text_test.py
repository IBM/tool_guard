from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text import (
    sap_s4_hana_add_requisition_item_text,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAItemTextTypes,
)


def test_sap_s4_hana_add_requisition_item_text_item_text() -> None:
    """
    Test that the `sap_s4_hana_add_requisition_item_text` function returns the expected response.

    Tests the response when item text type is ITEM_TEXT.
    """

    # Define test data:
    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_item_id": "10",
        "item_text": "Test Item Text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": SAPS4HANAItemTextTypes.ITEM_TEXT,
                "Language": "EN",
            }
        }

        response = sap_s4_hana_add_requisition_item_text(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            item_text_types="ITEM_TEXT",
        ).content

        assert response
        assert response.item_text == test_data["item_text"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')/to_PurchaseReqnItemText",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": str(SAPS4HANAItemTextTypes.ITEM_TEXT),
                "Language": "EN",
            },
        )


def test_sap_s4_hana_add_requisition_item_text_item_note() -> None:
    """
    Test that the `sap_s4_hana_add_requisition_item_text` function returns the expected response.

    Tests the response when item text type is ITEM_NOTE.
    """

    # Define test data:
    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_item_id": "10",
        "item_text": "Test Item Note",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": SAPS4HANAItemTextTypes.ITEM_NOTE,
                "Language": "EN",
            }
        }

        response = sap_s4_hana_add_requisition_item_text(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            item_text_types="ITEM_NOTE",
        ).content

        assert response
        assert response.item_text == test_data["item_text"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')/to_PurchaseReqnItemText",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": str(SAPS4HANAItemTextTypes.ITEM_NOTE),
                "Language": "EN",
            },
        )


def test_sap_s4_hana_add_requisition_item_text_delivery_text() -> None:
    """
    Test that the `sap_s4_hana_add_requisition_item_text` function returns the expected response.

    Tests the response when item text type is DELIVERY_TEXT.
    """

    # Define test data:
    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_item_id": "10",
        "item_text": "Test Delivery Text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": SAPS4HANAItemTextTypes.DELIVERY_TEXT,
                "Language": "EN",
            }
        }

        response = sap_s4_hana_add_requisition_item_text(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            item_text_types="DELIVERY_TEXT",
        ).content

        assert response
        assert response.item_text == test_data["item_text"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')/to_PurchaseReqnItemText",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": str(SAPS4HANAItemTextTypes.DELIVERY_TEXT),
                "Language": "EN",
            },
        )


def test_sap_s4_hana_add_requisition_item_text_material_po_text() -> None:
    """
    Test that the `sap_s4_hana_add_requisition_item_text` function returns the expected response.

    Tests the response when item text type is MATERIAL_PO_TEXT.
    """

    # Define test data:
    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_item_id": "10",
        "item_text": "Test Material PO Text",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": SAPS4HANAItemTextTypes.MATERIAL_PO_TEXT,
                "Language": "EN",
            }
        }

        response = sap_s4_hana_add_requisition_item_text(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            item_text_types="MATERIAL_PO_TEXT",
        ).content

        assert response
        assert response.item_text == test_data["item_text"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')/to_PurchaseReqnItemText",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": str(SAPS4HANAItemTextTypes.MATERIAL_PO_TEXT),
                "Language": "EN",
            },
        )


def test_sap_s4_hana_add_requisition_item_text_in_rr_sale_order_3rd_party() -> None:
    """
    Test that the `sap_s4_hana_add_requisition_item_text` function returns the expected response.

    Tests the response when item text type is IN_RR_SALE_ORDER_3RD_PARTY.
    """

    # Define test data:
    test_data = {
        "purchase_requisition_id": "10000134",
        "purchase_requisition_item_id": "10",
        "item_text": "Test Sale Order 3rd Party",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_requisition_item_text.get_sap_s4_hana_client"
    ) as mock_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": SAPS4HANAItemTextTypes.IN_RR_SALE_ORDER_3RD_PARTY,
                "Language": "EN",
            }
        }

        response = sap_s4_hana_add_requisition_item_text(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            purchase_requisition_item_id=test_data["purchase_requisition_item_id"],
            item_text=test_data["item_text"],
            item_text_types="IN_RR_SALE_ORDER_3RD_PARTY",
        ).content

        assert response
        assert response.item_text == test_data["item_text"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition='{test_data['purchase_requisition_id']}',PurchaseRequisitionItem='{test_data['purchase_requisition_item_id']}')/to_PurchaseReqnItemText",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
                "NoteDescription": test_data["item_text"],
                "DocumentText": str(SAPS4HANAItemTextTypes.IN_RR_SALE_ORDER_3RD_PARTY),
                "Language": "EN",
            },
        )
