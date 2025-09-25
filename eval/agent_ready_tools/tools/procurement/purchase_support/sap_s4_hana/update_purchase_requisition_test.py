from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_requisition import (
    sap_s4_hana_update_purchase_requisition,
)


def test_update_purchase_requisition() -> None:
    """Test that the sap_s4_hana_update_purchase_requisition tool updates purchase requisition
    successfully."""

    # Define test data
    test_data = {
        "purchase_requisition_id": "10000000",
        "description": "sample description",
        "http_code": 204,
    }
    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.sap_s4_hana.update_purchase_requisition.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": test_data["http_code"]}

        # Call the function under test
        response = sap_s4_hana_update_purchase_requisition(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            description=test_data["description"],
        ).content

        # Ensure that update_purchase_requisition() executed and returned proper values
        assert response
        assert response["http_code"] == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=f"API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader('{test_data["purchase_requisition_id"]}')",
            payload={
                "PurReqnDescription": test_data["description"],
            },
        )
