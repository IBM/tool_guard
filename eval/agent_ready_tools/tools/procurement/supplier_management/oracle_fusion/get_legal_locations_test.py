from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_legal_locations import (
    oracle_fusion_get_legal_locations,
)


def test_oracle_fusion_get_legal_locations() -> None:
    """Test the getting of legal locations from Oracle Fusion using a mock client."""
    legal_locations = {
        "items": [
            {
                "LocationId": "300000015729683",
                "FormattedAddress": "Queensbridge Street/Southbank VICTORIA/AUSTRALIA",
            }
        ]
    }

    test_data = {"tax_registration_id": "300000025229353"}

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_legal_locations.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = legal_locations

        response = oracle_fusion_get_legal_locations(
            tax_registration_id=test_data["tax_registration_id"]
        )

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name=f"taxRegistrations/{test_data["tax_registration_id"]}/lov/legalLocations",
            params={"limit": 10, "offset": 0},
        )
