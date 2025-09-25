from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.get_all_suppliers import (
    coupa_get_all_suppliers,
)


def test_coupa_get_all_suppliers() -> None:
    """Test get all suppliers using a mock client."""
    test_supplier = {
        "id": 1234,
        "number": "5678",
        "status": "active",
        "name": "test-supplier",
        "primary-contact": {"email": "test-supplier@gmail.com"},
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.get_all_suppliers.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [test_supplier]

        response = coupa_get_all_suppliers(status="active").content

        assert response

        mock_client.get_request_list.assert_called_once_with(
            resource_name="suppliers",
            params={
                "fields": '["id","number","status","name",{"primary_contact":["email"]}]',
                "status": "active",
                "limit": 10,
                "offset": 0,
            },
        )
