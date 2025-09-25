from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.common_classes_purchase_support import (
    SAPS4HANAAccountAssignmentCategory,
)
from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.create_purchase_requisition import (
    sap_s4_hana_create_purchase_requisition,
)


def test_sap_s4_hana_create_purchase_requisition_unknown() -> None:
    """Test the `sap_s4_hana_create_purchase_requisition` function when the
    account_assignment_category is Unknown."""

    # Define test data
    test_data = {
        "purchase_requisition_id": "123999",
        "account_assignment_category": "UNKNOWN",
        "material_id": "2000000050",
        "requested_quantity": "50",
        "purchase_requisition_price": "500",
        "purchasing_group": "001",
        "plant": "1010",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.create_purchase_requisition.get_sap_s4_hana_client"
    ) as mock_hana_client:
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {"PurchaseRequisition": test_data["purchase_requisition_id"]}
        }

        response = sap_s4_hana_create_purchase_requisition(
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
            purchasing_group=test_data["purchasing_group"],
            plant=test_data["plant"],
        ).content

        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader",
            payload={
                "to_PurchaseReqnItem": {
                    "results": [
                        {
                            "PurchaseRequisitionType": "NB",
                            "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                                test_data["account_assignment_category"]
                            ].value,
                            "Material": test_data["material_id"],
                            "PurchasingGroup": test_data["purchasing_group"],
                            "RequestedQuantity": test_data["requested_quantity"],
                            "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                            "Plant": test_data["plant"],
                        }
                    ]
                },
            },
        )


def test_sap_s4_hana_create_purchase_requisition_sales_order() -> None:
    """Test the `sap_s4_hana_create_purchase_requisition` function when the
    account_assignment_category is Sales Order."""

    # Define test data
    test_data = {
        "purchase_requisition_id": "1000321",
        "account_assignment_category": "SALES_ORDER",
        "material_id": "2000000050",
        "requested_quantity": "20",
        "purchase_requisition_price": "200",
        "purchasing_group": "001",
        "plant": "1010",
        "gl_account": "540000",
        "sales_order": "100043",
        "sales_document_item": "10",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.create_purchase_requisition.get_sap_s4_hana_client"
    ) as mock_hana_client:
        mock_client = MagicMock()
        mock_hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {"PurchaseRequisition": test_data["purchase_requisition_id"]}
        }

        response = sap_s4_hana_create_purchase_requisition(
            account_assignment_category=test_data["account_assignment_category"],
            material_id=test_data["material_id"],
            requested_quantity=test_data["requested_quantity"],
            purchase_requisition_price=test_data["purchase_requisition_price"],
            purchasing_group=test_data["purchasing_group"],
            plant=test_data["plant"],
            gl_account=test_data["gl_account"],
            sales_order=test_data["sales_order"],
            sales_document_item=test_data["sales_document_item"],
        ).content

        assert response
        assert response.purchase_requisition_id == test_data["purchase_requisition_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader",
            payload={
                "to_PurchaseReqnItem": {
                    "results": [
                        {
                            "PurchaseRequisitionType": "NB",
                            "AccountAssignmentCategory": SAPS4HANAAccountAssignmentCategory[
                                test_data["account_assignment_category"]
                            ].value,
                            "Material": test_data["material_id"],
                            "PurchasingGroup": test_data["purchasing_group"],
                            "RequestedQuantity": test_data["requested_quantity"],
                            "PurchaseRequisitionPrice": test_data["purchase_requisition_price"],
                            "Plant": test_data["plant"],
                            "to_PurchaseReqnAcctAssgmt": {
                                "results": [
                                    {
                                        "GLAccount": test_data["gl_account"],
                                        "SalesOrder": test_data["sales_order"],
                                        "SalesDocumentItem": test_data["sales_document_item"],
                                    }
                                ]
                            },
                        }
                    ]
                },
            },
        )
