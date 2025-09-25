from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_requisition_line_item import (
    oracle_fusion_update_requisition_line_item,
)


def test_oracle_fusion_update_requisition_line_item() -> None:
    """Test that the `oracle_fusion_update_requisition_line_item` function updates requisition line
    item."""

    test_data = {
        "purchase_requisition_id": "300000025813701",
        "requisition_line_id": 300000025813702,
        "requisition_distribution_id": 300000025813703,
        "quantity": 20,
        "deliver_to_location_code": "USLOC_CENT",
        "destination_type_code": "EXPENSE",
        "requested_delivery_date": "2025-08-19",
        "billing_quantity": 3,
        "item": "Macbook Pro 15 inch",
        "item_id": 300000025339742,
        "item_description": "macbook pro 15 inch for Wxo test",
        "requester": "Jaiswal, Sangita",
        "distribution_number": 1,
        "charge_account_id": 300000024004106,
        "charge_account": "101.10.11101.000.000.000",
        "billing_amount": 2697.0,
        "budget_date": "2025-08-18",
    }

    test_response = {
        "RequisitionLineId": test_data["requisition_line_id"],
        "Item": test_data["item"],
        "ItemId": test_data["item_id"],
        "ItemDescription": test_data["item_description"],
        "Quantity": test_data["quantity"],
        "RequesterDisplayName": test_data["requester"],
        "DeliverToLocationCode": test_data["deliver_to_location_code"],
        "DestinationType": test_data["destination_type_code"],
        "RequestedDeliveryDate": test_data["requested_delivery_date"],
        "distributions": [
            {
                "RequisitionDistributionId": test_data["requisition_distribution_id"],
                "DistributionNumber": test_data["distribution_number"],
                "Quantity": test_data["billing_quantity"],
                "ChargeAccountId": test_data["charge_account_id"],
                "ChargeAccount": test_data["charge_account"],
                "CurrencyAmount": test_data["billing_amount"],
                "BudgetDate": test_data["budget_date"],
            }
        ],
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_requisition_line_item.get_oracle_fusion_client"
    ) as mock_oracle_client:
        # Create a mock client
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = test_response

        # Call the function
        response = oracle_fusion_update_requisition_line_item(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            requisition_line_id=str(test_data["requisition_line_id"]),
            requisition_distribution_id=str(test_data["requisition_distribution_id"]),
            quantity=test_data["quantity"],
            deliver_to_location_code=test_data["deliver_to_location_code"],
            destination_type_code=test_data["destination_type_code"],
            requested_delivery_date=test_data["requested_delivery_date"],
            billing_quantity=test_data["billing_quantity"],
        ).content

        assert response
        assert response.requisition_line_id == test_data["requisition_line_id"]
        assert response.quantity == test_data["quantity"]
        assert response.requester == test_data["requester"]
        assert response.deliver_to_location_code == test_data["deliver_to_location_code"]
        assert response.requested_delivery_date == test_data["requested_delivery_date"]
        assert (
            response.billing_details[0].requisition_distribution_id
            == test_data["requisition_distribution_id"]
        )
        assert response.billing_details[0].budget_date == test_data["budget_date"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            resource_name=f"purchaseRequisitions/{test_data['purchase_requisition_id']}/child/lines/{test_data['requisition_line_id']}",
            payload={
                "Quantity": test_data["quantity"],
                "DeliverToLocationCode": test_data["deliver_to_location_code"],
                "DestinationTypeCode": test_data["destination_type_code"],
                "RequestedDeliveryDate": test_data["requested_delivery_date"],
                "distributions": [
                    {
                        "RequisitionDistributionId": str(test_data["requisition_distribution_id"]),
                        "Quantity": test_data["billing_quantity"],
                    }
                ],
            },
        )
