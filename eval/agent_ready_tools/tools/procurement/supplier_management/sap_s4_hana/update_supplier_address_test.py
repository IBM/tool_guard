from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaBusinessPartner,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier_address import (
    sap_s4_hana_update_supplier_address,
)


def test_update_supplier_address() -> None:
    """Test that the update_supplier_address tool updates address successfully."""

    # Define test data
    test_data = {
        "supplier_id": "1074",
        "business_partner_id": "1074",
        "address_id": "25530",
        "address_line": "123 Main St",
        "city": "San Francisco",
        "country": "US",
        "postal_code": "94105",
        "house_number": "1-141",
        "region": "CA",
        "http_code": 204,
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier_address.get_business_partner_id_of_supplier"
    ) as mock_business_partner, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier_address.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": test_data["http_code"]}
        mock_client.get_request.return_value = {
            "response": {"d": {"results": [{"BusinessPartner": test_data["business_partner_id"]}]}}
        }

        # Ensure the mock returns the correct business partner ID
        mock_business_partner.return_value = ToolResponse(
            success=True,
            message="Success",
            content=S4HanaBusinessPartner(
                business_partner_id=str(test_data["business_partner_id"])
            ),
        )

        # Call the function under test
        response = sap_s4_hana_update_supplier_address(
            supplier_id=test_data["supplier_id"],
            address_id=test_data["address_id"],
            address_line=test_data["address_line"],
            city=test_data["city"],
            country=test_data["country"],
            postal_code=test_data["postal_code"],
            house_number=test_data["house_number"],
            region=test_data["region"],
        )

        # Ensure that update_supplier_address() executed and returned proper values
        assert response
        assert response.content.http_code == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=f"API_BUSINESS_PARTNER/A_BusinessPartnerAddress(BusinessPartner='{test_data["business_partner_id"]}',AddressID='{test_data['address_id']}')",
            payload={
                "d": {
                    "StreetName": test_data["address_line"],
                    "CityName": test_data["city"],
                    "Country": test_data["country"],
                    "PostalCode": test_data["postal_code"],
                    "HouseNumber": test_data["house_number"],
                    "Region": test_data["region"],
                }
            },
        )
