from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_purchase_requisition_by_id import (
    oracle_fusion_get_purchase_requisition_by_id,
)


def test_oracle_fusion_get_purchase_order_by_id() -> None:
    """Test that the `oracle_fusion_get_purchase_requisition_by_id` function returns expected
    purchase requisition details."""

    # Define test data
    purchase_requisition_id = "300000025809132"
    test_data: Dict[str, Any] = {
        "RequisitionHeaderId": 300000025809132,
        "DocumentStatus": "Approved",
        "CreationDate": "2025-07-24T11:51:20.274+00:00",
        "FundsStatus": "Not applicable",
        "Requisition": "204234",
        "RequisitioningBUId": 300000002168484,
        "RequisitioningBU": "US1 Business Unit",
        "PreparerId": 300000025809132,
        "Preparer": "sri",
        "Description": "testing",
        "Justification": "Testing rest api",
        "IdentificationKey": "REQ_300000025809132_0",
        "RequisitionLineGroup": "PO",
        "TaxationCountry": "United States",
        "lines": [
            {
                "RequisitionLineId": 300000025810082,
                "LineNumber": 1,
                "CategoryName": "Test Category",
                "ItemDescription": "Test001DemoJDE",
                "ItemId": 300000016236035,
                "Item": "Test001JDE",
                "Quantity": 10,
                "UnitPrice": 100,
                "RequesterDisplayName": "sri",
                "UOM": "Ea",
                "Price": 100,
                "LineStatusDisplayValue": "Approved",
                "PurchaseOrder": "US164540",
                "DeliverToLocationCode": "USLOC_CENT",
                "DestinationType": "Expense",
                "BuyerOnPurchaseOrder": "sriya",
                "SupplierOnPurchaseOrder": "ABC Corp",
                "SupplierItemNumber": "1234",
                "SourceAgreement": "52278",
                "RequestedDeliveryDate": "2025-08-16",
            }
        ],
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_purchase_requisition_by_id.get_oracle_fusion_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Call the function
        response = oracle_fusion_get_purchase_requisition_by_id(
            purchase_requisition_id=purchase_requisition_id
        ).content

        assert response
        assert response.purchase_requisition_id == test_data["RequisitionHeaderId"]
        assert response.requisitioning_business_unit == test_data["RequisitioningBU"]
        assert response.requisitioning_business_unit_id == test_data["RequisitioningBUId"]
        assert response.preparer_id == test_data["PreparerId"]
        assert response.preparer == test_data["Preparer"]
        assert response.description == test_data["Description"]
        assert response.justification == test_data["Justification"]
        assert response.identification_key == test_data["IdentificationKey"]
        assert response.requisition_line_group == test_data["RequisitionLineGroup"]
        assert response.taxation_country == test_data["TaxationCountry"]
        assert response.purchase_requisition_items[0].item_id == test_data["lines"][0]["ItemId"]
        assert response.purchase_requisition_items[0].item == test_data["lines"][0]["Item"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"purchaseRequisitions/{purchase_requisition_id}",
            params={"expand": "lines.distributions"},
        )
