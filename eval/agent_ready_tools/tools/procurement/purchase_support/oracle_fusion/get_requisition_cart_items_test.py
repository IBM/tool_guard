from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_requisition_cart_items import (
    oracle_fusion_get_requisition_cart_items,
)


def test_oracle_fusion_get_requisition_cart_items() -> None:
    """Test the getting of cart items from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "Item": "PK101",
                "Description": "Test Product ",
                "Category": "Test Category",
                "UOM": "Bg",
                "Price": 50,
                "CurrencyCode": "USD",
                "LineType": "Goods",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_requisition_cart_items.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_requisition_cart_items()

        assert response
        assert response.content[0].item_number == test_result["items"][0]["Item"]
        assert response.content[0].item_description == test_result["items"][0]["Description"]

        mock_client.get_request.assert_called_once_with(
            resource_name="purchaseAgreementLines",
            params={"limit": 10, "offset": 0},
        )
