from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.submit_purchase_order import (
    oracle_fusion_submit_purchase_order,
)


def test_oracle_fusion_submit_purchase_order() -> None:
    """Tests oracle_fusion_submit_purchase_order using a mock client."""
    test_data = {"purchase_order_id": "300000026074101"}

    mock_result = "Purchase order submitted successfully."

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.submit_purchase_order.get_oracle_fusion_client"
    ) as mock_oracle_client:
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {"result": mock_result}

        response = oracle_fusion_submit_purchase_order(
            purchase_order_id=test_data["purchase_order_id"]
        )

        assert response.success is True
        assert response.content.result == mock_result
        assert response.message == "Purchase order submitted successfully in Oracle Fusion."

        mock_client.post_request.assert_called_once_with(
            resource_name=f"draftPurchaseOrders/{test_data['purchase_order_id']}/action/submit",
            headers={"Content-Type": "application/vnd.oracle.adf.action+json"},
            payload={"validateBeforeSubmitFlag": "true"},
        )
