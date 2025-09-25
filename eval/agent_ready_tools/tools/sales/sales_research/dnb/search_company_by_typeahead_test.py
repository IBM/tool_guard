from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.search_company_by_typeahead import (
    search_company_by_typeahead,
)


def test_search_company_by_typeahead() -> None:
    """Test that the `typeahead_search` function returns the expected response."""

    # Define test data:
    test_data = {
        "search_query": "International Business Mac",
        "company_name": "International Business Machines Corporation",
        "company_id": "001368083",
        "company_country": "US",
        "company_region": "New York",
        "company_yearly_revenue": 6.2753e10,
        "company_revenue_currency": "USD",
        "company_usSicV4": "3571",
        "company_usSicV4Description": "Mfg electronic computers",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.search_company_by_typeahead.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "searchCandidates": [
                {
                    "displaySequence": 1,
                    "organization": {
                        "primaryName": test_data["company_name"],
                        "duns": test_data["company_id"],
                        "primaryAddress": {
                            "addressCountry": {"isoAlpha2Code": test_data["company_country"]},
                            "addressRegion": {"name": test_data["company_region"]},
                        },
                        "financials": [
                            {
                                "yearlyRevenue": [
                                    {
                                        "value": test_data["company_yearly_revenue"],
                                        "currency": test_data["company_revenue_currency"],
                                    }
                                ]
                            }
                        ],
                        "primaryIndustryCodes": [
                            {
                                "usSicV4": test_data["company_usSicV4"],
                                "usSicV4Description": test_data["company_usSicV4Description"],
                            }
                        ],
                    },
                }
            ]
        }

        # Search company by typehead
        response = search_company_by_typeahead(
            search_query=test_data["search_query"], country=test_data["company_country"]
        )

        # Ensure that search_company_by_typeahead() executed and returned proper values
        assert response and len(response)
        assert response[0].primary_name == "International Business Machines Corporation"
        assert response[0].duns_number == test_data["company_id"]
        assert response[0].address_country == test_data["company_country"]
        assert response[0].address_region == test_data["company_region"]
        assert response[0].yearly_revenue_value == test_data["company_yearly_revenue"]
        assert response[0].revenue_currency == test_data["company_revenue_currency"]
        assert response[0].industry_code == test_data["company_usSicV4"]
        assert response[0].industry_name == test_data["company_usSicV4Description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "search",
            "typeahead",
            params={
                "searchTerm": test_data["search_query"],
                "countryISOAlpha2Code": test_data["company_country"],
            },
        )
