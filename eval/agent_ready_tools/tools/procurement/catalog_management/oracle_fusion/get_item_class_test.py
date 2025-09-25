from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionItemClass,
)
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_item_class import (
    oracle_fusion_get_item_classes,
)


def test_get_item_classes_success() -> None:
    """Tests the successful retrieval and parsing of Item Classes."""
    mock_api_response = {
        "items": [
            {
                "ItemClass": "Root Item Class",
                "Description": "The main class for all items",
                "ItemClassId": 1000,
            },
            {
                "ItemClass": "Finished Goods",
                "Description": "Items ready for sale",
                "ItemClassId": 1001,
            },
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_item_class.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_api_response

        tool_response = oracle_fusion_get_item_classes()

        assert tool_response.success is True
        assert "Successfully retrieved 2 Item Classes" in tool_response.message
        assert tool_response.content is not None
        assert len(tool_response.content) == 2

        output_item_class = tool_response.content[0]
        assert isinstance(output_item_class, OracleFusionItemClass)
        assert output_item_class.item_class_name == "Root Item Class"

        mock_client.get_request.assert_called_once_with(resource_name="itemClasses", params={})


def test_get_item_classes_with_query() -> None:
    """Tests the retrieval of item classes with a search query."""
    mock_api_response = {
        "items": [
            {
                "ItemClass": "Root Item Class",
                "Description": "The main class for all items",
                "ItemClassId": 1000,
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_item_class.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_api_response

        tool_response = oracle_fusion_get_item_classes()

        assert tool_response.success is True
        assert "Successfully retrieved 1 Item Class" in tool_response.message

        mock_client.get_request.assert_called_once_with(resource_name="itemClasses", params={})


def test_get_item_classes_api_error() -> None:
    """Tests how the function handles an error response from the API."""
    mock_api_error_response = {"error": "Authentication failure"}

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_item_class.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_api_error_response

        tool_response = oracle_fusion_get_item_classes()

        assert tool_response.success is False
        assert "Authentication failure" in tool_response.message
        assert tool_response.content is None
