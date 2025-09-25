from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_payment_insight_l3 import (
    dnb_get_company_payment_insight_l3,
)


def test_dnb_get_company_payment_insight_l3() -> None:
    """Test that the `get_company_payment_insight_l3` function returns the expected response."""

    # Define test data:
    test_data = {"duns_number": "804735132", "paydex_score": "12"}

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_payment_insight_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["duns_number"],
                "businessTrading": [{"summary": [{"paydexScore": test_data["paydex_score"]}]}],
            }
        }
        # Get purchase by ID
        response = dnb_get_company_payment_insight_l3(duns_number=test_data["duns_number"]).content

        # Ensure that get_company_payment_insight_l3() executed and returned proper values
        assert response
        assert response.duns_number == test_data["duns_number"]
        assert response.paydex_score == test_data["paydex_score"]

        # Ensure the API call was made with expected parameters
        params = {"blockIDs": "paymentinsight_L3_v1"}
        mock_client.get_request.assert_called_once_with(
            "v1", "data", "duns/" + test_data["duns_number"], params=params
        )
