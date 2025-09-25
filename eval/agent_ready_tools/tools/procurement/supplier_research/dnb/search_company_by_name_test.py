from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.search_company_by_name import (
    dnb_search_company_by_name,
)


def test_dnb_search_company_by_name() -> None:
    """Test that the `search_company_by_name` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "001368083",
        "name": "International Business Machines Corporation",
        "short_name": "IBM",
        "country": "US",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.search_company_by_name.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "matchCandidates": [
                {
                    "organization": {
                        "duns": test_data["company_id"],
                        "primaryName": test_data["name"],
                    },
                    "matchQualityInformation": {"nameMatchScore": 0.99},
                }
            ]
        }

        # Get country details by short name
        response = dnb_search_company_by_name(
            search_query=test_data["short_name"], country=test_data["country"]
        ).content

        # Ensure that search_company_by_name() executed and returned proper values
        assert response
        assert len(response)
        assert response[0].primary_name == test_data["name"]
        assert response[0].duns_number == test_data["company_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "match",
            "cleanseMatch",
            params={
                "name": test_data["short_name"],
                "countryISOAlpha2Code": test_data["country"],
            },
        )
