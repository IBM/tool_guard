from typing import Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier import (
    coupa_create_supplier,
)
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaPurchaseOrderType,
    InvoiceMatchingLevel,
)


def test_coupa_create_supplier_types() -> None:
    """Test for create supplier simple without upserting new supplier."""
    invoice_matching_level = "2-way"
    po_method = "email"

    try:
        InvoiceMatchingLevel(invoice_matching_level)
        CoupaPurchaseOrderType(po_method)
    except Exception as exc:
        raise TypeError from exc


def test_coupa_create_supplier_mock() -> None:
    """Test create supplier using a mock client."""
    test_data: Dict[str, str] = {
        "name": "test-supplier",
        "po-email": "testemail@email.com",
        "invoice-matching-level": "2-way",
        "po-method": "email",
        "po-change-method": "email",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": 1234,
        }

        response = coupa_create_supplier(
            name=test_data["name"],
            po_email=test_data["po-email"],
            invoice_matching_level=test_data["invoice-matching-level"],
            po_method=test_data["po-method"],
            po_change_method=test_data["po-change-method"],
        ).content

        assert response
        assert response.id == 1234

        mock_client.post_request.assert_called_once_with(
            resource_name="suppliers", params={"fields": '["id"]'}, payload=test_data
        )
