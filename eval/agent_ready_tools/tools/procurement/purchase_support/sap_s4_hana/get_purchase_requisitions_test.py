from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_requisitions import (
    sap_s4_hana_get_purchase_requisitions,
)


def test_sap_s4_hana_get_purchase_requisition() -> None:
    """Test that the `sap_s4_hana_get_purchase_requisition` function returns the expected
    response."""

    # Define test data
    test_data = {
        "purchase_requisition_id": "10000000",
        "purchase_requisition_type": "NB",
        "purchase_requisition_description": "sample description",
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.get_purchase_requisitions.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:

        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "PurchaseRequisition": test_data["purchase_requisition_id"],
                            "PurchaseRequisitionType": test_data["purchase_requisition_type"],
                            "PurReqnDescription": test_data["purchase_requisition_description"],
                        }
                    ]
                }
            }
        }

        response = sap_s4_hana_get_purchase_requisitions().content
        assert response
        assert (
            response.purchase_requisitions[0].purchase_requisition_id
            == test_data["purchase_requisition_id"]
        )
        assert (
            response.purchase_requisitions[0].purchase_requisition_type
            == test_data["purchase_requisition_type"]
        )
        assert (
            response.purchase_requisitions[0].purchase_requisition_description
            == test_data["purchase_requisition_description"]
        )

        mock_client.get_request.assert_called_once_with(
            entity="API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader",
            expand_expr="to_PurchaseReqnItem",
            params={"$top": 20, "$skip": 0},
            filter_expr=None,
        )
