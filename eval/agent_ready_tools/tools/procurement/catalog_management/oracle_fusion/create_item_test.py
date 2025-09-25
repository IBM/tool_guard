from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionItem,
)
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.create_item import (
    oracle_fusion_create_item,
)


def test_create_supplier_item_success() -> None:
    """Tests the successful creation of a supplier item, including categories."""
    org_code = "0000"
    item_num = "ROBOT-TEST-001"
    item_desc = "A test item for robotic automation"
    item_class = "Root Item Class"

    mock_api_response = {
        "OrganizationCode": org_code,
        "ItemId": 98765,
        "ItemNumber": item_num,
        "ItemDescription": item_desc,
        "ItemStatusValue": "Active",
        "LifecyclePhaseValue": "Active",
        "ItemClass": item_class,
        "PrimaryUOMValue": "kg",
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.create_item.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = mock_api_response

        tool_response = oracle_fusion_create_item(
            organization_code=org_code,
            item_number=item_num,
            item_description=item_desc,
        )

        assert tool_response.success is True
        assert f"Successfully created item '{item_num}'" in tool_response.message

        assert tool_response.content is not None
        assert isinstance(tool_response.content, OracleFusionItem)

        output_item = tool_response.content
        assert output_item.organization_code == org_code
        assert output_item.item_number == item_num

        expected_payload = {
            "OrganizationCode": org_code,
            "ItemNumber": item_num,
            "ItemDescription": item_desc,
            "ItemStatusValue": "Active",
            "LifecyclePhaseValue": "Active",
            "ItemClass": item_class,
            "PrimaryUOMValue": "Ea",
            "CustomerOrderEnabledFlag": "true",
            "CustomerOrderFlag": "true",
        }

        mock_client.post_request.assert_called_once_with(
            resource_name="itemsV2", payload=expected_payload
        )


def test_create_supplier_item_api_error() -> None:
    """Tests how the function handles a generic error response from the API."""
    org_code = 204
    item_num = "FAIL-ITEM-001"
    item_desc = "This item will fail to be created"

    mock_api_error_response = {
        "errors": [{"title": "Invalid Attribute", "detail": "Organization ID does not exist."}]
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.create_item.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = mock_api_error_response

        tool_response = oracle_fusion_create_item(
            organization_code=org_code,
            item_number=item_num,
            item_description=item_desc,
        )

        assert tool_response.success is False
        assert "Invalid Attribute" in tool_response.message
        assert tool_response.content is None
