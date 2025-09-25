from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier_address import (
    oracle_fusion_create_supplier_address,
)


def test_oracle_fusion_create_supplier_address() -> None:
    """Tests oracle_fusion_create_supplier_address using a mock client."""

    test_data = {
        "supplier_id": "300100153044388",
        "street1": "22093 Market Street",
        "city": "SAN FRANCISCO",
        "country_code": "US",
        "country": "United States",
        "postal_code": "94102",
        "email": "eric.smith@example.com",
        "name": "HQ",
        "street2": None,
        "state": "CA",
        "purpose": ["ordering", "remit_to"],
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.create_supplier_address.get_oracle_fusion_client"
    ) as mock_oracle_client:
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "items": [
                {
                    "SupplierAddressId": "300100153044503",
                    "AddressName": test_data["name"],
                    "CountryCode": test_data["country_code"],
                    "Country": test_data["country"],
                    "City": test_data["city"],
                    "PostalCode": test_data["postal_code"],
                    "AddressPurposeOrderingFlag": "Y",
                    "AddressPurposeRemitToFlag": "Y",
                    "Email": test_data["email"],
                }
            ]
        }

        response = oracle_fusion_create_supplier_address(
            supplier_id=test_data["supplier_id"],
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
        assert response.address_id == "300100153044503"

        mock_client.post_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/child/addresses",
            payload={
                "AddressName": test_data["name"],
                "AddressLine1": test_data["street1"],
                "City": test_data["city"],
                "State": test_data["state"],
                "CountryCode": test_data["country_code"],
                "Country": test_data["country"],
                "PostalCode": test_data["postal_code"],
                "Email": test_data["email"],
                "AddressPurposeOrderingFlag": "Y",
                "AddressPurposeRemitToFlag": "Y",
            },
        )
