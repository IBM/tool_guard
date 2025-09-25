from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_countries import (
    S4HANACountriesResponse,
    S4HANACountry,
    sap_s4_hana_get_countries,
)


def test_sap_s4_hana_get_countries() -> None:
    """Tests that the countries can be retrieved by the `sap_s4_hana_get_countries` tool in SAP S4
    HANA."""

    # Define test data
    test_data: dict[str, str] = {
        "country_code": "IN",
        "country_name": "India",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_countries.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "Country": test_data["country_code"],
                            "CountryName": test_data["country_name"],
                        }
                    ]
                }
            }
        }

        # Call the function
        response = sap_s4_hana_get_countries(country_name=test_data["country_name"]).content
        # Verify that the country details matches the expected data
        expected_response = S4HANACountriesResponse(
            countries_list=[
                S4HANACountry(
                    country_code=test_data["country_code"],
                    country_name=test_data["country_name"],
                )
            ]
        )

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_COUNTRY_SRV/A_CountryText",
            filter_expr=f"Language eq 'EN' and CountryName eq '{test_data["country_name"]}'",
            params={"$top": 20, "$skip": 0},
        )
