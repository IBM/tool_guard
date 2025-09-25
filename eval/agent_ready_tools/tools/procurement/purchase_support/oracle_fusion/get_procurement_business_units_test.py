from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_procurement_business_units import (
    oracle_fusion_get_procurement_business_units,
)


def test_oracle_fusion_get_procurement_business_units() -> None:
    """Tests the getting of procurement business units from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "ProcurementBUId": 300000002168484,
                "ProcurementBU": "US1 Business Unit",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_procurement_business_units.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_procurement_business_units()

        assert response
        assert response.content is not None
        assert (
            response.content[0].procurement_business_unit_id
            == test_result["items"][0]["ProcurementBUId"]
        )
        assert (
            response.content[0].procurement_business_unit
            == test_result["items"][0]["ProcurementBU"]
        )

        mock_client.get_request.assert_called_once_with(
            resource_name=f"procurementBusinessUnitsLOV",
            params={"limit": 20, "offset": 0},
        )
