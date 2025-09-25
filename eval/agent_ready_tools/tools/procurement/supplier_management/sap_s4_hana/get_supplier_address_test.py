from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaBusinessPartner,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_address import (
    sap_s4_hana_get_supplier_address,
)


def test_get_supplier_address() -> None:
    """Test that the `sap_s4_hana_get_supplier_address` function returns the expected response."""

    test_data = {
        "supplier_id": "1053",
        "business_partner_id": "1053",
        "address_id": "25217",
        "street_name": "High Street",
        "house_number": "135",
        "postal_code": "334455",
        "city": "Delhi",
        "country": "IN",
        "region": "30",
        "time_zone": "INDIA",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_address.get_sap_s4_hana_client"
    ) as mock_get_client, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_address.get_business_partner_id_of_supplier"
    ) as mock_business_partner:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "AddressID": test_data["address_id"],
                            "StreetName": test_data["street_name"],
                            "HouseNumber": test_data["house_number"],
                            "PostalCode": test_data["postal_code"],
                            "CityName": test_data["city"],
                            "Country": test_data["country"],
                            "Region": test_data["region"],
                            "AddressTimeZone": test_data["time_zone"],
                        }
                    ]
                }
            }
        }

        mock_client.get_business_partner_id_of_supplier.return_value = {
            "response": {"d": {"results": [{"BusinessPartner": test_data["business_partner_id"]}]}}
        }

        # Ensure the mock returns the correct business partner ID
        mock_business_partner.return_value = ToolResponse(
            success=True,
            message="Success",
            content=S4HanaBusinessPartner(business_partner_id=test_data["business_partner_id"]),
        )

        response = sap_s4_hana_get_supplier_address(supplier_id=test_data["supplier_id"]).content

        assert response
        assert response.address_details[0].address_id == test_data["address_id"]
        assert response.address_details[0].city == test_data["city"]
        assert response.address_details[0].street_name == test_data["street_name"]

        mock_client.get_request.assert_any_call(
            entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{test_data["business_partner_id"]}')/to_BusinessPartnerAddress",
            params={"$top": 20, "$skip": 0},
        )
