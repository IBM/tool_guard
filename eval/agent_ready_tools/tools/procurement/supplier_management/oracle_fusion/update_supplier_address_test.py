from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_address import (
    oracle_fusion_update_supplier_address,
)


def test_oracle_fusion_update_supplier_address() -> None:
    """Tests oracle_fusion_update_supplier_address using a mock client."""

    test_data = {
        "supplier_id": "300100153044388",
        "address_id": "300100153044503",
        "street1": "123 broadway St.",
        "city": "OAKLAND",
        "country_code": "US",
        "country": "United States",
        "postal_code": "94607",
        "email": "updated@example.com",
        "name": "Updated HQ",
        "street2": "Suite 500",
        "state": "CA",
        "purpose": ["payment", "procurement"],
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.update_supplier_address.get_oracle_fusion_client"
    ) as mock_oracle_client:
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.patch_request.return_value = {
            "SupplierAddressId": test_data["address_id"],
            "AddressName": test_data["name"],
            "CountryCode": test_data["country_code"],
            "Country": test_data["country"],
            "City": test_data["city"],
            "PostalCode": test_data["postal_code"],
            "Email": test_data["email"],
            "AddressPurposePaymentFlag": "Y",
            "AddressPurposeProcurementFlag": "Y",
        }

        response = oracle_fusion_update_supplier_address(
            supplier_id=test_data["supplier_id"],
            address_id=test_data["address_id"],
            street1=test_data["street1"],
            city=test_data["city"],
            country_code=test_data["country_code"],
            country=test_data["country"],
            postal_code=test_data["postal_code"],
            email=test_data["email"],
            name=test_data["name"],
            street2=test_data["street2"],
            state=test_data["state"],
            purpose=test_data["purpose"],
        ).content

        assert response
        assert response.supplier_id == test_data["supplier_id"]
        assert response.address_id == test_data["address_id"]
        assert "raw_response" in response.__dict__

        mock_client.patch_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/child/addresses/{test_data['address_id']}",
            payload={
                "AddressName": test_data["name"],
                "AddressLine1": test_data["street1"],
                "AddressLine2": test_data["street2"],
                "City": test_data["city"],
                "State": test_data["state"],
                "CountryCode": test_data["country_code"],
                "Country": test_data["country"],
                "PostalCode": test_data["postal_code"],
                "Email": test_data["email"],
                "AddressPurposePaymentFlag": "Y",
                "AddressPurposeProcurementFlag": "Y",
            },
        )
