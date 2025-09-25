from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier import (
    coupa_update_supplier_details,
)


def test_coupa_update_supplier_details() -> None:
    """Test update supplier using a mock client."""
    test_data = {
        "name": "test-supplier",
        "po-email": "testemail@email.com",
        "invoice-matching-level": "2-way",
        "po-method": "email",
        "po-change-method": "email",
    }

    supplier_id = 1234

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": supplier_id,
        }

        response = coupa_update_supplier_details(
            supplier_id=supplier_id,
            name=test_data["name"],
            po_email=test_data["po-email"],
            invoice_matching_level=test_data["invoice-matching-level"],
            po_method=test_data["po-method"],
            po_change_method=test_data["po-change-method"],
        ).content

        assert response
        assert response.id == supplier_id

        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{supplier_id}",
            params={
                "fields": '["id","name","po-email","invoice-matching-level","po-method","po-change-method"]'
            },
            payload=test_data,
        )
