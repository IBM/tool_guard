from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_line_item import (
    coupa_update_requisition_line_item,
)


def test_coupa_update_requisition_line_item() -> None:
    """Test that `update_requisition_line_item` builds correct payload and returns True on
    success."""

    # Define test data:
    test_data = {
        "requisition_id": 5309,
        "line_num": 1,
        "line_id": 9912,
        "description": "Updated item description",
        "unit_price": 49.99,
        "quantity": "10",
        "supplier_id": 2001,
        "billing_account_id": 3001,
        "currency": "USD",
        "line_type": "RequisitionQuantityLine",
        "total_with_estimated_tax": "950.0",
    }

    expected_payload = {
        "description": test_data["description"],
        "unit-price": test_data["unit_price"],
        "quantity": test_data["quantity"],
        "supplier": {"id": test_data["supplier_id"]},
        "account": {"id": test_data["billing_account_id"]},
    }

    mock_requisition_response = {
        "requisition-lines": [
            {
                "id": test_data["line_id"],
                "line-num": test_data["line_num"],
                "total-with-estimated-tax": test_data["total_with_estimated_tax"],
                "line-type": test_data["line_type"],
                "currency": {"code": test_data["currency"]},
            }
            | expected_payload
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_line_item.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_requisition_response
        mock_client.put_request.return_value = mock_requisition_response["requisition-lines"][0]

        # Update a requisition line item
        result = coupa_update_requisition_line_item(
            requisition_id=test_data["requisition_id"],
            line_num=test_data["line_num"],
            description=test_data["description"],
            unit_price=test_data["unit_price"],
            quantity=test_data["quantity"],
            supplier_id=test_data["supplier_id"],
            billing_account_id=test_data["billing_account_id"],
        ).content

        # Ensure that update_requisition_line_item() executed and returns the requisition line data object
        assert result.id == test_data["line_id"]
        assert result.line_num == test_data["line_num"]
        assert result.description == test_data["description"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_id']}"
        )

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"requisition_lines/{test_data['line_id']}",
            payload=expected_payload,
        )
