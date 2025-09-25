from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_comments import (
    coupa_get_purchase_order_comments,
)


def test_coupa_get_purchase_order_comments() -> None:
    """Test that the `get_purchase_order_comments` function returns the expected response."""

    # Define test data:
    test_data: dict[str, Any] = {
        "purchase_order_id": 4160,
        "comments": [
            {
                "id": 470,
                "created-at": "2025-04-11T15:36:40-07:00",
                "updated-at": "2025-04-11T15:36:40-07:00",
                "commentable-id": 4160,
                "commentable-type": "OrderHeader",
                "comments": "testing comments",
                "created-by": {"login": "IBMFunctionalUser"},
                "updated-by": {"login": "IBMFunctionalUser"},
            },
            {
                "id": 471,
                "created-at": "2025-04-11T15:37:24-07:00",
                "updated-at": "2025-04-11T15:37:24-07:00",
                "commentable-id": 4160,
                "commentable-type": "OrderHeader",
                "comments": "testing comments2",
                "created-by": {"login": "IBMFunctionalUser"},
                "updated-by": {"login": "IBMFunctionalUser"},
            },
        ],
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_comments.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data["comments"]

        # Get purchase order comments
        response = coupa_get_purchase_order_comments(
            purchase_order_id=test_data["purchase_order_id"]
        ).content

        # Ensure that get_purchase_order_comments() executed and returned proper values
        assert response
        assert response.comment_list and len(response.comment_list) == 2
        assert response.comment_list[0].comment_text == "testing comments"
        assert response.comment_list[1].comment_text == "testing comments2"

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name=f"purchase_orders/{test_data["purchase_order_id"]}/comments"
        )
