from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_ship_to_locations import (
    oracle_fusion_get_ship_to_locations,
)


def test_oracle_fusion_get_ship_to_locations() -> None:
    """Tests the getting of ship-to locations from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "LocationId": 300000006267076,
                "LocationName": "Riverbed Technology Pte. Ltd.",
                "Address": "., .,  238873",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_ship_to_locations.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_ship_to_locations()

        assert response
        assert response.content is not None
        assert response.content[0].location_id == test_result["items"][0]["LocationId"]
        assert response.content[0].location_name == test_result["items"][0]["LocationName"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"b2bShipToLocationsLOV",
            params={"limit": 20, "offset": 0, "q": "SetName='Common Set'"},
        )
