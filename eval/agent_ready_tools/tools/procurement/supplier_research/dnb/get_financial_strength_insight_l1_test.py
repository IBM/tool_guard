from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_financial_strength_insight_l1 import (
    dnb_get_company_financial_strength,
)


def test_dnb_get_financial_strength_insight_l1() -> None:
    """Test that the `get_financial_strength_insight_l1` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "001368083",
        "name": "International Business Machines Corporation",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_financial_strength_insight_l1.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "primaryName": test_data["name"],
                "dnbAssessment": {
                    "financialCondition": {
                        "description": "50B Profit",
                    },
                    "failureScore": {"classScoreDescription": "F - far below average"},
                    "delinquencyScore": {"classScoreDescription": "F - far below average"},
                },
            },
        }

        # Get company financial strength
        response = dnb_get_company_financial_strength(duns_number=test_data["company_id"]).content

        # Ensure that get_company_financial_strength() executed and returned proper values
        assert response
        assert response.primary_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_data["company_id"],
            params={"blockIDs": "financialstrengthinsight_L1_v1"},
        )
