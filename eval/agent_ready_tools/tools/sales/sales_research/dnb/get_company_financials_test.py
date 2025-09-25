from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.get_company_financials import (
    CompanyFinancialsResponse,
    get_company_financials,
)


def test_get_company_financials() -> None:
    """Test that the `get_company_financials` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "804735132",
        "name": "International Business Machines Corporation",
        "country": "US",
        "units": "1000 USD",  # Change this to string to match pydantic class
        "sales_revenue": 100,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_company_financials.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "primaryName": test_data["name"],
                "countryISOAlpha2Code": test_data["country"],
                "duns": test_data["company_id"],
                "latestFiscalFinancials": {
                    "units": test_data["units"],
                    "overview": {"salesRevenue": test_data["sales_revenue"]},
                },
            },
        }

        # Get company financials
        response = get_company_financials(duns_number=test_data["company_id"])

        # Ensure that get_company_financials() executed and returned proper values
        assert response
        assert isinstance(response, CompanyFinancialsResponse)
        assert response.name == test_data["name"]
        assert response.units == test_data["units"]
        assert response.sales_revenue == test_data["sales_revenue"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            version="v1",
            category="data",
            endpoint="duns",
            path_parameter=test_data["company_id"],
            params={"blockIDs": "companyfinancials_L1_v3"},
        )
