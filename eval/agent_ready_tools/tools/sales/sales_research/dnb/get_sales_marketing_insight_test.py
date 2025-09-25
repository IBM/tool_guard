from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.dnb.get_sales_marketing_insight import (
    get_sales_marketing_insight,
)


def test_get_sales_market_insight() -> None:
    """Test that the `get_sales_marketing_insight` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "804735132",
        "company_name": "Gorman Manufacturing Company, Inc.",
        "country_code": "US",
        "risk_class": "Alpha",
        "risk_segment": "Charlie",
        "score": 50,
        "is_decision_hq": False,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_sales_marketing_insight.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "primaryName": test_data["company_name"],
                "countryISOAlpha2Code": test_data["country_code"],
                "salesMarketingAssessment": {
                    "marketingRiskClass": {"description": test_data["risk_class"]},
                    "materialChange": {
                        "riskSegment": {
                            "description": test_data["risk_segment"],
                        },
                    },
                    "triplePlay": {"compositeRiskScore": test_data["score"]},
                    "decisionPowerScore": test_data["score"],
                    "isDecisionHeadQuarter": test_data["is_decision_hq"],
                },
            }
        }

        # Get sales marketing insight
        response = get_sales_marketing_insight(test_data["company_id"])

        # Ensure that get_sales_marketing_insight() executed and returned proper values
        assert response
        assert response.primary_name == test_data["company_name"]
        assert response.marketing_risk_description == test_data["risk_class"]
        assert response.risk_segment_description == test_data["risk_segment"]
        assert response.composite_risk_score == test_data["score"]
        assert response.decision_power_score == test_data["score"]
        assert response.is_decision_hq == test_data["is_decision_hq"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            version="v1",
            category="data",
            endpoint="duns",
            path_parameter=test_data["company_id"],
            params={"blockIDs": "salesmarketinginsight_L3_v2"},
        )
