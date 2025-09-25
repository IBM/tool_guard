from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_filing_insight_l3 import (
    dnb_get_company_filing_insight_l3,
)


def test_dnb_get_company_filing_insight_l3() -> None:
    """Test that the `get_company_filing_insight_l3` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "001368083",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_filing_insight_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "legalEvents": {
                    "hasBankruptcy": 0,
                    "hasJudgments": 0,
                    "hasLiquidation": 0,
                },
                "significantEvents": {"hasControlChange": 0},
            },
        }

        # Get Company insight
        response = dnb_get_company_filing_insight_l3(duns_number=test_data["company_id"]).content

        # Ensure that get_company_filing_insight_l3() executed and returned proper values
        assert response
        assert response.duns_number == test_data["company_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_data["company_id"],
            params={"blockIDs": "eventfilings_L3_v1"},
        )
