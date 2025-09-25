import copy
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.search_company_by_criteria import (
    search_company_by_criteria,
)


def test_search_company_by_name() -> None:
    """Test that the `search_company_by_criteria` function returns the expected response."""

    # Define test data:
    # test_request = {
    #     "address_country": "NZ",
    #     "industry_description": "Railroad",
    # }
    test_request = {
        "address_country": "NZ",
        "ussicv4_code": "7353",
    }

    # missing response parameter, as a test
    test_response: Dict[str, Any] = {
        "businessEntityType": {"description": "Corporation", "dnbCode": 451},
        "corporateLinkage": {
            "familytreeRolesPlayed": [{"description": "Subsidiary", "dnbCode": 9159}],
            "globalUltimate": {
                "duns": "748723920",
                "primaryAddress": {"addressCountry": {"isoAlpha2Code": "NZ"}},
                "primaryName": "EMPIRE CAPITAL " "HOLDINGS COMPANY " "LIMITED",
            },
            "globalUltimateFamilyTreeMembersCount": 5,
            "isBranch": False,
            "parent": {
                "duns": "748723920",
                "primaryName": "EMPIRE CAPITAL HOLDINGS " "COMPANY LIMITED",
            },
        },
        "duns": "758604609",
        "dunsControlStatus": {
            "isDelisted": False,
            "isMailUndeliverable": False,
            "isMarketable": True,
            "isOutOfBusiness": False,
            "subjectHandlingDetails": [{"description": "Skeletal " "Record", "dnbCode": 9161}],
        },
        "financials": [{"yearlyRevenue": [{"currency": "USD", "value": 86710}]}],
        "industryCodes": [
            {
                "code": "532412",
                "description": "Construction, Mining, and Forestry "
                "Machinery and Equipment Rental and "
                "Leasing",
                "priority": 1,
                "typeDescription": "North American Industry " "Classification System 2022",
                "typeDnbCode": 37788,
            },
            {
                "code": "73530000",
                "description": "Heavy construction equipment rental",
                "priority": 1,
                "typeDescription": "D&B Standard Industry Code",
                "typeDnbCode": 3599,
            },
            {
                "code": "176",
                "description": "Specialty Construction Trade " "Contractors",
                "priority": 1,
                "typeDescription": "D&B Hoovers Industry Classification",
                "typeDnbCode": 35912,
            },
        ],
        "isFortune1000Listed": False,
        "isPubliclyTradedCompany": False,
        "isStandalone": False,
        "numberOfEmployees": [
            {
                "informationScopeDescription": "Consolidated",
                "informationScopeDnBCode": 9067,
                "reliabilityDescription": "Modelled",
                "reliabilityDnBCode": 9094,
                "value": 20,
            },
            {
                "informationScopeDescription": "Individual",
                "informationScopeDnBCode": 9066,
                "reliabilityDescription": "Modelled",
                "reliabilityDnBCode": 9094,
                "value": 20,
            },
        ],
        "primaryAddress": {
            "addressCountry": {"isoAlpha2Code": "NZ", "name": "New Zealand"},
            "addressLocality": {"name": "Auckland"},
            "latitude": -36.81624,
            "longitude": 174.59997,
            "postalCode": "0814",
            "streetAddress": {"line1": "18/4 Spring Garden Ave", "line2": "Westgate"},
        },
        "primaryIndustryCodes": [
            {"usSicV4": "7353", "usSicV4Description": "Heavy construction " "equipment rental"}
        ],
        "primaryName": "VULCANUS MACHINERY MANAGEMENT LIMITED",
        "registeredAddress": {
            "addressCountry": {"isoAlpha2Code": "NZ", "name": "New Zealand"},
            "addressLocality": {"name": "Auckland"},
            "addressRegion": {"name": "AUCKLAND"},
            "postalCode": "0814",
            "streetAddress": {"line1": "18/4 Spring Garden Ave", "line2": "Westgate"},
        },
        "registrationNumbers": [
            {
                "registrationNumber": "9429051202880",
                "typeDescription": "Business Number (NZ)",
                "typeDnBCode": 33961,
            },
            {
                "registrationNumber": "8667566",
                "typeDescription": "Company Number (NZ)",
                "typeDnBCode": 578,
            },
        ],
    }

    test_response_unprocessed = copy.deepcopy(test_response)

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.search_company_by_criteria.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "searchCandidates": [
                {
                    "displaySequence": 1,
                    "organization": test_response,
                }
            ]
        }

        # Search company by criteria
        response = search_company_by_criteria(
            address_country=test_request["address_country"],
            ussicv4_code=test_request["ussicv4_code"],
        )

        # Ensure that search_company_by_criteria() executed and returned proper values
        assert response
        assert len(response)
        assert response[0].primary_name == test_response_unprocessed["primaryName"]
        assert response[0].duns_number == test_response_unprocessed["duns"]
        assert (
            response[0].number_of_employees
            == test_response_unprocessed["numberOfEmployees"][0]["value"]
        )
        assert (
            response[0].yearly_revenue_value
            == test_response_unprocessed["financials"][0]["yearlyRevenue"][0]["value"]
        )
        assert (
            response[0].industry_name
            == test_response_unprocessed["primaryIndustryCodes"][0]["usSicV4Description"]
        )
        assert (
            response[0].address_country
            == test_response_unprocessed["primaryAddress"]["addressCountry"]["isoAlpha2Code"]
        )
        assert response[0].address_region == ""  # missing parameter

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_with(
            version="v1",
            category="search",
            endpoint="criteria",
            data={
                "globalUltimateCountryISOAlpha2Code": test_request["address_country"],
                "locationNavigatorType": "countryISOAlpha2Code",
                "numberOfEmployees": {
                    "minimumValue": 1,
                    "maximumValue": 999999,
                },
                "yearlyRevenue": {
                    "minimumValue": 1,
                    "maximumValue": 100000000000000,
                },
                "usSicV4": [test_request["ussicv4_code"]],
                "searchTerm": "OOO",
            },
        )
