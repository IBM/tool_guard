from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.update_item import (
    coupa_update_item,
)


def test_coupa_update_item() -> None:
    """test the update_item tool."""

    item_id = 2694
    item_name = "Full Item"
    item_number = "FULL-095"
    desc = "Full description"
    item_type = "Item"
    expected_payload = {
        "name": item_name,
        "item-number": item_number,
        "item-type": item_type,
        "description": desc,
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.update_item.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = expected_payload | {"id": item_id}

        params = {"fields": '["id", "item-number", "name", "description", "item-type", "active"]'}

        result = coupa_update_item(
            item_id=item_id,
            name=item_name,
            item_number=item_number,
            item_type=item_type,
            description=desc,
        ).content

        assert result
        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"items/{item_id}", params=params, payload=expected_payload
        )
