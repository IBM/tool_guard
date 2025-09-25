from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.add_item_to_requisition import (
    coupa_add_item_to_requisition,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id_test import (
    mock_requisition_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaRequisition,
)


def test_coupa_add_item_to_requisition() -> None:
    """Test that the `add_item_to_requisition_coupa` function returns the expected response."""

    # Define test data:
    test_data = mock_requisition_response()

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.add_item_to_requisition.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = test_data

        # Add item to a requisition
        response: CoupaRequisition = coupa_add_item_to_requisition(
            requisition_id=test_data["id"],
            description=test_data["requisition-lines"][0]["description"],
            unit_price=test_data["requisition-lines"][0]["unit-price"],
            quantity=test_data["requisition-lines"][0]["quantity"],
            supplier_id=test_data["requisition-lines"][0]["supplier"]["id"],
            billing_account_id=test_data["requisition-lines"][0]["account"]["id"],
        ).content

        # Ensure that add_item_to_requisition_coupa() executed and returned proper values
        assert response
        assert response.id == test_data["id"]
        assert response.requisition_lines
        response_req_line_0 = response.requisition_lines[0]
        test_req_line_0 = test_data["requisition-lines"][0]
        assert response_req_line_0.description == test_req_line_0["description"]
        assert response_req_line_0.unit_price == test_req_line_0["unit-price"]
        assert response_req_line_0.quantity == test_req_line_0["quantity"]
        assert response_req_line_0.supplier_id == test_req_line_0["supplier"]["id"]
        assert response_req_line_0.billing_account_id == test_req_line_0["account"]["id"]

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['id']}",
            payload={
                "requisition-lines": [
                    {
                        "description": test_data["requisition-lines"][0]["description"],
                        "unit-price": test_data["requisition-lines"][0]["unit-price"],
                        "quantity": test_data["requisition-lines"][0]["quantity"],
                        "supplier": {"id": test_data["requisition-lines"][0]["supplier"]["id"]},
                        "account": {"id": test_data["requisition-lines"][0]["account"]["id"]},
                    }
                ]
            },
        )
