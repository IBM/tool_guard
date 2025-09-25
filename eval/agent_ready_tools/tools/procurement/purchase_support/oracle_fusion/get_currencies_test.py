from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_currencies import (
    oracle_fusion_get_currencies,
)


def test_oracle_fusion_get_currencies() -> None:
    """Test the getting of currencies from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "Name": "US Dollar",
                "CurrencyCode": "USD",
            }
        ]
    }

    test_data = {"currency": "US Dollar"}

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_currencies.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_currencies(currency=test_data["currency"])

        assert response
        assert response.content is not None
        assert response.content[0].currency_code == test_result["items"][0]["CurrencyCode"]
        assert response.content[0].currency == test_result["items"][0]["Name"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"currenciesLOV",
            params={"limit": 20, "offset": 0, "q": f"Name='{test_data["currency"]}'"},
        )
