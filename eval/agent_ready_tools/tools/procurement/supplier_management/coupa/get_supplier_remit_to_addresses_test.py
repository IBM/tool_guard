from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_remit_to_addresses import (
    coupa_get_supplier_remit_to_addresses,
)


def test_coupa_get_supplier_remit_to_addresses() -> None:
    """Test get supplier remit-to-addresses."""
    test_rta = {
        "id": "1234",
        "name": "test-rta",
        "active": True,
        "street1": "123 Fake Street",
        "street2": "Apt 1",
        "city": "Springfield",
        "state": "IL",
        "postal-code": "12345",
        "remit-to-code": "test-rta",
        "country": {"code": "US"},
    }

    supplier_id = "1234"

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.get_supplier_remit_to_addresses.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [test_rta]

        response = coupa_get_supplier_remit_to_addresses(supplier_id=supplier_id).content

        assert response

        mock_client.get_request_list.assert_called_once_with(
            resource_name=f"suppliers/{supplier_id}/addresses",
            params={
                "fields": '["id","remit-to-code","name","street1","street2","city","state",{"country":["code"]},"active","postal-code"]'
            },
        )
