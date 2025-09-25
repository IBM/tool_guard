from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_supplier_po_transmission import (
    oracle_fusion_update_supplier_po_transmission,
)


def test_oracle_fusion_update_supplier_po_transmission() -> None:
    """Test that the `oracle_fusion_update_supplier_po_transmission` function updates supplier PO
    transmission."""

    # Define test data
    test_data = {
        "purchase_order_id": "300000025672061",
        "supplier_id": "300000010011003",
        "supplier_site_id": "300000010011025",
        "communication_method": "EMAIL",
        "supplier_email": "abcteste@ibm.com",
        "supplier_cc_email": "ccabctest@ibm.com",
        "supplier_bcc_email": "bccabctest@ibm.com",
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_supplier_po_transmission.get_oracle_fusion_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = {
            "SupplierId": test_data["supplier_id"],
            "SupplierSiteId": test_data["supplier_site_id"],
            "SupplierCommunicationMethod": test_data["communication_method"],
            "SupplierCCEmailAddress": test_data["supplier_cc_email"],
            "SupplierBCCEmailAddress": test_data["supplier_bcc_email"],
            "SupplierEmailAddress": test_data["supplier_email"],
        }

        # Call the function
        response = oracle_fusion_update_supplier_po_transmission(
            purchase_order_id=test_data["purchase_order_id"],
            supplier_id=test_data["supplier_id"],
            supplier_site_id=test_data["supplier_site_id"],
            communication_method=test_data["communication_method"],
            supplier_email=test_data["supplier_email"],
            supplier_cc_email=test_data["supplier_cc_email"],
            supplier_bcc_email=test_data["supplier_bcc_email"],
        ).content

        assert response
        assert response.communication_method == test_data["communication_method"]
        assert response.supplier_email == test_data["supplier_email"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            resource_name=f"draftPurchaseOrders/{test_data['purchase_order_id']}",
            payload={
                "SupplierId": test_data["supplier_id"],
                "SupplierSiteId": test_data["supplier_site_id"],
                "SupplierCommunicationMethod": test_data["communication_method"],
                "SupplierCCEmailAddress": test_data["supplier_cc_email"],
                "SupplierBCCEmailAddress": test_data["supplier_bcc_email"],
                "SupplierEmailAddress": test_data["supplier_email"],
            },
        )
