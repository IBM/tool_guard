from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_special_handling_types import (
    oracle_fusion_get_special_handling_types,
)


def test_oracle_fusion_get_special_handling_types() -> None:
    """Tests the getting of special handling types from Oracle Fusion using a mock client."""

    test_result = {
        "items": [
            {
                "SpecialHandlingType": "Bill Only",
                "SpecialHandlingTypeCode": "ORA_PO_BILL_ONLY",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_special_handling_types.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_result

        response = oracle_fusion_get_special_handling_types()

        assert response
        assert response.content is not None
        assert (
            response.content[0].special_handling_type
            == test_result["items"][0]["SpecialHandlingType"]
        )
        assert (
            response.content[0].special_handling_type_code
            == test_result["items"][0]["SpecialHandlingTypeCode"]
        )

        mock_client.get_request.assert_called_once_with(
            resource_name=f"specialHandlingTypes",
            params={"limit": 20, "offset": 0},
        )
