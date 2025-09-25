from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionUOM,
)
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_units_of_measure import (
    oracle_fusion_get_units_of_measure,
)


def test_get_units_of_measure_success() -> None:
    """Tests the successful retrieval of Units of Measure."""
    mock_api_response = {
        "items": [
            {
                "UOMCode": "Ea",
                "Description": "Each",
                "UOMClassName": "Quantity",
                "BaseUnitFlag": True,
            },
            {
                "UOMCode": "Kg",
                "Description": "Kilogram",
                "UOMClassName": "Weight",
                "BaseUnitFlag": True,
            },
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_units_of_measure.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_api_response

        tool_response = oracle_fusion_get_units_of_measure()

        assert tool_response.success is True
        assert "Successfully retrieved 2 Units of Measure" in tool_response.message
        assert tool_response.content is not None
        assert len(tool_response.content) == 2

        output_uom = tool_response.content[0]
        assert isinstance(output_uom, OracleFusionUOM)
        assert output_uom.uom_code == "Ea"

        mock_client.get_request.assert_called_once_with(resource_name="unitsOfMeasure", params={})


def test_get_units_of_measure_api_error() -> None:
    """Tests how the function handles an error response from the API."""
    mock_api_error_response = {"error": "Service temporarily unavailable"}

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_units_of_measure.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_api_error_response

        tool_response = oracle_fusion_get_units_of_measure()

        assert tool_response.success is False
        assert "Service temporarily unavailable" in tool_response.message
        assert tool_response.content is None
