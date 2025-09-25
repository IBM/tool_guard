from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.get_industry_peers_by_name import (
    get_industry_peers_by_name,
)


def test_get_industry_peers_by_name() -> None:
    """Test that the `get_industry_peers_by_name` function returns the expected response."""

    # Define test data:
    test_data = {
        "search_usSICV4": "2844",
        "primary_name": "The Procter & Gamble Company",
        "duns_number": "001316827",
        "address_country": "United States",
        "industry_name": "Mfg toilet preparations",
        "number_of_employees": "108000",
        "yearly_revenue_value": "8.4039E10",
        "yearly_revenue_currency": "USD",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_industry_peers_by_name.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "searchCandidates": [
                {
                    "displaySequence": 1,
                    "organization": {
                        "primaryName": test_data["primary_name"],
                        "duns": test_data["duns_number"],
                        "primaryAddress": {
                            "addressCountry": {
                                "name": test_data["address_country"],
                            },
                        },
                        "primaryIndustryCodes": [
                            {"usSicV4Description": test_data["industry_name"]}
                        ],
                        "numberOfEmployees": [
                            {
                                "value": test_data["number_of_employees"],
                                "informationScopeDescription": "Consolidated",
                            },
                        ],
                        "financials": [
                            {
                                "yearlyRevenue": [
                                    {
                                        "value": test_data["yearly_revenue_value"],
                                        "currency": test_data["yearly_revenue_currency"],
                                    }
                                ]
                            }
                        ],
                    },
                },
            ]
        }

        response = get_industry_peers_by_name(industry_code=test_data["search_usSICV4"])

        # Ensure that get_industry_peers_by_name() executed and returned proper values
        assert response
        assert len(response)
        assert response[0].primary_name == test_data["primary_name"]
        assert response[0].duns_number == test_data["duns_number"]
        assert response[0].address_country == test_data["address_country"]
        assert response[0].industry_name == test_data["industry_name"]
        assert response[0].number_of_employees == int(test_data["number_of_employees"])
        assert response[0].yearly_revenue_value == float(test_data["yearly_revenue_value"])
        assert response[0].yearly_revenue_currency == test_data["yearly_revenue_currency"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_with(
            version="v1",
            category="search",
            endpoint="criteria",
            data={
                "usSicV4": [test_data["search_usSICV4"]],
            },
        )
