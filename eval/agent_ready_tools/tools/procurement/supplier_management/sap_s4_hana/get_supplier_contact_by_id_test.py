from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_contact_by_id import (
    sap_s4_hana_get_supplier_contact_by_id,
)


def test_sap_s4_hana_get_supplier_contact_by_id() -> None:
    """Test that the `sap_s4_hana_get_supplier_contact_by_id` function returns the expected
    response."""

    test_data = {
        "person_id": "1204",
        "full_name": "test wxo",
        "first_name": "test",
        "last_name": "wxo",
        "email_address": "test.wxo@ibm.com",
        "house_number": "114",
        "street": "Church street",
        "city": "Hyderabad",
        "country": "IN",
        "postal_code": "560066",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_supplier_contact_by_id.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "BusinessPartner": test_data["person_id"],
                            "LastName": test_data["last_name"],
                            "FirstName": test_data["first_name"],
                            "BusinessPartnerName": test_data["full_name"],
                            "to_BusinessPartnerAddress": {
                                "results": [
                                    {
                                        "CityName": test_data["city"],
                                        "Country": test_data["country"],
                                        "HouseNumber": test_data["house_number"],
                                        "PostalCode": test_data["postal_code"],
                                        "StreetName": test_data["street"],
                                        "to_EmailAddress": {
                                            "results": [
                                                {"EmailAddress": test_data["email_address"]}
                                            ]
                                        },
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }

        response = sap_s4_hana_get_supplier_contact_by_id(
            contact_person_id=test_data["person_id"]
        ).content

        assert response
        assert response.persons[0].person_id == test_data["person_id"]
        assert response.persons[0].full_name == test_data["full_name"]
        assert response.persons[0].first_name == test_data["first_name"]
        assert response.persons[0].last_name == test_data["last_name"]
        assert response.persons[0].email_address == test_data["email_address"]
        assert response.persons[0].street == test_data["street"]

        mock_client.get_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_BusinessPartner",
            params={"$top": 20, "$skip": 0},
            filter_expr=f"BusinessPartnerCategory eq '1' and BusinessPartner eq '{test_data["person_id"]}'",
            expand_expr="to_BusinessPartnerAddress,to_BusinessPartnerAddress/to_EmailAddress",
        )
