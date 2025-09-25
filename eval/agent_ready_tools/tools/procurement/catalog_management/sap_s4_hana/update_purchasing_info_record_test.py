from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_purchasing_info_record import (
    S4HanaUpdatePurchasingInfoRecordResponse,
    sap_s4_hana_update_purchasing_info_record,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_sap_s4_hana_update_purchasing_info_record_success() -> None:
    """Test that the purchasing info record update returns expected ToolResponse on success."""

    # Define test data
    test_data = {
        "purchasing_info_record_id": "5300000597",
        "supplier": "1070",
        "material": "FG251",
        "purchasing_info_record_desc": "Test Description",
        "supplier_resp_sales_person_name": "John Doe",
        "supplier_phone_number": "9876543210",
        "availability_start_date": "2025-07-11",
        "availability_end_date": "2026-07-11",
        "manufacturer": "Test Manufacturer",
        "product_purchase_points_quantity": "100",
        "product_purchase_points_quantity_unit": "P",
    }

    expected_response = ToolResponse(
        success=True,
        message="Record updated successfully.",
        content=S4HanaUpdatePurchasingInfoRecordResponse(http_code=204),
    )

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_purchasing_info_record.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": 204}

        # Call the function
        response = sap_s4_hana_update_purchasing_info_record(**test_data)

        # Verify that the details match the expected data
        assert isinstance(response, ToolResponse)
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord('5300000597')",
            payload={
                "d": {
                    "Supplier": "1070",
                    "Material": "FG251",
                    "PurchasingInfoRecordDesc": "Test Description",
                    "SupplierRespSalesPersonName": "John Doe",
                    "SupplierPhoneNumber": "9876543210",
                    "AvailabilityStartDate": "/Date(1752192000000)/",
                    "AvailabilityEndDate": "/Date(1783728000000)/",
                    "Manufacturer": "Test Manufacturer",
                    "ProductPurchasePointsQty": "100",
                    "ProductPurchasePointsQtyUnit": "P",
                }
            },
        )
