from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_comments import (
    coupa_get_requisition_comments,
)


def test_coupa_get_requisition_comments() -> None:
    """Test that the `get_requisition_comments` function returns the expected response."""

    # Define test data:
    test_data: dict[str, Any] = {
        "requisition_id": 5309,
        "comments": [
            {
                "id": 467,
                "created-at": "2025-04-11T15:36:40-07:00",
                "updated-at": "2025-04-11T15:36:40-07:00",
                "commentable-id": 5309,
                "commentable-type": "RequisitionHeader",
                "comments": "testing comments",
                "created-by": {"login": "IBMFunctionalUser"},
                "updated-by": {"login": "IBMFunctionalUser"},
            },
            {
                "id": 468,
                "created-at": "2025-04-11T15:37:24-07:00",
                "updated-at": "2025-04-11T15:37:24-07:00",
                "commentable-id": 5309,
                "commentable-type": "RequisitionHeader",
                "comments": "testing comments2",
                "created-by": {"login": "IBMFunctionalUser"},
                "updated-by": {"login": "IBMFunctionalUser"},
            },
        ],
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_comments.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data["comments"]

        # Get requisition comments
        response = coupa_get_requisition_comments(
            requisition_id=test_data["requisition_id"]
        ).content

        # Ensure that get_requisition_comments() executed and returned proper values
        assert response
        assert response.comment_list and len(response.comment_list) == 2
        assert response.comment_list[0].comment_text == "testing comments"
        assert response.comment_list[1].comment_text == "testing comments2"

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name=f"requisitions/{test_data["requisition_id"]}/comments"
        )
