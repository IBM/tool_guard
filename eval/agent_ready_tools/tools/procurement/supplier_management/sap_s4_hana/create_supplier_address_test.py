from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaBusinessPartner,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier_address import (
    sap_s4_hana_create_supplier_address,
)


def test_create_supplier_address() -> None:
    """Test that the create_supplier_address tool creates address successfully."""

    # Define test data
    test_data = {
        "supplier_id": "1074",
        "address_id": "26233",
        "business_partner_id": "1074",
        "address_line": "",
        "city": "Hyderabad",
        "country": "IN",
        "postal_code": "500004",
        "house_number": None,
        "region": None,
        "address_timezone": None,
        "http_code": 201,
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier_address.get_business_partner_id_of_supplier"
    ) as mock_business_partner, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.create_supplier_address.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "BusinessPartner": test_data["supplier_id"],
                "AddressID": test_data["address_id"],
            },
        }
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "BusinessPartner": test_data["business_partner_id"],
                        }
                    ]
                }
            }
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
        response = sap_s4_hana_create_supplier_address(
            supplier_id=test_data["supplier_id"],
            address_line=test_data["address_line"],
            city=test_data["city"],
            country=test_data["country"],
            postal_code=test_data["postal_code"],
            house_number=test_data["house_number"],
            region=test_data["region"],
            address_timezone=test_data["address_timezone"],
        ).content

        # Ensure that create_supplier_address() executed and returned proper values
        assert response
        assert response.supplier_id == test_data["supplier_id"]
        assert response.address_id == test_data["address_id"]

        mock_client.post_request.assert_called_once_with(
            entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{test_data['business_partner_id']}')/to_BusinessPartnerAddress",
            payload={
                "CityName": test_data["city"],
                "Country": test_data["country"],
                "PostalCode": test_data["postal_code"],
            },
        )
