from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.search_company_by_sic import (
    MatchedCompanyDetails,
    dnb_search_company_by_sic,
)


def test_dnb_search_company_by_sic() -> None:
    """Test that the `search_company_by_sic` function returns the expected response."""

    # --- Define test data ---
    test_params = {
        "address_region": "CA",
        "address_country": "US",
        "employee_min_count": 10,
        "employee_max_count": 1000,
        "revenue_min_quantity": 500000,
        "revenue_max_quantity": 100000000,
        "ussicv4_code": ["7371", "7372"],
    }
    mock_api_response_data = {
        "duns": "123456789",
        "primary_name": "Test Company Inc.",
    }
    expected_matched_company = MatchedCompanyDetails(
        duns_number=mock_api_response_data["duns"],
        primary_name=mock_api_response_data["primary_name"],
    )

    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.search_company_by_sic.get_dnb_client"
    ) as mock_dnb_client:
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "searchCandidates": [
                {
                    "organization": {
                        "duns": mock_api_response_data["duns"],
                        "primaryName": mock_api_response_data["primary_name"],
                    },
                }
            ]
        }

        # --- Call the function under test ---
        response = dnb_search_company_by_sic(**test_params).content

        # --- Assert the results ---
        assert response is not None, "Response should not be None"
        assert isinstance(response, list), "Response should be a list"
        # This assertion should now pass because the CorpTypes loop runs only once
        assert (
            len(response) == 1
        ), f"Response list should contain one company, but got {len(response)}"
        assert (
            response[0] == expected_matched_company
        ), "The returned company does not match expected data"
        assert response[0].duns_number == expected_matched_company.duns_number
        assert response[0].primary_name == expected_matched_company.primary_name

        # --- Assert the API call ---
        mock_dnb_client.assert_called_once()  # Ensure client was requested

        # Construct the expected payload
        expected_search_criteria = {
            "countryISOAlpha2Code": test_params["address_country"],
            "numberOfEmployees": {
                "minimumValue": test_params["employee_min_count"],
                "maximumValue": test_params["employee_max_count"],
            },
            "yearlyRevenue": {
                "minimumValue": test_params["revenue_min_quantity"],
                "maximumValue": test_params["revenue_max_quantity"],
            },
            "addressRegion": test_params["address_region"],
            "usSicV4": test_params["ussicv4_code"],
        }

        # Check the arguments of the call to post_request
        # Since the loop now runs only once, assert_called_once_with is appropriate
        mock_client.post_request.assert_called_once_with(
            version="v1",
            category="search",
            endpoint="criteria",
            data=expected_search_criteria,
        )
