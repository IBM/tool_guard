from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_by_id_test import (
    mock_purchase_order_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.update_purchase_order_general_info_by_id import (
    coupa_update_purchase_order_general_info_by_id,
)


def test_coupa_update_purchase_order_general_info_by_id() -> None:
    """Test that `update_purchase_order_general_info_by_id` function returns the expected
    response."""

    # Define test data:
    test_data: dict[str, Any] = {
        "id": 4152,
        "update_po": {
            "exported": False,
            "ship-to-attention": "Sargam Singh",
            "department": "Operations",
            "ship-to-user": {"login": "mjordan"},
            "shipping-term": "Standard",
            "payment-term": "2/10 Net 30",
        },
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.update_purchase_order_general_info_by_id.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.put_request.return_value = mock_purchase_order_response()

        # Update purchase order general info
        result = coupa_update_purchase_order_general_info_by_id(
            purchase_order_id=test_data["id"],
            exported=test_data["update_po"]["exported"],
            ship_to_attention=test_data["update_po"]["ship-to-attention"],
            department=test_data["update_po"]["department"],
            ship_to_user=test_data["update_po"]["ship-to-user"]["login"],
            shipping_terms=test_data["update_po"]["shipping-term"],
            payment_terms=test_data["update_po"]["payment-term"],
        ).content

        # Ensure that update_purchase_order_general_info_by_id() executed and returned updated response
        assert result.purchase_order_id == test_data["id"]
        assert result.exported == test_data["update_po"]["exported"]
        assert result.ship_to_attention == test_data["update_po"]["ship-to-attention"]

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"purchase_orders/{test_data['id']}",
            payload=test_data["update_po"],
        )
