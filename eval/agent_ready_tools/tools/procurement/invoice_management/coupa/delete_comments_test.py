from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.delete_comments import (
    coupa_delete_a_comment_of_an_invoice,
)


def test_coupa_delete_a_comment_of_an_invoice() -> None:
    """Test that the `coupa_delete_a_comment_of_an_invoice` function returns the expected
    response."""

    # Define test data:
    test_data = {"invoice_id": 1234, "comment_id": 2}

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.delete_comments.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.delete_request.return_value = 200
        response = coupa_delete_a_comment_of_an_invoice(
            test_data["invoice_id"], test_data["comment_id"]
        ).content
        assert response
