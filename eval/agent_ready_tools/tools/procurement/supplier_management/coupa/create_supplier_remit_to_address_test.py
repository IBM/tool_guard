from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_remit_to_address import (
    coupa_create_supplier_remit_to_address,
)


def test_coupa_create_remit_to_address() -> None:
    """Test create supplier remit-to-address using a mock client."""
    test_country_code = "US"
    test_data: Dict[str, Any] = {
        "remit-to-code": "rta-test",
        "name": "test-rta",
        "street1": "123 Fake Street",
        "city": "Springfield",
        "state": "IL",
        "postal-code": "12345",
        "active": True,
        "country": {"code": test_country_code},
    }
    supplier_id = 5678

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_remit_to_address.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": "1234",
        }

        response = coupa_create_supplier_remit_to_address(
            supplier_id=supplier_id,
            remit_to_code=test_data["remit-to-code"],
            name=test_data["name"],
            street1=test_data["street1"],
            city=test_data["city"],
            state=test_data["state"],
            postal_code=test_data["postal-code"],
            active=test_data["active"],
            country_code=test_country_code,
        ).content

        assert response
        assert response.id == 1234

        mock_client.post_request.assert_called_once_with(
            resource_name=f"suppliers/{supplier_id}/addresses",
            params={"fields": '["id"]'},
            payload=test_data,
        )
