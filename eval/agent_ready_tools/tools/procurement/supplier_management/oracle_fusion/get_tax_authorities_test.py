from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_tax_authorities import (
    oracle_fusion_get_tax_authorities,
)


def test_oracle_fusion_get_tax_authorities() -> None:
    """Test the getting of all tax authorities from Oracle Fusion using a mock client."""
    tax_authorities = {
        "items": [
            {
                "PartyTaxProfileId": "300000009708504",
                "PartyName": "IBM Inc",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_tax_authorities.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = tax_authorities

        response = oracle_fusion_get_tax_authorities()

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="taxAuthorityProfiles",
            params={"limit": 10, "offset": 0},
        )
