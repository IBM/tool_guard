from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_remit_to_address import (
    coupa_update_supplier_remit_to_address,
)


def test_coupa_update_supplier_remit_to_address() -> None:
    """Tests `update_supplier_remit_to_address` using a mock client."""

    test_data = {
        "supplier_id": "2",
        "remit_to_address_id": "229445",
        "remit_to_code": "remyit7h17u727171",
        "name": "Remit test8",
        "street1": "Road no: 43, New town",
        "street2": "33",
        "city": "New orleons",
        "state": None,
        "postal_code": None,
        "country": None,
        "active": False,
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.update_supplier_remit_to_address.get_coupa_client"
    ) as mock_coupa_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {"id": test_data["remit_to_address_id"]}

        # Call the function under test
        response = coupa_update_supplier_remit_to_address(
            supplier_id=test_data["supplier_id"],
            remit_to_address_id=int(str(test_data["remit_to_address_id"])),
            remit_to_code=test_data["remit_to_code"],
            name=test_data["name"],
            street1=test_data["street1"],
            street2=test_data["street2"],
            city=test_data["city"],
            state=test_data["state"],
            postal_code=test_data["postal_code"],
            country=test_data["country"],
            active=test_data["active"],
        ).content

        # Ensure that coupa_update_supplier_remit_to_address() executed and returned proper values
        assert response.remit_to_address_id == int(str(test_data["remit_to_address_id"]))

        mock_client.put_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/addresses/{test_data['remit_to_address_id']}",
            payload={
                "remit-to-code": test_data["remit_to_code"],
                "name": test_data["name"],
                "street1": test_data["street1"],
                "street2": test_data["street2"],
                "city": test_data["city"],
                "active": test_data["active"],
            },
        )
