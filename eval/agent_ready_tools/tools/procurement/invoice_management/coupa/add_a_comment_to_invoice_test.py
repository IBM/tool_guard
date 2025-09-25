from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.add_a_comment_to_invoice import (
    coupa_add_a_comment_to_invoice,
)


def test_coupa_add_a_comment_to_invoice() -> None:
    """Test that the `add_a_comment_to_invoice` function returns the expected response."""

    # Define test data:
    test_data = {
        "invoice_id": "713513",
        "comment": "test comment",
        "comment_id": 123456,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.add_a_comment_to_invoice.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["comment_id"],
        }

        # Add comment to invoice
        response = coupa_add_a_comment_to_invoice(
            invoice_id=test_data["invoice_id"], comment=test_data["comment"]
        ).content

        # Ensure that add_a_comment_to_invoice_coupa() executed and returned proper values
        assert response
        assert response.comment_id == test_data["comment_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}/comments",
            payload={
                "comments": f"{test_data['comment']}",
                "commentable-id": f"{test_data['invoice_id']}",
                "commentable-type": "InvoiceHeader",
            },
        )
