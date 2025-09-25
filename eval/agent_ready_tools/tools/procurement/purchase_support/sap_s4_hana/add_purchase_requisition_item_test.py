from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_purchase_requisition_item import (
    sap_s4_hana_add_purchase_requisition_item,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAAccountAssignmentCategory,
)


def test_sap_s4_hana_add_purchase_requisition_item_with_unknown() -> None:
    """Verify that the `sap_s4_hana_add_purchase_requisition_item` tool successfully adds an item to
    a purchase requisition in SAP S4 HANA."""

    # Define test data
    test_data: Dict[str, Any] = {
        "purchase_requisition_item_id": "230",
        "purchase_requisition_id": "10000264",
        "account_assignment_category": "UNKNOWN",
        "material_id": "34",
        "plant": "1010",
        "purchasing_group": "Z01",
        "requested_quantity": "25",
        "purchase_requisition_price": "13",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_purchase_requisition_item.get_sap_s4_hana_client"
    ) as mock_s4hana_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_s4hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
            }
        }

        # Add a purchase requisition item
        response = sap_s4_hana_add_purchase_requisition_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            purchasing_group=test_data["purchasing_group"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
        ).content

        # Ensure that sap_s4_hana_add_purchase_requisition_item() executed and returned proper values
        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]
        assert response.purchase_requisition_item_id == test_data["purchase_requisition_item_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                    test_data["account_assignment_category"]
                ].value,
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "PurchasingGroup": test_data["purchasing_group"],
                "RequestedQuantity": test_data["requested_quantity"],
                "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                "to_PurchaseReqnItemText": {
                    "results": [
                        {
                            "Language": "EN",
                        }
                    ]
                },
            },
        )


def test_sap_s4_hana_add_purchase_requisition_item_with_order_or_cost_center() -> None:
    """Verify that the `sap_s4_hana_add_purchase_requisition_item` tool successfully adds an item to
    a purchase requisition in SAP S4 HANA."""

    # Define test data
    test_data: Dict[str, Any] = {
        "purchase_requisition_item_id": "230",
        "purchase_requisition_id": "10000264",
        "account_assignment_category": "ORDER",
        "material_id": "34",
        "plant": "1010",
        "purchasing_group": "Z01",
        "requested_quantity": "25",
        "purchase_requisition_price": "13",
        "gl_account": "54300000",
        "order_id": "1000044",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_purchase_requisition_item.get_sap_s4_hana_client"
    ) as mock_s4hana_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_s4hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
            }
        }

        # Add a purchase requisition item
        response = sap_s4_hana_add_purchase_requisition_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            purchasing_group=test_data["purchasing_group"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
            gl_account=test_data["gl_account"],
            order_id=test_data["order_id"],
        ).content

        # Ensure that sap_s4_hana_add_purchase_requisition_item() executed and returned proper values
        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]
        assert response.purchase_requisition_item_id == test_data["purchase_requisition_item_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                    test_data["account_assignment_category"]
                ].value,
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "PurchasingGroup": test_data["purchasing_group"],
                "RequestedQuantity": test_data["requested_quantity"],
                "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                "to_PurchaseReqnAcctAssgmt": {
                    "results": [
                        {
                            "GLAccount": test_data["gl_account"],
                            "OrderID": test_data["order_id"],
                        }
                    ]
                },
                "to_PurchaseReqnItemText": {
                    "results": [
                        {
                            "Language": "EN",
                        }
                    ]
                },
            },
        )


def test_sap_s4_hana_add_purchase_requisition_item_with_sales_order() -> None:
    """Verify that the `sap_s4_hana_add_purchase_requisition_item` tool successfully adds an item to
    a purchase requisition in SAP S4 HANA."""

    # Define test data
    test_data: Dict[str, Any] = {
        "purchase_requisition_item_id": "230",
        "purchase_requisition_id": "10000264",
        "account_assignment_category": "SALES_ORDER",
        "material_id": "34",
        "plant": "1010",
        "purchasing_group": "Z01",
        "requested_quantity": "25",
        "purchase_requisition_price": "13",
        "gl_account": "54300000",
        "sales_order": "10000332",
        "sales_document_item": "10",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_purchase_requisition_item.get_sap_s4_hana_client"
    ) as mock_s4hana_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_s4hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
            }
        }

        # Add a purchase requisition item
        response = sap_s4_hana_add_purchase_requisition_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            purchasing_group=test_data["purchasing_group"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
            gl_account=test_data["gl_account"],
            sales_order=test_data["sales_order"],
            sales_document_item=test_data["sales_document_item"],
        ).content

        # Ensure that sap_s4_hana_add_purchase_requisition_item() executed and returned proper values
        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]
        assert response.purchase_requisition_item_id == test_data["purchase_requisition_item_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                    test_data["account_assignment_category"]
                ].value,
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "PurchasingGroup": test_data["purchasing_group"],
                "RequestedQuantity": test_data["requested_quantity"],
                "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                "to_PurchaseReqnAcctAssgmt": {
                    "results": [
                        {
                            "GLAccount": test_data["gl_account"],
                            "SalesOrder": test_data["sales_order"],
                            "SalesDocumentItem": test_data["sales_document_item"],
                        }
                    ]
                },
                "to_PurchaseReqnItemText": {
                    "results": [
                        {
                            "Language": "EN",
                        }
                    ]
                },
            },
        )


def test_sap_s4_hana_add_purchase_requisition_item_with_project() -> None:
    """Verify that the `sap_s4_hana_add_purchase_requisition_item` tool successfully adds an item to
    a purchase requisition in SAP S4 HANA."""

    # Define test data
    test_data: Dict[str, Any] = {
        "purchase_requisition_item_id": "230",
        "purchase_requisition_id": "10000264",
        "account_assignment_category": "PROJECT",
        "material_id": "34",
        "plant": "1010",
        "purchasing_group": "Z01",
        "requested_quantity": "25",
        "purchase_requisition_price": "13",
        "gl_account": "54300000",
        "wbse_element": "DE.000.01-00011",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.add_purchase_requisition_item.get_sap_s4_hana_client"
    ) as mock_s4hana_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_s4hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "PurchaseRequisitionItem": test_data["purchase_requisition_item_id"],
            }
        }

        # Add a purchase requisition item
        response = sap_s4_hana_add_purchase_requisition_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            purchasing_group=test_data["purchasing_group"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
            gl_account=test_data["gl_account"],
            wbse_element=test_data["wbse_element"],
        ).content

        # Ensure that sap_s4_hana_add_purchase_requisition_item() executed and returned proper values
        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]
        assert response.purchase_requisition_item_id == test_data["purchase_requisition_item_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem",
            payload={
                "PurchaseRequisition": test_data["purchase_requisition_id"],
                "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                    test_data["account_assignment_category"]
                ].value,
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "PurchasingGroup": test_data["purchasing_group"],
                "RequestedQuantity": test_data["requested_quantity"],
                "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                "to_PurchaseReqnAcctAssgmt": {
                    "results": [
                        {
                            "GLAccount": test_data["gl_account"],
                            "WBSElement": test_data["wbse_element"],
                        }
                    ]
                },
                "to_PurchaseReqnItemText": {
                    "results": [
                        {
                            "Language": "EN",
                        }
                    ]
                },
            },
        )
