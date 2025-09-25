from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_financial_insight_l3 import (
    dnb_get_company_financial_insight_l3,
)


def test_dnb_get_company_financial_insight_l3() -> None:
    """Test that the `get_company_financial_insight_l3` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "001368083",
        "cost_of_sales": 9999999999,
        "accountant_name": "John Smith",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_financial_insight_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "latestFinancials": {
                    "overview": {"costOfSales": test_data["cost_of_sales"]},
                    "accountantName": test_data["accountant_name"],
                },
                "previousFinancials": [
                    {
                        "overview": {
                            "salesRevenue": 0,
                            "grossProfit": 100,
                            "netIncome": 20,
                        }
                    }
                ],
            },
        }

        # Get Company insight
        response = dnb_get_company_financial_insight_l3(duns_number=test_data["company_id"]).content

        # Ensure that get_company_financial_insight_l3() executed and returned proper values
        assert response
        assert response.duns_number == test_data["company_id"]
        assert response.cost_of_sales == test_data["cost_of_sales"]
        assert response.accountant_name == test_data["accountant_name"]
        assert response.net_income_prev == 20
        assert response.gross_profit_prev == 100

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + str(test_data["company_id"]),
            params={"blockIDs": "companyfinancials_L3_v1"},
        )
