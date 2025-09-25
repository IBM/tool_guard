from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.delete_requisition_line_item import (
    coupa_delete_requisition_line_item,
)


def test_coupa_delete_requisition_line_item() -> None:
    """Test that `delete_requisition_line_item` builds correct payload and returns True on
    success."""
    # Define test data:
    test_data = {
        "requisition_id": 5309,
        "line_num": 1,
        "line_id": 9912,
        "description": "Updated item description",
        "unit_price": 49.99,
        "quantity": 10,
        "supplier_id": 2001,
        "billing_account_id": 3001,
    }

    mock_requisition_response = {
        "requisition-lines": [
            {
                "id": test_data["line_id"],
                "line-num": test_data["line_num"],
            }
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.delete_requisition_line_item.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_requisition_response
        mock_client.delete_request.return_value = 200

        # Update a requisition line item
        result = coupa_delete_requisition_line_item(
            requisition_id=test_data["requisition_id"],
            line_num=test_data["line_num"],
        ).content

        # Ensure that delete_requisition_line_item() executed and returned True to condition
        assert result == 200

        mock_client.get_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_id']}"
        )

        # Ensure the API call was made with expected parameters and payload
        mock_client.delete_request.assert_called_once_with(
            resource_name=f"requisition_lines/{test_data['line_id']}",
        )
