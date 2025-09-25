from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_requisition_general_info import (
    oracle_fusion_update_requisition_general_info,
)


def test_oracle_fusion_update_requisition_general_info() -> None:
    """Test that the `oracle_fusion_update_requisition_general_info` function updates requisition
    general info."""

    # Define test data
    test_data = {
        "purchase_requisition_id": "300000025241141",
        "description": "Updated requisition description",
        "justification": "Created requisition for testing.",
    }

    update_response = {
        "RequisitionHeaderId": 300000025241141,
        "Requisition": "204221",
        "Preparer": "Test Buyer",
        "Description": test_data["description"],
        "DocumentStatus": "Approved",
        "CreationDate": "2025-07-24T11:51:20.274+00:00",
        "FundsStatus": "Not applicable",
        "Justification": test_data["justification"],
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.update_requisition_general_info.get_oracle_fusion_client"
    ) as mock_oracle_client:
        # Create a mock client
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = update_response

        # Call the function
        response = oracle_fusion_update_requisition_general_info(
            purchase_requisition_id=test_data["purchase_requisition_id"],
            description=test_data["description"],
            justification=test_data["justification"],
        ).content

        assert response
        assert response.purchase_requisition_id == int(test_data["purchase_requisition_id"])
        assert response.description == test_data["description"]
        assert response.justification == test_data["justification"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            resource_name=f"purchaseRequisitions/{test_data['purchase_requisition_id']}",
            payload={
                "Description": test_data["description"],
                "Justification": test_data["justification"],
            },
        )
