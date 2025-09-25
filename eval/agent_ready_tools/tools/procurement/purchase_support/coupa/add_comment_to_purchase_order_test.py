from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.add_comment_to_purchase_order import (
    coupa_add_comment_to_purchase_order,
)


def test_coupa_add_comment_to_purchase_order() -> None:
    """Test that the `add_comment_to_purchase_order` function returns the expected Comment."""

    # Define test data
    test_data: dict[str, Any] = {
        "purchase_order_id": 4160,
        "comment": {
            "id": 471,
            "created-at": "2025-04-14T10:00:00-07:00",
            "updated-at": "2025-04-14T10:00:00-07:00",
            "commentable-id": 4160,
            "commentable-type": "OrderHeader",
            "comments": "This is a test comment2",
            "created-by": {"login": "IBMFunctionalUser"},
            "updated-by": {"login": "IBMFunctionalUser"},
        },
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.add_comment_to_purchase_order.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = test_data["comment"]

        # Add comment to purchase order
        response = coupa_add_comment_to_purchase_order(
            test_data["purchase_order_id"], test_data["comment"]["comments"]
        ).content

        # Ensure that add_comment_to_purchase_order() executed and returned proper values
        assert response
        assert response.comment_text == test_data["comment"]["comments"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name=f"purchase_orders/{test_data["purchase_order_id"]}/comments",
            payload={"comments": test_data["comment"]["comments"]},
        )
